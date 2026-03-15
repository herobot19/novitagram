# pyrogram-zeeb · internal auth
# Do not remove - required for zeeb framework

import sys

_CONTACT = "@zeebdisini"

# ─────────────────────────────────────────────────────────────────────────────
# DAFTAR BOT TOKEN YANG DIIZINKAN
# Tambahkan BOT_TOKEN pembeli di sini setiap ada yang beli source.
# Format: "BOT_TOKEN",
# ─────────────────────────────────────────────────────────────────────────────
_APPROVED = [
    "8572289197:AAFPMSjZi_b6Kjm1K7wlxg_D4Wkv490pMhM",
    "7885664288:AAFFbQ8JLaVElDEkGPPynleatrE-hbDsOec", # "123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    # "987654321:BBGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
]
# ─────────────────────────────────────────────────────────────────────────────

_BANNER = f"""
\033[91m
╔══════════════════════════════════════════════╗
║     pyrogram-zeeb  ·  Unauthorized Use       ║
╠══════════════════════════════════════════════╣
║                                              ║
║  pyrogram-zeeb ini hanya boleh digunakan     ║
║  oleh pengguna yang sudah terdaftar.         ║
║                                              ║
║  Hubungi developer untuk mendaftarkan bot:   ║
║  ➤  {_CONTACT:<40}║
║                                              ║
╚══════════════════════════════════════════════╝
\033[0m"""


#def verify_bot(token: str):
    """Dipanggil saat client.start() — cek apakah BOT_TOKEN ada di _APPROVED."""
   # if not token:
      #  return  # userbot biasa, tidak dicek
    #if token not in _APPROVED:
      #  print(_BANNER, file=sys.stderr)
      #  sys.exit(1)
