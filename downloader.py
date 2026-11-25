import os
import subprocess
import sys
import threading
from tkinter import filedialog
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def get_bin_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


class MediaDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Media Downloader")
        self.geometry("580x440")
        self.resizable(False, False)

        self.bin_dir = get_bin_dir()
        self.yt_dlp = (
            os.path.join(self.bin_dir, "yt-dlp.exe")
            if getattr(sys, "frozen", False)
            else "yt-dlp"
        )
        self.save_dir = os.getcwd()

        self._build_ui()

    def _build_ui(self):
        # Título
        self.lbl_title = ctk.CTkLabel(
            self, text="Media Downloader", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl_title.pack(pady=(20, 4))

        self.lbl_sub = ctk.CTkLabel(
            self,
            text="Baixe vídeos e áudios em MP4, MP3 ou OGG Vorbis",
            font=ctk.CTkFont(size=13),
            text_color="gray70",
        )
        self.lbl_sub.pack(pady=(0, 18))

        # Frame URL
        frame_url = ctk.CTkFrame(self, fg_color="transparent")
        frame_url.pack(fill="x", padx=30, pady=6)

        self.entry_url = ctk.CTkEntry(
            frame_url, placeholder_text="Cole o link do YouTube aqui...", height=38
        )
        self.entry_url.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_paste = ctk.CTkButton(
            frame_url, text="Colar", width=75, height=38, command=self.colar_link
        )
        self.btn_paste.pack(side="right")

        # Frame Pasta de Destino
        frame_dir = ctk.CTkFrame(self, fg_color="transparent")
        frame_dir.pack(fill="x", padx=30, pady=6)

        self.lbl_dir = ctk.CTkLabel(
            frame_dir,
            text=f"Salvar em: {self.save_dir}",
            font=ctk.CTkFont(size=12),
            text_color="gray80",
            anchor="w",
        )
        self.lbl_dir.pack(side="left", fill="x", expand=True)

        self.btn_dir = ctk.CTkButton(
            frame_dir,
            text="Alterar Pasta",
            width=110,
            height=30,
            fg_color="gray30",
            hover_color="gray40",
            command=self.escolher_pasta,
        )
        self.btn_dir.pack(side="right")

        # Seletor de Formato
        self.lbl_fmt = ctk.CTkLabel(
            self, text="Formato de saída:", font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_fmt.pack(pady=(14, 6))

        self.formato_var = ctk.StringVar(value="MP4")
        self.seg_formato = ctk.CTkSegmentedButton(
            self,
            values=["MP4 (Vídeo + Som)", "MP3 (Áudio)", "OGG (Vorbis)"],
            variable=self.formato_var,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.seg_formato.set("MP4 (Vídeo + Som)")
        self.seg_formato.pack(fill="x", padx=30)

        # Botão Baixar
        self.btn_download = ctk.CTkButton(
            self,
            text="Baixar Agora",
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.iniciar_download,
        )
        self.btn_download.pack(fill="x", padx=30, pady=(20, 10))

        # Barra de Progresso e Status
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=30, pady=(4, 8))
        self.progress.set(0)

        self.lbl_status = ctk.CTkLabel(
            self,
            text="Pronto para baixar.",
            font=ctk.CTkFont(size=12),
            text_color="gray75",
            wraplength=510,
        )
        self.lbl_status.pack(pady=(2, 15))

    def colar_link(self):
        try:
            texto = self.clipboard_get().strip()
            self.entry_url.delete(0, "end")
            self.entry_url.insert(0, texto)
        except Exception:
            pass

    def escolher_pasta(self):
        pasta = filedialog.askdirectory(initialdir=self.save_dir)
        if pasta:
            self.save_dir = os.path.normpath(pasta)
            self.lbl_dir.configure(text=f"Salvar em: {self.save_dir}")

    def iniciar_download(self):
        url = self.entry_url.get().strip()
        if not url:
            self.lbl_status.configure(
                text="Por favor, cole um link válido primeiro.", text_color="#ff6b6b"
            )
            return

        self.btn_download.configure(state="disabled", text="Baixando...")
        self.lbl_status.configure(
            text="Conectando e processando mídia... Aguarde.", text_color="#4dabf7"
        )
        self.progress.start()

        thread = threading.Thread(
            target=self._executar_ytdlp, args=(url, self.formato_var.get()), daemon=True
        )
        thread.start()

    def _executar_ytdlp(self, url, formato):
        base_cmd = [self.yt_dlp, "--no-playlist", "-P", self.save_dir]
        if getattr(sys, "frozen", False):
            base_cmd += ["--ffmpeg-location", self.bin_dir]

        if "MP4" in formato:
            cmd = base_cmd + [
                "-S",
                "vcodec:h264,res,acodec:m4a",
                "--merge-output-format",
                "mp4",
                "-o",
                "%(title)s.%(ext)s",
                url,
            ]
        elif "MP3" in formato:
            cmd = base_cmd + [
                "-x",
                "--audio-format",
                "mp3",
                "--audio-quality",
                "0",
                "-o",
                "%(title)s.%(ext)s",
                url,
            ]
        else:
            cmd = base_cmd + [
                "-x",
                "--audio-format",
                "vorbis",
                "--audio-quality",
                "0",
                "-o",
                "%(title)s.%(ext)s",
                url,
            ]

        # Oculta qualquer janela preta secundaria do yt-dlp/ffmpeg no Windows
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        try:
            resultado = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                startupinfo=startupinfo,
            )
            self.after(0, self._finalizar_download, resultado.returncode == 0)
        except Exception as e:
            self.after(0, self._finalizar_download, False, str(e))

    def _finalizar_download(self, sucesso, erro=""):
        self.progress.stop()
        self.progress.set(1 if sucesso else 0)
        self.btn_download.configure(state="normal", text="Baixar Agora")

        if sucesso:
            self.lbl_status.configure(
                text=f"Concluído com sucesso! Salvo em: {self.save_dir}",
                text_color="#51cf66",
            )
            self.entry_url.delete(0, "end")
        else:
            msg = f"Erro no download. {erro}".strip()
            self.lbl_status.configure(text=msg, text_color="#ff6b6b")


if __name__ == "__main__":
    app = MediaDownloaderApp()
    app.mainloop()