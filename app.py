import os
import pafy
import logging
from datetime import datetime
from telegram import *
from telegram.ext import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


BOT_TOKEN = os.getenv("BOT_API")
YT_TOKEN = os.getenv("YT_API")

url = ""

def youtube(update, context):
  
  global url
  url = update.message.text
  
  menu = InlineKeyboardMarkup([[ 
           InlineKeyboardButton(text="🎬 Video", callback_data = "video"),
           InlineKeyboardButton(text="🎵 Audio", callback_data = "audio")
         ]])

  update.message.reply_text(text="Choose one to get download url.", reply_markup = menu)




def youtube_handler(update, context):
  
  query = update.callback_query
  query.answer()
  
  pafy.set_api_key(YT_TOKEN)
  content = pafy.new(url)
  streams = content.streams if query.data == "video" else content.audiostreams
  
  results = []
  reply_markup = InlineKeyboardMarkup(results)
  
  for item in streams:
    results.append([InlineKeyboardButton(text = f"{item.resolution if query.data == 'video' else item.bitrate} {item.extension}", url=item.url)])
  
  date = datetime.strptime(content.published, "%Y-%m-%d %H:%M:%SZ").date()
  
  query.edit_message_text(
    f"""*{content.title}*
    
    
    🤖 Channel: {content.author} 
    👁️ Views: {beauty(content.viewcount)}
    📆 Upload: {date}
    ♥️ Like: {beauty(content.likes)}
    ⭐ Rating: {beauty(content.rating)} 
    
 
    🔽 Select {query.data} quality 🔽"""
    , parse_mode="Markdown", reply_markup = reply_markup
  )




def beauty(num):
  return "{:,}".format(num)



def start(update, context):
  username = update.message.from_user.first_name
  update.message.reply_text(f"Halo *{username}*, silahkan paste url untuk mendapatkan tanggapan.", parse_mode="Markdown")




def main(): 
  updater = Updater(BOT_TOKEN)
  dp = updater.dispatcher
  
  dp.add_handler(CommandHandler("start",start))
  dp.add_handler(MessageHandler(Filters.regex('(youtu|youtube)') & ~Filters.command, youtube))
  dp.add_handler(CallbackQueryHandler(youtube_handler))
 
  
  updater.start_polling()
  
  updater.idle()
  

if (__name__) == "__main__":
  main()