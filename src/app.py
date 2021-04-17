from typing import ContextManager
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackQueryHandler, CallbackContext
from env import TOKEN
from db import reminders, birthdays
from scheduleCheckBD import checkBirthday
from scheduleCheckRM import checkReminder
import schedule
import time

FAQ, DIRETORIAS, TECNOLOGIAS, SELECTING_ACTION, SELECTING_THEME, SELECTING_QUESTION, STOPPING, END = map(
    chr, range(8))


def say(update, context, message):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message
    )


def lembrete(update, context):
    response_message = "Só me fala o dia e a hora"

    # TODO: Salvar o lembrete no banco
    say(update, context, response_message)


def sugestao(update, context):
    response_message = "Qualquer coisa"

    # TODO: Pergunta qual a sugestão, depois pra quem e por fim manda a sugestão
    say(update, context, response_message)


def unknown(update, context):
    response_message = "Como é que é?"
    say(update, context, response_message)


def denunciaAnonima(update, context):
    response_message = "Manda a braba"
    say(update, context, response_message)

    # TODO: Pega a proxima mensagem que te mandarem e manda ela pro RH


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
        chat_id=update.effective_chat.id, text="Para de me usar, ainda estou em desenvolvimento"
    )

# Funções teste conversa


def start(update, context):
    reply_keyboard = [
        ['FAQ', 'Sugestão'],
        ['Xapralá']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = ("Olá! Com o que posso ajudar?")
    update.message.reply_text(text=text, reply_markup=markup)

    return SELECTING_ACTION


def selectTheme(update, context):
    text = "Sobre qual assunto é sua dúvida?"
    reply_keyboard = [
        ['Diretorias', 'Tecnologias', 'Processo Seletivo'],
        ['Xapralá']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)


def selectQuestion(update, context):
    reply_keyboard = [
        ['Pergunta 1', 'Pergunta 2'],
        ['Pergunta 3', 'Outra']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = "Perguntas comuns desse tema:"
    update.message.reply_text(text=text, reply_markup=markup)


def showAnswer(update, context):
    update.message.reply_text(text="Resposta")


def stopNested(update, context):
    return STOPPING


def stop(update, context):
    return END


def main():
    updater = Updater(token=TOKEN)

    schedule.every(1).day.at("11:30").do(checkBirthday())
    schedule.every(1).minutes.do(checkReminder())

    dispatcher = updater.dispatcher

    faq_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('FAQ'), selectTheme)],
        states={
            SELECTING_THEME: [MessageHandler(Filters.text, selectQuestion)],
            SELECTING_QUESTION: [MessageHandler(Filters.text, showAnswer)]
        },
        fallbacks=[CommandHandler('stop', stopNested)]
    )

    """ sugestao_conv = ConversationHandler(
      entry_points=[CallbackQueryHandler(getAlvo, patten=f'^{SUGESTAO}$')],
      state={
        TYPING: [CallbackQueryHandler()]
      }
    ) """

    selectionHandlers = [
        faq_conv,
        """ sugestao_conv,
      lembrete_conv,
      justificativa_conv,
      segfault_conv """
    ]

    starting_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_ACTION: selectionHandlers,
            STOPPING: [CommandHandler('start', start)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    # Quando usar o comando com a palavra chave (primeiro parametro) da trigger na função (segundo parametro)
    dispatcher.add_handler(starting_conv)
    dispatcher.add_handler(CommandHandler("mybirthday", setBirthday))
    dispatcher.add_handler(CommandHandler("lembrete", lembrete))
    dispatcher.add_handler(CommandHandler("sugestao", sugestao))
    dispatcher.add_handler(CommandHandler("181", denunciaAnonima))
    dispatcher.add_handler(CommandHandler("teste", teste))
    # Quando chegar uma menssagem e ela n for um comando da trigger na função segundo parâmetro
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command), copia))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    while(True):
        schedule.run_pending()
        time.sleep(1)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    print("press CTRL + C to cancel.")
    main()
