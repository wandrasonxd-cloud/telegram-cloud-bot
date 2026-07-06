import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá!\n\n"
        "Envie uma foto, vídeo ou documento e eu vou guardá-lo."
    )

async def salvar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        tipo = "📷 Foto"

    elif update.message.video:
        file_id = update.message.video.file_id
        tipo = "🎥 Vídeo"

    elif update.message.document:
        file_id = update.message.document.file_id
        tipo = "📄 Documento"

    else:
        return

    with open("arquivos.txt", "a", encoding="utf-8") as f:
        f.write(f"{tipo}|{file_id}\n")

    await update.message.reply_text(f"{tipo} salvo com sucesso!")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.Document.ALL,
        salvar,
    )
)

app.run_polling()
