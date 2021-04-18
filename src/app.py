import threading
from typing import ContextManager
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler
from env import TOKEN
from scheduledEvents import checkBirthday, checkReminder
import multiprocessing
from db import reminders, birthdays
from mail import send_mail
from actions import say, start, restart, end
from convs import faq, suggestion, justification, segfault
import schedule
import time

(
    SELECTING_ACTION,
    TYPING_TARGET,
    TARGET,
    TYPING_SUGGESTION,
    TYPING_JUSTIFICATION,
    TYPING_SEGFAULT,
    RESTART) = map(chr, range(7))


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
    # Retorna se o bot foi chamado no privado
    return update.message.chat.type == "private"

def month(elem):
    # Essa e a próxima função apenas retornam os campos específicos do dicionário pelos quais eu quero ordenar
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


def birthdayToday(update, context):
    all = checkBirthday()
    if(all):
        if(len(all) == 1):
            response_message = "Hoje temos um aniversariante!!!!!\nParabéns " + \
                all[0]["userName"] + " pelos " + \
                str(all[0]["idade"]) + " aninhos!"
        else:
            response_message = "Hoje temos alguns aniversariantes!!!!!\n"
            for i in all:
                response_message += "Parabéns " + \
                    i["userName"] + " pelos " + str(i["idade"]) + " aninhos!\n"
        say(update, context, "🥳")
        say(update, context, "🥳")
        say(update, context, "🥳")
        say(update, context, response_message)


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


# Função para exibir os comandos disponíveis do bot
def getHelp(update, context):
    response_message = "Olá sou o iSpirito, por enquanto em grupos eu apenas registro e lembro os" + \
        " aniversários de todo mundo, os comandos são os seguintes:\n/mybirthday <DD/MM/AAAA> Para registrar" + \
        " seu aniversário\n/birthdaylist Lista os aniversários registrados\n No privado tenho algumas funcionalidades" + \
        " extras como:\n - Enviar email de justificativa pro RH\n - FAQ, com perguntas frequentes sobre diversos temas" + \
        " pertinentes à empresa\n - Segfault, por meio do bot é possível fazer reclamações 100% anônimas pro RH" + \
        " (espero que ninguem precise usar esse recurso)\n - Suegestões, onde vc pode fazer a sugestão de ideias" + \
        " à empresa, podendo ser direcionado ou com o escopo geral\nPra usar essas funcionalidades basta me chamar" + \
        " no privado com um /start\n Espero ser útil! 👻"
    say(update, context, response_message)


def init(update, context):
    if(not context.user_data.get("initCheck")):
        context.user_data["initCheck"] = True

        def sched():
            # TODO: Reminder com sync com google agenda e afins
            # schedule.every().minute.do(checkReminder)
            schedule.every().day.at("12:30").do(birthdayToday, update, context)
            while True:
                schedule.run_pending()
                time.sleep(1)
        threading.Thread(target=sched).start()


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

    dispatcher.add_handler(starting_conv)
    dispatcher.add_handler(CommandHandler("init", init))
    dispatcher.add_handler(CommandHandler("mybirthday", setBirthday))
    dispatcher.add_handler(CommandHandler("birthdaylist", getBirthdays))
    dispatcher.add_handler(CommandHandler("help", getHelp))

    updater.start_polling()
    updater.idle()


def main():
    multiprocessing.Process(target=bot).start()


if __name__ == "__main__":
    main()
