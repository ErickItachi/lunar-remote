# Ambiente Linux de desenvolvimento

O ambiente principal roda como usuário sem privilégios apt. As dependências
nativas são instaladas em `lunar-remote-dev:bookworm`, construído por este projeto.
Rust 1.75.0 fica em `/workspace/toolchains` e é montado no contêiner; a imagem
de desenvolvimento não contém credenciais, fontes ou certificados da sessão.

## Uso nesta máquina

```sh
cd /workspace/lunar-remote
bash dev/run.sh cargo metadata --locked --no-deps --format-version 1
bash dev/run.sh python3 dev/test-codec.py
bash dev/run.sh bash
```

`run.sh` verifica o daemon Docker local, reutiliza camadas de build, monta o
checkout e as ferramentas e executa como seu UID/GID para preservar a propriedade
dos arquivos. A CA combinada do sistema é montada somente para a sessão; TLS
permanece habilitado. `LUNAR_CA_BUNDLE` permite selecionar outro bundle confiável.
Mantenha a configuração de proxy e autenticação Docker fornecida pela plataforma.
Não exponha o socket Docker ao contêiner de desenvolvimento.

Ferramentas verificadas: Rust/Cargo 1.75.0, Clang 14, CMake 3.25.1, Ninja 1.11.1,
GTK 3.24.38, ALSA 1.2.8, PulseAudio 16.1 e protoc 3.21.12.

## Validação delimitada

`test-codec.py` compila diretamente o arquivo original
`libs/hbb_common/src/bytes_codec.rs` em um harness temporário. Ele fixa suas seis
dependências às versões do `Cargo.lock` principal e executa sete testes, incluindo
limite de pré-alocação para cabeçalhos grandes. Não altera o workspace original.
Não equivale a executar todo `hbb_common` nem o aplicativo desktop.

O comando do workspace completo continua sendo:

```sh
bash dev/run.sh cargo test --locked -p hbb_common --lib --no-default-features
```

Sua resolução inclui dependências desktop como libwebm e ainda está bloqueada pela
política atual para `chromium.googlesource.com`. A liberação foi salva no rascunho
do ambiente; ela precisa ser aplicada nas configurações. Não use espelhos para
contornar uma negação de política.

## Requisitos restantes do desktop

- Flutter 3.24.5 para a UI desktop e dependências de `flutter/pubspec.lock`.
- Ponte gerada conforme `.github/workflows/bridge.yml`.
- vcpkg no commit `120deac3062162151622ca4860575a33844ba10b` e codecs nativos.
- Runners Windows/MSVC e macOS/Xcode para os respectivos pacotes.
- Testes em computadores autorizados, incluindo conexões entre redes distintas.

Consulte os jobs originais de `.github/workflows/flutter-build.yml` para detalhes
por plataforma. Eles são referências de upstream, não builds Lunar verificados.
Cada tarefa da nuvem já é isolada: use este checkout e não crie worktrees sem
solicitação explícita.
