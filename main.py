from tinydb import TinyDB 
from telegram.ext import Updater,MessageHandler,Filters,CallbackContext,CommandHandler,CallbackQueryHandler
from telegram import Update, ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,InputMediaPhoto
from tinydb.database import Document
import telegram
import json
import db 


TOKEN = '5792178472:AAGJ9ZoAwfDiTiOGUagi9H0txEXOlfP3RQc'
updater = Updater(TOKEN)

def start(update:Update, context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id 
    inlineKeyboard = InlineKeyboardButton('INLINE',callback_data='data 123')
    reply_markup = InlineKeyboardMarkup([[inlineKeyboard]])
    update.message.reply_text(text='Phone',reply_markup=reply_markup)

def main(update:Update,context:CallbackContext):
    bot = context.bot
    chat_id = update.channel_post.chat.id
    photo = update.channel_post.photo[-1].file_id
    caption = update.channel_post.caption
    db.update_db(photo, caption)

def send_img(update:Update, context:CallbackContext):
    bot = context.bot
    text = update.callback_query.message.text
    chat_id = update.callback_query.message.chat.id 
    all_data=db.all_db()
    idx=db.idx_count()
    if len(all_data)==idx:
        db.update_count(-1)
        idx=db.idx_count()

    inlineKeyboard = InlineKeyboardButton('⏭',callback_data='next')
    reply_markup = InlineKeyboardMarkup([[inlineKeyboard]])
    bot.sendPhoto(chat_id,all_data[idx]['photo'],all_data[idx]['caption'],reply_markup=reply_markup)


def send_photo(update:Update, context:CallbackContext):
    bot = context.bot
    query = update.callback_query
    inlineKeyboard = InlineKeyboardButton('⏭',callback_data='next')
    reply_markup = InlineKeyboardMarkup([[inlineKeyboard]])
    all_data=db.all_db()
    idx=db.idx_count()
    db.update_count(idx)
    idx=db.idx_count()
    if len(all_data)==idx:
        db.update_count(-1)
        idx=db.idx_count()
    query.edit_message_media(media=InputMediaPhoto(all_data[idx]['photo'],all_data[idx]['caption']), reply_markup=reply_markup)



updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(MessageHandler(Filters.all,main, channel_post_updates=True))
updater.dispatcher.add_handler(CallbackQueryHandler(send_img,pattern='data 123'))
updater.dispatcher.add_handler(CallbackQueryHandler(send_photo,pattern='next'))


updater.start_polling()
updater.idle()