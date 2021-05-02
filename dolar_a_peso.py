from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_markup=buttons)

def convert(update, context):

    access_key = os.getenv('access_key')
    r = requests.get(f'http://api.currencylayer.com/live?access_key={access_key}&source=USD&currencies=CLP').json()

    dolarInput = update.message.text
    
    convertion_value = r.get("quotes").get("USDCLP")

    result = str(int(float(dolarInput) * float(convertion_value)))

    length = len(result)

    # only work with in range 1.000 : 999.999
    formated_result = f'${result[:length - 3]}.{result[-3:]}'

    context.bot.send_message(chat_id=update.effective_chat.id, text=formated_result)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    
    token = os.getenv('token')
    port = os.getenv('PORT', 80)

    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher

    buttons = ReplyKeyboardMarkup(keyboard=[["52.48", "47.23"], ["104.96", "99.13"]])

    start_handler = CommandHandler('start', start)
    convert_handler = MessageHandler(Filters.text & (~Filters.command), convert)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(convert_handler)
    dispatcher.add_error_handler(error)
    
    # updater.start_polling() # testing
    updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
    updater.bot.setWebhook('https://dolar-a-peso.herokuapp.com/' + token)

    updater.idle()

if __name__ == '__main__':
    main()