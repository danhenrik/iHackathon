from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from mail import send_mail
from actions import restart

(
    TYPING_TARGET,
    TARGET,
    TYPING_JUSTIFICATION) = map(chr, range(3))

def getTarget(update, context):
    text = ('Certo. Precisa justificar alguma falta.\n'
            'Exatamente que situação você está justificando?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return TYPING_TARGET

def getJustification(update, context):
    target = update.message.text
    context.user_data[TARGET] = target
    text = ('Perfeito!\n'
            'E qual foi a razão?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return TYPING_JUSTIFICATION


def sendJustification(update, context):

    justification = (f'Quem está justificando: {update.message.from_user.first_name}\n'
        f'O que está justificando: {context.user_data.get(TARGET)}\n'
        f'Justificativa: {update.message.text}')

    send_mail('Justificativa', justification)

    update.message.reply_text(
        text='Sua justificativa será enviada diretamente para nosso email!')
    update.message.reply_text(text='Muito obrigado!', reply_markup = ReplyKeyboardRemove())
    
    del context.user_data[TARGET]

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Justificativa']), getTarget)],
    states={
        TYPING_TARGET: [MessageHandler(~Filters.text(['Cancelar']) & Filters.text, getJustification)],
        TYPING_JUSTIFICATION: [MessageHandler(
            ~Filters.text(['Cancelar']) & Filters.text, sendJustification)]
    },
    fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
)