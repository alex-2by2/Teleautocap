
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import channels

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode="HTML")

def make_buttons(buttons):
    kb = InlineKeyboardMarkup()
    for b in buttons:
        kb.add(InlineKeyboardButton(b["text"], url=b["url"]))
    return kb

@bot.channel_post_handler(content_types=['photo', 'video'])
def handle_channel_post(message):
    ch = channels.find_one({"channel_id": message.chat.id})
    if not ch:
        return

    base = ch["photo_caption"] if message.photo else ch["video_caption"]
    caption = ch["template"].replace("{caption}", base) + "\n\n" + ch["footer"]

    try:
        bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.message_id,
            caption=caption,
            reply_markup=make_buttons(ch.get("buttons", []))
        )
    except:
        pass

print("🤖 Bot running")
bot.infinity_polling()
