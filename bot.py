import logging

logging.basicConfig(level=logging.INFO)

import os
from swibots import Client, BotCommand, BotContext, CommandEvent, MessageEvent
from config import Config
from pdfquery import PDFQuery
from pypdf import PdfReader

Client = Client(Config.BOT_TOKEN)

Client.set_bot_commands(
    [
        BotCommand("start", "Get Start message", True),
        BotCommand("clear", "Clear conversation", True),
    ]
)

CONFIG = {}


@Client.on_command("start")
async def startMessage(ctx: BotContext[CommandEvent]):
    event = ctx.event.message
    await event.reply_text(
        "Hi, I am PDF-GPT\n\n🪄 Send me a pdf to update your config\n📚 Answer your related questions."
    )


@Client.on_command("clear")
async def clearConv(ctx: BotContext[CommandEvent]):
    m = ctx.event.message
    user_id = m.user_session_id or m.channel_id or m.group_id or int(ctx.event.action_by_id)
    if not CONFIG.get(user_id):
        return
    pdf = CONFIG[user_id]["pdf"]
    pdf.forget()
    message = "☑️ Conversation has been cleared!"
    await ctx.event.message.send(message)


@Client.on_message()
async def onMessage(ctx: BotContext[MessageEvent]):
    event = ctx.event.message
    chat_id = event.user_session_id or event.channel_id or event.group_id or event.user_id

    if not CONFIG.get(chat_id):
        CONFIG[chat_id] = {"pdf": PDFQuery(Config.OPEN_AI_KEY)}

    pdfquery: PDFQuery = CONFIG[event.user_id]["pdf"]
    if event.media_link and event.media_link.endswith(".pdf"):
        msg = await event.reply_text("🪄 Downloading PDF..")
        file = await event.download("downloads")
        with open(file, "rb") as f:
            reader = PdfReader(f)
            metadata = reader.metadata
            numPage = len(reader.pages)
        msg = await msg.edit_text(
            f"Loading *{metadata.title if metadata else os.path.basename(file)}*\n🪇 Total Pages: {numPage}\n🥤 Hold back, This may take some while..."
        )
        pdfquery.ingest(file)
        os.remove(file)
        await msg.delete()
        await event.reply_text("📂 Added Pdf!\n❓ Send your question!")
        return
    if not pdfquery.db:
        await event.reply_text("Provide me a pdf first!")
        return
    answer = pdfquery.ask(event.message)
    if answer:
        await event.reply_text(answer)


if __name__ == "__main__":
    Client.run()
