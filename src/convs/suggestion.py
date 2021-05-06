from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from mail import send_mail
from actions import restart

""" Módulo da conversa de Sugestão """

# Declaração de constantes de estado usadas pela conversa
(
    TYPING_TARGET,
    TARGET,
    TYPING_SUGGESTION) = map(chr, range(3))

# Função que introduz a conversa de Sugestão e atualiza o estado para receber o alvo da sugestão
def getTarget(update, context):
    text = ('Que ótimo! Adorarei ouvir sua sugestão!\n'
            'Qual será o alvo da sua sugestão?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    return TYPING_TARGET

# Função que recebe o alvo no update e atualiza o estado para receber a sugestão
def getSuggestion(update, context):
    target = update.message.text
    context.user_data[TARGET] = target
    text = ('Perfeito!\n'
            'E qual será a sua sugestão?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    return TYPING_SUGGESTION

# Função que recebe a sugestão no update e a envia por email, encerrando a conversa
def sendSuggestion(update, context):
    suggestion = (f'Alvo da sugestão: {context.user_data.get(TARGET)}\n'
                   f'Sugestão: {update.message.text}')

    send_mail('Sugestão', suggestion)

    update.message.reply_text(
        text='Sua sugestão será enviada diretamente para nosso email!')
    update.message.reply_text(text='Muito obrigado!', reply_markup = ReplyKeyboardRemove())
    
    del context.user_data[TARGET]
    return ConversationHandler.END

def saysorry(update,context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Essa função infelizmente ainda não está funcionando, estamos no aguardo do email oficial do iSpirito para tal. :("
    )


# Conversartion Handler: gerencia a o início, os estados e o fim da conversa
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Sugestão']), saysorry)],
    # entry_points=[MessageHandler(Filters.text(['Sugestão']), getTarget)],
    states={
        TYPING_TARGET: [MessageHandler(~Filters.text(['Cancelar']) & Filters.text, getSuggestion)],
        TYPING_SUGGESTION: [MessageHandler(
            ~Filters.text(['Cancelar']) & Filters.text, sendSuggestion)]
    },
    fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
)