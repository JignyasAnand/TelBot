from telegram.ext import *
from telegram.update import Update
import Keys as keys
import mainfuncs2 as mfun

def off(update: Update, context: CallbackContext):
    exit(0)

def main():
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("a",mfun.adminfunc))
    dp.add_handler(CommandHandler("start",mfun.start))
    dp.add_handler(CommandHandler("rfile",mfun.send_doc))
    dp.add_handler(CommandHandler("cap",mfun.getcap))
    dp.add_handler(CommandHandler("g", mfun.guest))
    dp.add_handler(CommandHandler("andf", off))
    dp.add_handler(CommandHandler("clear", mfun.clear))
    dp.add_handler(MessageHandler(Filters.text,mfun.handle))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, mfun.doc_downloader))


    dp.add_error_handler(mfun.error)

    updater.start_polling()
    updater.idle()

main()

