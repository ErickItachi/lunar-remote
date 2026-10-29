# Recursos oficiais da Lunar House

`site-assets.json` registra as referências encontradas nos HTMLs fornecidos e
separa URLs explícitas de caminhos inferidos dos arquivos salvos pelo navegador.
**Nenhum desses recursos foi baixado ainda.** O HTML não contém imagens, fontes
ou a folha de estilo da marca incorporadas.

As solicitações HTTPS ao CSS e ao logotipo retornaram HTTP 403 pelo proxy do
ambiente. A liberação de `lunarhouse.com.br` e `www.lunarhouse.com.br` existe no
rascunho das configurações, mas não está aplicada à instância atual. Salvar o
rascunho não muda a política de rede em execução.

Após aplicar a configuração, retomar o download a partir do site oficial e
verificar os nomes atuais dos bundles, que podem mudar em cada publicação.
Registrar os hashes dos recursos efetivamente obtidos antes de usá-los na UI.
Extrair a paleta e a tipografia do CSS oficial; não usar as cores do widget de
notificações como identidade da empresa. Não incorporar o JavaScript do site ou
o chat Digisac no aplicativo desktop.

Alternativa offline: a pasta `Lunar House_files` gerada junto ao HTML salvo pelo
navegador contém os recursos referenciados; ela pode ser fornecida em um ZIP.
