from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests
import os
import logging
import locale

locale.setlocale(locale.LC_ALL, '')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
buttons = ReplyKeyboardMarkup(keyboard=[["52.48", "47.23"], ["104.96", "99.13"]])

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! envía un valor en Pesos Chilenos y lo Convertiré en Dólares", reply_markup=buttons)

def convert(update, context):

    access_key = os.getenv('access_key')
    r = requests.get(f'http://api.currencylayer.com/live?access_key={access_key}&source=USD&currencies=CLP').json()

    dolarInput = update.message.text
    
    convertion_value = r.get("quotes").get("USDCLP")

    result = int(float(dolarInput) * float(convertion_value))

    formated_result = locale.currency(result)

    context.bot.send_message(chat_id=update.effective_chat.id, text=formated_result)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    
    token = os.getenv('token')
    port = int(os.getenv('PORT', 5000))

    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    convert_handler = MessageHandler(Filters.text & (~Filters.command), convert)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(convert_handler)

    dispatcher.add_error_handler(error)
    
    updater.start_webhook(listen="0.0.0.0", 
                            port=port, 
                            url_path=token, 
                            webhook_url='https://dolar-a-peso.herokuapp.com/' + token)

    updater.idle()

if __name__ == '__main__':
    main()