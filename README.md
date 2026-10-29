# Lunar Remote

Projeto de acesso remoto da **Lunar House Tecnologia**, baseado no motor real do
[RustDesk](https://github.com/rustdesk/rustdesk). Este projeto não é um produto
oficial nem endossado pelos desenvolvedores do RustDesk.

**Estado: desenvolvimento inicial.** A base desktop importada ainda tem a marca
RustDesk. Não há executáveis Lunar Remote, instaladores ou releases validados.
Windows 10/11 x64 portátil é a prioridade, seguido de instalador Windows e macOS.

## O que já funciona nesta etapa

- Checkout da base RustDesk 1.4.9 e submódulo fixados em commits verificáveis.
- Contêiner Linux com compiladores, GTK, áudio, Protobuf e dependências de sistema.
- Sete testes originais do codec de rede executados com as versões do lockfile.
- RustDesk Server OSS 1.1.16 em Docker Compose com imagens fixadas por digest.
- Testes reais de sinalização TCP, registro UDP, rejeição de chave incorreta e
  transporte de bytes nos dois sentidos pelo relay, dentro de uma rede isolada.
- Workflow Lunar para executar as validações do codec e do servidor, sem publicar releases.

Esses testes não comprovam captura de tela, autenticação de uma sessão desktop,
controle de teclado/mouse nem distribuição para Windows/macOS.

## Desenvolvimento

Leia [o estado e a arquitetura](docs/LUNAR-DEVELOPMENT.md) e
[o ambiente Linux](dev/README.md). Nesta máquina:

```sh
bash dev/run.sh cargo metadata --locked --no-deps --format-version 1
bash dev/run.sh python3 dev/test-codec.py
bash infra/server/smoke.sh
```

O script de preparação salvo nas configurações do ambiente instala/ativa Rust e
constrói a imagem de desenvolvimento. O build desktop completo ainda depende de
Flutter, vcpkg/codecs, geração da ponte Flutter/Rust e acesso de rede liberado.
Não altere lockfiles para contornar esses requisitos.

## Infraestrutura

O [guia do servidor OSS](infra/server/README.md) cobre configuração, portas,
persistência da identidade e backups. Não há VPS, domínio ou chave de produção
configurados. Nenhuma infraestrutura pública foi implantada.

## Marca e distribuição

Os arquivos HTML fornecidos referenciam CSS e logotipos externos ainda indisponíveis.
A identidade visual deve ser extraída dos recursos oficiais antes da personalização.
Os workflows nativos herdados permanecem como referência, com a publicação noturna
e por tags desativada. Não há certificado de assinatura nem notarização configurados.

## Origem e licença

- RustDesk: tag `1.4.9`, commit `6c578292e8ebbbec708b76986ba8c4bc7c509747`.
- `hbb_common`: commit `7e1c392c62d39c364127307cd408421dd5f8cfb0`.
- [AGPL-3.0](LICENCE), atribuições e licenças de terceiros devem ser preservadas.
- [README original](README.upstream.md) preservado como referência técnica.

Ao distribuir versões modificadas, disponibilize o código-fonte correspondente,
incluindo alterações e instruções de build, e revise as obrigações de todas as
dependências. Não use a marca RustDesk para sugerir endosso ao Lunar Remote.
