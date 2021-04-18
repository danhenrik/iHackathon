from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from mail import send_mail
from actions import restart

(
    TYPING_TARGET,
    TARGET,
    TYPING_SUGGESTION) = map(chr, range(3))

def getTarget(update, context):
    text = ('Que ótimo! Adorarei ouvir sua sugestão!\n'
            'Qual será o alvo da sua sugestão?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return TYPING_TARGET

def getSuggestion(update, context):
    target = update.message.text
    context.user_data[TARGET] = target
    text = ('Perfeito!\n'
            'E qual será a sua sugestão?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return TYPING_SUGGESTION


def sendSuggestion(update, context):

    suggestion = (f'Alvo da sugestão: {context.user_data.get(TARGET)}\n'
                  f'Sugestão: {update.message.text}')

    send_mail('Sugestão', suggestion)

    update.message.reply_text(
        text='Sua sugestão será enviada diretamente para nosso email!')
    update.message.reply_text(text='Muito obrigado!', reply_markup = ReplyKeyboardRemove())
    
    del context.user_data[TARGET]

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Sugestão']), getTarget)],
    states={
        TYPING_TARGET: [MessageHandler(~Filters.text(['Cancelar']) & Filters.text, getSuggestion)],
        TYPING_SUGGESTION: [MessageHandler(
            ~Filters.text(['Cancelar']) & Filters.text, sendSuggestion)]
    },
    fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
)