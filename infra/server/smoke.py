"""Functional checks against an isolated RustDesk Server OSS deployment.

Generate rendezvous_pb2.py from libs/hbb_common/protos/rendezvous.proto first.
Run inside the Compose network with the server-data volume mounted read-only.
No desktop session is created and no private key is read.
"""

import os
from pathlib import Path
import socket
import time
import unittest
import uuid

import rendezvous_pb2 as proto


HBBS = os.environ.get("SMOKE_HBBS", "hbbs")
HBBR = os.environ.get("SMOKE_HBBR", "hbbr")
PUBLIC_KEY_PATH = Path(os.environ.get("SMOKE_PUBLIC_KEY", "/data/id_ed25519.pub"))
TIMEOUT = 5


def frame(message):
    payload = message.SerializeToString()
    for size in range(1, 5):
        if len(payload) < (1 << (size * 8 - 2)):
            return ((len(payload) << 2) | (size - 1)).to_bytes(size, "little") + payload
    raise ValueError("Oversized test message")


def read_exact(stream, length):
    result = bytearray()
    while len(result) < length:
        chunk = stream.recv(length - len(result))
        if not chunk:
            raise EOFError("Server closed the connection before the expected response")
        result.extend(chunk)
    return bytes(result)


def receive_message(stream):
    first = read_exact(stream, 1)
    size = (first[0] & 3) + 1
    header = first + read_exact(stream, size - 1)
    length = int.from_bytes(header, "little") >> 2
    if length > 65536:
        raise ValueError("Unexpected response length")
    return proto.RendezvousMessage.FromString(read_exact(stream, length))


class ServerSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        deadline = time.monotonic() + 20
        while True:
            try:
                cls.public_key = PUBLIC_KEY_PATH.read_text().strip()
                if cls.public_key:
                    break
            except FileNotFoundError:
                pass
            if time.monotonic() >= deadline:
                raise RuntimeError("The server has not generated a public identity")
            time.sleep(0.25)
        # Readiness retries are bounded; assertions below exercise the protocol.
        for host, port in [(HBBS, 21115), (HBBS, 21116), (HBBR, 21117)]:
            deadline = time.monotonic() + 20
            while True:
                try:
                    with socket.create_connection((host, port), timeout=1):
                        break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise
                    time.sleep(0.25)

    def test_hbbs_nat_discovery(self):
        for port in (21115, 21116):
            with self.subTest(port=port):
                with socket.create_connection((HBBS, port), timeout=TIMEOUT) as stream:
                    stream.sendall(frame(proto.RendezvousMessage(
                        test_nat_request=proto.TestNatRequest(serial=0))))
                    response = receive_message(stream)
                    self.assertEqual(response.WhichOneof("union"), "test_nat_response")
                    self.assertEqual(response.test_nat_response.port, stream.getsockname()[1])

    def test_hbbs_udp_requests_device_identity(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as stream:
            stream.settimeout(TIMEOUT)
            request = proto.RendezvousMessage(register_peer=proto.RegisterPeer(
                id=str(uuid.uuid4().int)[:12]))
            stream.sendto(request.SerializeToString(), (HBBS, 21116))
            packet, _ = stream.recvfrom(65536)
            response = proto.RendezvousMessage.FromString(packet)
            self.assertEqual(response.WhichOneof("union"), "register_peer_response")
            self.assertTrue(response.register_peer_response.request_pk)

    def test_hbbr_rejects_incorrect_server_key(self):
        with socket.create_connection((HBBR, 21117), timeout=TIMEOUT) as stream:
            stream.sendall(frame(proto.RendezvousMessage(request_relay=proto.RequestRelay(
                uuid=str(uuid.uuid4()), licence_key="incorrect-smoke-key"))))
            try:
                self.assertEqual(stream.recv(1), b"")
            except ConnectionResetError:
                pass  # An explicit reset also rejects the unauthenticated peer.

    def test_hbbr_transfers_bytes_in_both_directions(self):
        session = str(uuid.uuid4())
        request = proto.RendezvousMessage(request_relay=proto.RequestRelay(
            uuid=session, licence_key=self.public_key))
        with socket.create_connection((HBBR, 21117), timeout=TIMEOUT) as first:
            first.sendall(frame(request))
            # Queueing bytes after the request also checks framed-to-raw switching.
            forward = b"Lunar Remote isolated relay probe\x00\xff"
            first.sendall(forward)
            with socket.create_connection((HBBR, 21117), timeout=TIMEOUT) as second:
                second.sendall(frame(request))
                self.assertEqual(read_exact(second, len(forward)), forward)
                backward = b"relay response\xff\x00"
                second.sendall(backward)
                self.assertEqual(read_exact(first, len(backward)), backward)


if __name__ == "__main__":
    unittest.main(verbosity=2)
