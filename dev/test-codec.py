#!/usr/bin/env python3
"""Run upstream codec unit tests independently of desktop-only dependencies.

The library source is used unchanged and dependency versions come from the main
lockfile. The temporary harness never updates repository manifests/lockfiles.
This is a focused check, not the full hbb_common or desktop test suite.
"""

from pathlib import Path
import subprocess
import tempfile
import tomllib


root = Path(__file__).resolve().parents[1]
lock = tomllib.loads((root / "Cargo.lock").read_text())
dependencies = ["bytes", "tokio", "tokio-util", "futures-core", "futures-sink", "pin-project-lite"]
manifest = (
    '[package]\nname = "lunar-codec-check"\nversion = "0.0.0"\nedition = "2021"\n'
    '\n[lib]\npath = "' + str(root / "libs/hbb_common/src/bytes_codec.rs") + '"\n'
    '\n[dependencies]\n'
)
for name in dependencies:
    matches = [p for p in lock["package"] if p["name"] == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one locked version of {name}")
    version = matches[0]["version"]
    features = ', features = ["codec"]' if name == "tokio-util" else ""
    manifest += f'{name} = {{ version = "={version}", default-features = false{features} }}\n'

with tempfile.TemporaryDirectory(prefix="lunar-codec-") as directory:
    path = Path(directory) / "Cargo.toml"
    path.write_text(manifest)
    subprocess.run(["cargo", "+1.75.0", "test", "--manifest-path", str(path), "--lib"], check=True)
