from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters
from mail import send_mail
from actions import restart

TYPING_SEGFAULT = map(chr, range(1))

def getSegfault(update, context):
    text = ('Que pena que você tenha uma reclamação\n'
            'Mas que bom que você está me contando!\n'
            'Qual é o problema? Não se preocupe, essa denúncia é anônima')

    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return TYPING_SEGFAULT


def sendSegfault(update, context):
    segfault = update.message.text
    send_mail('Segfault', segfault)
    text = ('Muito obrigado pela sua submissão!\n'
            'Sua reclamação já foi enviada para o nosso email!')

    update.message.reply_text(text=text, reply_markup = ReplyKeyboardRemove())

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text('Segfault'), getSegfault)],
    states={
        TYPING_SEGFAULT: [MessageHandler(~Filters.text(
            ['Cancelar']) & Filters.text, sendSegfault)]
    },
    fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
)