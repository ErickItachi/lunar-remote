# Servidor Lunar — RustDesk Server OSS

Este Compose prepara `hbbs` (registro/sinalização/NAT) e `hbbr` (relay). As imagens
oficiais 1.1.16 estão fixadas por digest. Um helper BusyBox sem acesso à rede
aguarda a criação da identidade compartilhada antes de iniciar o relay.

Não inclui console de gerenciamento, API comercial, catálogo central de
dispositivos ou recursos exclusivos do Server Pro. O código-fonte do servidor
OSS é [rustdesk/rustdesk-server](https://github.com/rustdesk/rustdesk-server),
tag 1.1.16, commit `73523b31cfd25d77dee862e6fc9f5e1fb5e485ef`.

## Validar localmente

Requisitos: Docker, Compose 2.24.4 ou superior (suporte a `!reset`) e a imagem
de desenvolvimento construída conforme `dev/README.md`.

```sh
cd /workspace/lunar-remote
bash infra/server/smoke.sh
```

O script cria rede e volume exclusivos, não publica portas, gera classes Protobuf
diretamente do protocolo importado e verifica:

1. Respostas NAT reais nas portas TCP 21115 e 21116.
2. Registro UDP de um ID temporário solicitando a identidade pública do dispositivo.
3. Rejeição de uma chave de servidor incorreta pelo relay.
4. Transferência real de bytes nos dois sentidos entre dois clientes do relay.
5. Preservação da identidade pública após restart e repetição dos quatro testes.

Ao sair, remove somente seus próprios contêineres, rede e volume temporários.
A chave privada não é lida pelo teste. Não use esse teste contra produção: ele
registra um ID efêmero e abre conexões de teste. Ele não valida uma sessão desktop,
criptografia ponta a ponta de uma sessão, consentimento, controle remoto nem P2P
entre redes distintas.

## Preparar uma VPS Linux

1. Provisione Docker/Compose, DNS e firewall na VPS escolhida.
2. Copie `.env.example` para `.env` nesta pasta.
3. Preencha `LUNAR_RELAY_HOST` com o endereço real do relay e porta `21117`.
   Não inclua `https://`: o protocolo desktop não é HTTP.
4. O bind padrão é `127.0.0.1`, para validação local. Para atender clientes na VPS,
   defina explicitamente `LUNAR_BIND_ADDRESS=0.0.0.0` e configure o firewall.
5. Execute a partir de `infra/server`:

```sh
docker compose -p lunar-server config --quiet
docker compose -p lunar-server up -d --wait --wait-timeout 45
docker compose -p lunar-server ps
```

`up --wait` comprova a partida dos processos; faça a validação de protocolo e os
testes com clientes autorizados antes de abrir a distribuição. Nenhuma VPS foi
implantada ou validada neste trabalho.

| Porta | Protocolo | Finalidade |
| --- | --- | --- |
| 21115 | TCP | Detecção NAT |
| 21116 | TCP e UDP | Registro e sinalização |
| 21117 | TCP | Relay |

Não há portas WebSocket publicadas: o escopo é o cliente desktop nativo.
Uma proxy HTTP comum não substitui essas portas. Garanta encaminhamento TCP/UDP
correto se a VPS estiver atrás de NAT. O endereço anunciado pelo relay precisa ser
alcançável pelos clientes externos; `hbbr:21117` só serve à rede Docker de teste.

## Identidade, configuração do cliente e backup

O volume persistente `lunar-server_server-data` guarda o banco de registro e
`id_ed25519`/`id_ed25519.pub`. `-k _` exige a chave pública correspondente nos
clientes. Essa chave identifica o servidor; não substitui a senha temporária,
confirmação de acesso ou criptografia da sessão desktop.

Exporte **somente a chave pública** para configurar o cliente:

```sh
docker compose -p lunar-server cp hbbs:/data/id_ed25519.pub ./server-key.pub
```

O cliente deverá usar o endereço real do hbbs, o relay real e essa chave pública.
A incorporação centralizada desses valores no build Lunar ainda está pendente;
nenhum endereço ou chave de produção foi inventado. Não distribua a chave privada.

Faça backup consistente do volume com os serviços parados e armazene a cópia em
local privado, fora do Git e do diretório público de distribuição. Restrinja o
acesso à VPS, ao daemon Docker e aos backups. Preserve a chave original ao
restaurar; substituí-la exige atualizar a confiança dos clientes. Nunca execute
`docker compose down -v` em produção sem uma decisão explícita de apagar dados.
Para uma parada normal, use `docker compose -p lunar-server down`, sem `-v`.

## Operação e custos

Os serviços reiniciam com o Docker; dados permanecem no volume e logs têm rotação.
Acompanhe espaço em disco, atualizações de segurança e tráfego do relay. Há custos
possíveis de VPS, domínio, backup e banda, mesmo usando software OSS gratuito.
Não há assinatura digital, credenciais comerciais nem infraestrutura paga
configuradas por estes arquivos.
