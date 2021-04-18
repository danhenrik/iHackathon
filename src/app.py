from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackQueryHandler, CallbackContext
from env import TOKEN
from scheduledEvents import checkBirthday, checkReminder
import multiprocessing
from db import reminders, birthdays, faq
from mail import send_mail
import schedule

(
    SELECTING_ACTION,
    SELECTING_THEME,
    SELECTING_QUESTION,
    TYPING_TARGET,
    TYPING_SUGGESTION,
    TYPING_SEGFAULT,
    RESTART) = map(chr, range(7))


def say(update, context, message):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message
    )


def Lembrete(update, context):
    response_message = "Só me fala o dia e a hora"

    # TODO: Salvar o lembrete no banco
    say(update, context, response_message)


def teste(update, context):
    response_message = "Testado"
    print("context> ", context, "\n\n")
    print("context.bot> ", context.bot, "\n\n")
    print("update> ", update, "\n\n")

    say(update, context, response_message)


def validateDate(context):
    if (not len(context.args) == 0):
        date_string = context.args[0]
        dateArr = date_string.split("/")
        date = "".join(dateArr)
        if(len(date) == 8 and date.isdigit()):
            return True
    else:
        return False


def checkPrivate(update):
    return update.message.chat.type == "private"


def setBirthday(update, context):
    userID = update.message.from_user.id
    checkdb = birthdays.count_documents({"userID": userID})
    print(update)
    if(checkPrivate(update)):
        say(update, context, "Essa funcionalidade é exclusiva para grupos")
    else:
        if(validateDate(context)):
            birthday = context.args[0].split("/")
            dayMonth = birthday[0] + birthday[1]
            year = birthday[2]
            name = str(update.message.from_user.first_name)
            if update.message.from_user.last_name:
                name = name + " " + update.message.from_user.last_name
            newBirthday = {
                "userID": update.message.from_user.id,
                "userName": name,
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


def month(elem):
    return elem["month"]


def day(elem):
    return elem["day"]


def newMonth(month):
    if(month == 1):
        return "Janeiro"
    if(month == 2):
        return "Fevereiro"
    if(month == 3):
        return "Março"
    if(month == 4):
        return "Abril"
    if(month == 5):
        return "Maio"
    if(month == 6):
        return "Junho"
    if(month == 7):
        return "Julho"
    if(month == 8):
        return "Agosto"
    if(month == 9):
        return "Setembro"
    if(month == 10):
        return "Outubro"
    if(month == 11):
        return "Novembro"
    if(month == 12):
        return "Dezembro"


def getBirthdays(update, context):
    if(checkPrivate(update)):
        say(update, context, "Essa funcionalidade é exclusiva para grupos")
    else:
        response_message = "Aniversariantes:\n"
        all = birthdays.find()
        arr = []
        for i in all:
            arr.append(i)
            i["month"] = int(i["dayMonth"][2] + i["dayMonth"][3])
            i["day"] = int(i["dayMonth"][0] + i["dayMonth"][1])
        arr.sort(key=day)
        arr.sort(key=month)
        prevmonth = 0
        print(prevmonth)

        for j in arr:
            print(j["month"])
            if(j["month"] != prevmonth):
                response_message += newMonth(j["month"])+":\n"
            prevmonth == j["month"]
            print(j)
            response_message += str(j["day"]) + " - " + j["userName"] + "\n"
        say(update, context, response_message)


# Funções teste conversa
def start(update, context):
    if update.message.chat.type != 'private':
        text = 'Desculpe, mas só podemos ter uma conversa no privado! ^-^'
        update.message.reply_text(text=text)
        return ConversationHandler.END

    reply_keyboard = [
        ['FAQ', 'Sugestão', 'Segfault'],
        ['Xapralá']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    if not context.user_data.get(RESTART):
        intro = ('Olá!\nEu sou o iSpirito.\n'
                 'Sou seu assistente pessoal da iJunior!')
        update.message.reply_text(text=intro)

    context.user_data[RESTART] = False
    text = 'Com o que posso ajudar?'
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


def getHelp(update, context):
    if(update.message.chat.type == "group"):
        response_message = "Commands:\n/mybirthday\n/birthdaylist\n/FAQ"
    else:
        response_message = "Commands:\n\n/birthdaylist"
    say(update, context, response_message)


def getSuggestion(update, context):
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
    text = ('Que pena que você tenha uma reclamação\n'
            'Mas que bom que você está nos contando!\n'
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

    update.message.reply_text(text=text)


def restart(update, context):
    context.user_data[RESTART] = True
    start(update, context)
    return ConversationHandler.END


def end(update, context):
    say(update, context, 'Tudo bem! Até a próxima! Qualquer coisa é só chamar! ^-^')
    return ConversationHandler.END


def sched():
    schedule.every().minute.do(checkReminder)
    schedule.every().day.at("10:30").do(checkBirthday)
    while True:
        schedule.run_pending()


def bot():
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher

    faq_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('FAQ'), selectTheme)],
        states={
            SELECTING_THEME: [MessageHandler(Filters.text(['Diretorias', 'Tecnologias', 'Outros']), selectQuestion)],
            SELECTING_QUESTION: [MessageHandler(
                ~Filters.text(['Cancelar']) & Filters.text, showAnswer)]
        },
        fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
    )

    sugestao_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.text(['Sugestão']), getTarget)],
        states={
            TYPING_TARGET: [MessageHandler(~Filters.text(['Cancelar']) & Filters.text, getSuggestion)],
            TYPING_SUGGESTION: [MessageHandler(
                ~Filters.text(['Cancelar']) & Filters.text, sendSuggestion)]
        },
        fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
    )

    segfault_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.text('Segfault'), getSegfault)],
        states={
            TYPING_SEGFAULT: [MessageHandler(~Filters.text(
                ['Cancelar']) & Filters.text, sendSegfault)]
        },
        fallbacks=[MessageHandler(Filters.text(['Cancelar']), restart)]
    )

    selectionHandlers = [
        faq_conv,
        sugestao_conv,
        segfault_conv,
        MessageHandler(Filters.text(['Xapralá']), end)
    ]

    starting_conv = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(Filters.text & (
                ~Filters.command), start)
        ],
        states={
            SELECTING_ACTION: selectionHandlers
        },
        fallbacks=[]
    )

    # Quando usar o comando com a palavra chave (primeiro parametro) da trigger na função (segundo parametro)
    dispatcher.add_handler(starting_conv)
    dispatcher.add_handler(CommandHandler("mybirthday", setBirthday))
    dispatcher.add_handler(CommandHandler("birthdaylist", getBirthdays))
    dispatcher.add_handler(CommandHandler("lembrete", Lembrete))
    dispatcher.add_handler(CommandHandler("help", getHelp))
    dispatcher.add_handler(CommandHandler("teste", teste))
    # Quando chegar uma menssagem e ela n for um comando da trigger na função segundo parâmetro

    updater.start_polling()
    updater.idle()


def main():
    scheduleProcess = multiprocessing.Process(target=sched)
    botProcess = multiprocessing.Process(target=bot)
    scheduleProcess.start()
    botProcess.start()


if __name__ == "__main__":
    print("press CTRL + C to cancel.")
    main()
