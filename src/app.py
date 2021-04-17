from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackQueryHandler, CallbackContext
from env import TOKEN
from scheduledEvents import checkBirthday, checkReminder
import time

import schedule
from db import reminders, birthdays, faq
from mail import send_mail
import json

(
    SELECTING_ACTION,
    SELECTING_THEME,
    SELECTING_QUESTION,
    STOPPING,
    END,
    TYPING_TARGET,
    TYPING_SUGGESTION,
    TYPING_SEGFAULT) = map(chr, range(8))


def say(update, context, message):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message
    )


def Lembrete(update, context):
    response_message = "Só me fala o dia e a hora"

    # TODO: Salvar o lembrete no banco
    say(update, context, response_message)


def Sugestao(update, context):
    response_message = "Qualquer coisa"

    # TODO: Pergunta qual a sugestão, depois pra quem e por fim manda a sugestão
    say(update, context, response_message)


def unknown(update, context):
    response_message = "Como é que é?"
    say(update, context, response_message)


def DenunciaAnonima(update, context):
    response_message = "Manda a braba"

    # TODO: Pega a proxima mensagem que te mandarem e manda ela pro RH
    say(update, context, response_message)


def teste(update, context):
    response_message = "Testado"
    print("context> ", context, "\n\n")
    print("context.bot> ", context.bot, "\n\n")
    print("update> ", update, "\n\n")

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def validateDate(context):
    if (not len(context.args) == 0):
        date_string = context.args[0]
        dateArr = date_string.split("/")
        date = "".join(dateArr)
        if(len(date) == 8 and date.isdigit()):
            return True
    else:
        return False


def setBirthday(update, context):
    userID = update.message.from_user.id
    checkdb = birthdays.count_documents({"userID": userID})
    print(update)
    if(validateDate(context)):
        birthday = context.args[0].split("/")
        dayMonth = birthday[0] + birthday[1]
        year = birthday[2]
        newBirthday = {
            "userID": update.message.from_user.id,
            "userName": update.message.from_user.first_name,
            "dayMonth": dayMonth,
            "year": year
        }
        if(checkdb == 0):
            birthdays.insert_one(newBirthday)
            say(update, context, "Seu aniversário foi registrado!")
        else:
            birthdays.replace_one(
                {"userID": update.message.from_user.id}, newBirthday)
            say(update, context, "Seu aniversário foi atualizado!")

    else:
        say(update, context, "Por favor insira sua data de aniversário no seguinte formato:'/mybirthday DD/MM/YYYY'")


def copia(update, context):
    response_message = update.message.text
    print("update> ", update, "\n\n")
    print(update.message.from_user.id)
    print(update.message.text)

    newReminder = {
        "author_id": update.message.from_user.id,
        "author_name": update.message.from_user.first_name,
        "text": update.message.text,
    }
    # birthdays.insert_one(newReminder)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message+"!"
    )

# Funções teste conversa


