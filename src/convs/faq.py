from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from actions import restart
from db import faq

""" Módulo da conversa do FAQ """

# Declaração de constantes de estado usadas pela conversa
(SELECTING_THEME, SELECTING_QUESTION) = map(chr, range(2))

# Função que introduz a conversa do FAQ e atualiza o estado para esperar a entrada do tema desejado
# Envia um teclado para auxiliar na escolha
def selectTheme(update, context):
    text = "Sobre qual assunto é sua dúvida?"

    reply_keyboard = [
        ['Diretorias', 'Tecnologias', 'Outros'],
        ['Cancelar']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return SELECTING_THEME

# Função que recebe o tema no update e atualiza o estado para esperar a escolha da pergunta desejada
# Envia um teclado para auxiliar na escolha
def selectQuestion(update, context):
    tema = update.message.text

    reply_keyboard = []

    for pergunta in faq.find({"tema": tema}):
        reply_keyboard.append([pergunta['enunciado']])

    reply_keyboard.append(['Outra', 'Cancelar'])

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = "Perguntas comuns desse tema:"
    update.message.reply_text(text=text, reply_markup=markup)

    return SELECTING_QUESTION

# Função que recebe a pergunta desejada no update e envia a resposta da pergunta
def showAnswer(update, context):
    enunciado = update.message.text
    
    pergunta = faq.find_one({"enunciado": enunciado})

    text = pergunta['resposta']
    update.message.reply_text(text=text)


# Conversartion Handler: gerencia a o início, os estados e o fim da conversa
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('FAQ'), selectTheme)],
    states={
        SELECTING_THEME: [MessageHandler(Filters.text(['Diretorias', 'Tecnologias', 'Outros']), selectQuestion)],
        SELECTING_QUESTION: [MessageHandler(
            ~Filters.text(['Cancelar']) & Filters.text, showAnswer)]
    },
    fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
)