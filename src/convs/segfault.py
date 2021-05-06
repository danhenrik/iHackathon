from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters
from mail import send_mail
from actions import restart

""" Módulo da conversa do Segfault """

# Declaração de constantes de estado usadas pela conversa
TYPING_SEGFAULT = map(chr, range(1))

# Função que introduz a conversa do segfault e atualiza o estado para esperar a entrada da reclamação
def getSegfault(update, context):
    text = ('Que pena que você tenha uma reclamação\n'
            'Mas que bom que você está me contando!\n'
            'Qual é o problema? Não se preocupe, essa denúncia é anônima')

    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return TYPING_SEGFAULT

# Função que recebe pelo update o texto do segfault e o envia por email, encerrando a conversa
def sendSegfault(update, context):
    segfault = update.message.text
    send_mail('Segfault', segfault)
    text = ('Muito obrigado pela sua submissão!\n'
            'Sua reclamação já foi enviada para o nosso email!')

    update.message.reply_text(text=text, reply_markup = ReplyKeyboardRemove())

    return ConversationHandler.END

def saysorry(update,context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Essa função infelizmente ainda não está funcionando, estamos no aguardo do email oficial do iSpirito para tal. :("
    )

# Conversartion Handler: gerencia a o início, os estados e o fim da conversa
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text('Segfault'), saysorry)],
    # entry_points=[MessageHandler(Filters.text('Segfault'), getSegfault)],
    
    states={
        TYPING_SEGFAULT: [MessageHandler(~Filters.text(
            ['Cancelar']) & Filters.text, sendSegfault)]
    },
    fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
)