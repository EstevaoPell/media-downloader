# Media Downloader

Aplicação desktop para Windows desenvolvida em Python com interface gráfica (`CustomTkinter`) que utiliza `yt-dlp` e `FFmpeg` para baixar e converter mídias em **MP4 (H.264/AAC)**, **MP3** ou **OGG Vorbis**.

## Download (Executável Pronto)

1. Acesse a seção **Releases** no menu lateral direito desta página.
2. Baixe o arquivo **`MediaDownloader.exe`** da versão mais recente.
3. Execute o programa, cole o link desejado, escolha a pasta de destino e o formato de saída.

> **Nota:** Como o executável não possui certificado digital comercial, o Windows SmartScreen pode exibir um aviso na primeira execução. Clique em **Mais informações** > **Executar assim mesmo**.

## Isenção de Responsabilidade (Disclaimer)

- Este software é apenas uma interface gráfica (*wrapper*) local que automatiza comandos para as ferramentas públicas `yt-dlp` e `FFmpeg`.
- Este projeto **não hospeda, indexa, armazena nem distribui** arquivos de áudio ou vídeo.
- Esta ferramenta **não contorna nem remove** mecanismos de proteção digital (DRM).
- O uso deste programa destina-se exclusivamente ao download de mídias de autoria própria, em domínio público, sob licenças Creative Commons ou com autorização expressa do detentor dos direitos. O usuário é o único responsável por cumprir os Termos de Serviço das plataformas e a legislação de direitos autorais vigente.

## Executando via Código-Fonte

Caso prefira rodar diretamente pelo Python (requer `yt-dlp` e `ffmpeg` instalados no `PATH` do sistema):

```bash
pip install -r requirements.txt
python downloader.py