def start(update, context):
    if update.message.chat.type != 'private':
      text='Desculpe, mas só podemos ter uma conversa no privado! ^^'
      update.message.reply_text(text=text)
      return None

    reply_keyboard = [
        ['FAQ', 'Sugestão', 'Segfault'],
        ['Xapralá']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = ('Olá! Eu sou o iSpirito.\n'
            'Sou seu assistente pessoal da iJunior!\n'
            'Com o que posso ajudar?')
    update.message.reply_text(text=text, reply_markup=markup)

    return SELECTING_ACTION


def selectTheme(update, context):
    text = "Sobre qual assunto é sua dúvida?"

    reply_keyboard = [
        ['Diretorias', 'Tecnologias', 'Outros'],
        ['Cancelar']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return SELECTING_THEME


def selectQuestion(update, context):
    tema = update.message.text

    if tema == 'Cancelar':
        start(update, context)
        return None

    reply_keyboard = []

    for pergunta in faq.find({"tema": tema}):
        reply_keyboard.append([pergunta['enunciado']])

    reply_keyboard.append(['Outra', 'Cancelar'])

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = "Perguntas comuns desse tema:"
    update.message.reply_text(text=text, reply_markup=markup)

    return SELECTING_QUESTION


def showAnswer(update, context):
    enunciado = update.message.text
    if enunciado == 'Cancelar':
        start(update, context)
        return None

    pergunta = faq.find_one({"enunciado": enunciado})

    text = pergunta['resposta']
    update.message.reply_text(text=text)


def getTarget(update, context):
    text = ('Que ótimo! Adorarei ouvir sua sugestão!\n'
            'Qual será o alvo da sua sugestão?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return TYPING_TARGET


def getSuggestion(update, context):
    alvo = update.message.text
    if alvo == 'Cancelar':
        start(update, context)
        return None

    text = ('Perfeito!\n'
            'E qual será a sua sugestão?')
    reply_keyboard = [['Cancelar']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)

    return TYPING_SUGGESTION


def sendSuggestion(update, context):

    suggestion = update.message.text

    send_mail('Sugestão', suggestion)

    update.message.reply_text(
        text='Sua sugestão será enviada diretamente para nosso email!')
    update.message.reply_text(text='Muito obrigado!')
    start(update, context)

def getSegfault(update, context):
    text=('Que pena que você tenha uma reclamação\n'
      'Mas que bom que você está nos contando!\n'
      'Qual é o problema? Não se preocupe, essa denúncia é anônima')
    update.message.reply_text(text = text)

    return TYPING_SEGFAULT

def sendSegfault(update, context):
    segfault = update.message.text
    send_mail('Segfault', segfault)
    text=('Muito obrigado pela sua submissão!\n'
      'Sua reclamação já foi enviada para o nosso email!')

    update.message.reply_text(text=text)

def main():
    updater = Updater(token=TOKEN)

    schedule.every(1).day.at("11:30").do(checkBirthday)
    schedule.every(1).minutes.do(checkReminder)
    #schedule.every(10).seconds.do(testeSched)

    dispatcher = updater.dispatcher

    faq_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('FAQ'), selectTheme)],
        states={
            SELECTING_THEME: [MessageHandler(Filters.text(['Diretorias', 'Tecnologias', 'Outros']), selectQuestion)],
            SELECTING_QUESTION: [MessageHandler(Filters.text, showAnswer)]
        },
        fallbacks=[]
    )

    sugestao_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.text(['Sugestão']), getTarget)],
        states={
            TYPING_TARGET: [MessageHandler(Filters.text, getSuggestion)],
            TYPING_SUGGESTION: [MessageHandler(
                Filters.text, sendSuggestion)]
        },
        fallbacks=[]
    )

    segfault_conv = ConversationHandler(
      entry_points=[MessageHandler(Filters.text('Segfault'), getSegfault)],
      states={
        TYPING_SEGFAULT: [MessageHandler(Filters.text, sendSegfault)]
      },
      fallbacks=[]
    )

    selectionHandlers = [
      faq_conv,
      sugestao_conv,
      segfault_conv
    ]

    starting_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_ACTION: selectionHandlers,
            STOPPING: [CommandHandler('start', start)]
        },
        fallbacks=[]
    )

    # Quando usar o comando com a palavra chave (primeiro parametro) da trigger na função (segundo parametro)
    dispatcher.add_handler(starting_conv)
    dispatcher.add_handler(CommandHandler("mybirthday", setBirthday))
    dispatcher.add_handler(CommandHandler("lembrete", Lembrete))
    dispatcher.add_handler(CommandHandler("sugestao", Sugestao))
    dispatcher.add_handler(CommandHandler("181", DenunciaAnonima))
    dispatcher.add_handler(CommandHandler("teste", teste))
    # Quando chegar uma menssagem e ela n for um comando da trigger na função segundo parâmetro
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command), copia))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    print("press CTRL + C to cancel.")
    main()
