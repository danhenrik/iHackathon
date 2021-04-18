from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from mail import send_mail
from actions import restart

""" Módulo da conversa de Justificativa """

# Declaração de constantes de estado usadas pela conversa
(
    TYPING_TARGET,
    TARGET,
    TYPING_JUSTIFICATION) = map(chr, range(3))

# Função que introduz a conversa de justificativa e atualiza o estado para esperar a entrada de alvo da justificativa
def getTarget(update, context):
    """
    text = ('Certo. Precisa justificar alguma falta.\n'
            'Exatamente que situação você está justificando?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    """
    return TYPING_TARGET

# Função que recebe o alvo da justificativa no update e atualiza o estado para receber a justificativa
def getJustification(update, context):
    """
    target = update.message.text
    context.user_data[TARGET] = target
    text = ('Perfeito!\n'
            'E qual foi a razão?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    """
    return TYPING_JUSTIFICATION

# Função que recebe a justificativa e a envia por email, encerrando a conversa
def sendJustification(update, context):
    """
    justification = (f'Quem está justificando: {update.message.from_user.first_name}\n'
        f'O que está justificando: {context.user_data.get(TARGET)}\n'
        f'Justificativa: {update.message.text}')

    send_mail('Justificativa', justification)

    update.message.reply_text(
        text='Sua justificativa será enviada diretamente para nosso email!')
    update.message.reply_text(text='Muito obrigado!', reply_markup = ReplyKeyboardRemove())
    
    del context.user_data[TARGET]
    """
    update.message.reply_text(text="Essa função infelizmente ainda não está funcionando, estamos no aguardo do email oficial do iSpirito para tal. :(", reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END

def saysorry(update,context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Essa função infelizmente ainda não está funcionando, estamos no aguardo do email oficial do iSpirito para tal. :("
    )

# Conversartion Handler: gerencia a o início, os estados e o fim da conversa
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['Justificativa']), saysorry)],
    # entry_points=[MessageHandler(Filters.text(['Justificativa']), getTarget)],
    states={
        TYPING_TARGET: [MessageHandler(~Filters.text(['Cancelar']) & Filters.text, getJustification)],
        TYPING_JUSTIFICATION: [MessageHandler(
            ~Filters.text(['Cancelar']) & Filters.text, sendJustification)]
    },
    fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
)