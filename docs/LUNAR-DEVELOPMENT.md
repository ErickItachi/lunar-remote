# Lunar Remote — estado inicial de desenvolvimento

## Origem verificável

- Repositório de destino: `ErickItachi/lunar-remote` (sem refs remotas na consulta inicial).
- Base: https://github.com/rustdesk/rustdesk, tag `1.4.9`.
- Commit: `6c578292e8ebbbec708b76986ba8c4bc7c509747`.
- Submódulo `libs/hbb_common`: `7e1c392c62d39c364127307cd408421dd5f8cfb0`.
- Branch de trabalho: `development/lunar-remote`.
- Licença original preservada em `LICENCE`; manter atribuições e disponibilizar o código modificado conforme AGPL-3.0.

Esta importação ainda é o RustDesk original. Não constitui uma distribuição Lunar Remote personalizada ou validada. Os workflows importados são os de upstream e precisam de revisão antes de execução/publicação; não publicar releases automaticamente nesta etapa.

## Arquitetura e plano de adaptação

Preservar o protocolo e autenticação em `src/rendezvous_mediator.rs`, o motor de sessão em `src/client.rs` e `src/server/`, captura em `libs/scrap`, entrada em `libs/enigo` e configurações compartilhadas em `libs/hbb_common`. A UI desktop atual fica em `flutter/lib/desktop`; o código em `src/ui` é a interface legada Sciter.

Separar personalização visual de alterações do motor. Revisar a inicialização de `APP_NAME`, diretórios de configurações, identificadores de pacotes, recursos Windows/macOS e instaladores em conjunto, evitando substituição textual indiscriminada de RustDesk. Preservar avisos legais e todos os controles de consentimento. Não configurar servidor, chave, acesso permanente ou elevação automática sem dados e autorização próprios.

Prioridade: Windows x64 portátil e instalável, depois macOS x64/ARM64. Builds nativos exigem Windows/MSVC e macOS/Xcode respectivamente; esta máquina Linux não comprova esses artefatos.

## Ferramentas e validação nesta máquina

Rust 1.75.0 instalado em `/workspace/toolchains`, com checksum do instalador oficial verificado. Ativação:

```sh
export CARGO_HOME=/workspace/toolchains/cargo
export RUSTUP_HOME=/workspace/toolchains/rustup
export PATH="$CARGO_HOME/bin:$PATH"
cd /workspace/lunar-remote
git submodule update --init --recursive
cargo metadata --locked --no-deps --format-version 1
cargo test --locked -p hbb_common --lib --no-default-features
```

Resultado: metadata do workspace validada; testes bloqueados durante resolução de dependências pelo acesso negado a `chromium.googlesource.com` (libwebm). Nenhum teste executado. A instalação apt de bibliotecas nativas também foi bloqueada por ausência de privilégios administrativos. Flutter, CMake, Ninja, Clang e bibliotecas de desenvolvimento ainda precisam ser provisionados.

Referência de versões: `.github/workflows/flutter-build.yml` fixa Flutter 3.24.5 para Windows x64, Rust 1.75, Rust 1.81 para macOS e vcpkg `120deac3062162151622ca4860575a33844ba10b`. Não atualizar os lockfiles para contornar dependências. Antes de compilar, conferir requisitos específicos do job e gerar a ponte Flutter/Rust conforme `.github/workflows/bridge.yml`.

## Marca e recursos pendentes

O HTML fornecido identifica título Lunar House, mas contém somente um contêiner React e referências externas. Não contém paleta, fontes ou imagens incorporadas. Recursos referenciados:

- `/assets/index-Dnm6iH6E.css`
- `/assets/index-CwaV5c-e.js`
- `/assets/lunar-site.png`
- `/favicon.png`

O acesso ao site foi negado pelo proxy (CONNECT 403). Obter esses recursos pelo site após liberar o domínio, ou por arquivos fornecidos pelo responsável. Não copiar o widget Digisac para o aplicativo desktop.

O segundo arquivo fornecido, `Lunar House.htm`, contém o DOM renderizado (aproximadamente 100 KB), mas continua referenciando uma pasta externa `Lunar House_files` não incluída no anexo. Ele identifica o logotipo `lunarcompleto-branco-D5O5pA7d.png`, além do CSS `index-Dnm6iH6E.css`. O estilo incorporado pertence às notificações Sonner; suas cores não estabelecem a paleta da marca. Solicitar a pasta de recursos compactada ou aplicar a liberação de rede antes de extrair a identidade visual completa.

## Critérios ainda não verificados

Nenhum executável, instalador, DMG ou release gerado. Nenhuma conexão remota, captura, controle, instalação, desinstalação, assinatura ou notarização testada. Faltam personalização visual, revisão de workflows, infraestrutura hbbs/hbbr, endereços e chave pública reais e máquinas Windows/macOS para validação. Não declarar o produto nem o ambiente completos antes de resolver os bloqueios e executar as validações correspondentes.
