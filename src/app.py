from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from env import TOKEN
from scheduledEvents import checkBirthday, checkReminder
import multiprocessing
from db import reminders, birthdays
from mail import send_mail
from actions import say, start, restart, end, getHelp
from convs import faq, suggestion, justification, segfault
import schedule

(
    SELECTING_ACTION,
    TYPING_TARGET,
    TARGET,
    TYPING_SUGGESTION,
    TYPING_JUSTIFICATION,
    TYPING_SEGFAULT,
    RESTART) = map(chr, range(7))

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

def sched():
    schedule.every().minute.do(checkReminder)
    schedule.every().day.at("10:30").do(checkBirthday)
    while True:
        schedule.run_pending()


def bot():
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher

    selectionHandlers = [
        faq.conv_handler,
        suggestion.conv_handler,
        justification.conv_handler,
        segfault.conv_handler,
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
        fallbacks=[MessageHandler(Filters.text, start)]
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
