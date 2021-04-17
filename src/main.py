from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackQueryHandler, CallbackContext
from config.env import TOKEN
from config.db import reminders,birthdays
import json

FAQ, DIRETORIAS, TECNOLOGIAS, SELECTING_ACTION, SELECTING_THEME, SELECTING_QUESTION, STOPPING, END = map(chr, range(8))

def Lembrete(update, context):
    response_message = "Só me fala o dia e a hora"

    # TODO: Salvar o lembrete no banco
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def Sugestao(update, context):
    response_message = "Qualquer coisa"

    # TODO: Pergunta qual a sugestão, depois pra quem e por fim manda a sugestão
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def unknown(update, context):
    response_message = "Como é que é?"

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def DenunciaAnonima(update, context):
    response_message = "Manda a braba"

    # TODO: Pega a proxima mensagem que te mandarem e manda ela pro RH
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def teste(update, context):
    response_message = "Testado"
    print("context> ", context, "\n\n")
    print("context.bot> ", context.bot, "\n\n")
    print("update> ", update, "\n\n")

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )
def setBirthday(update, context):
  userID = update.message.from_user.id
  checkdb = birthdays.find_one({"userID":userID})
  print(checkdb)
  """
  newBirthday = {
        "author_id": update.message.from_user.id ,
        "author_name": update.message.from_user.first_name ,
        "text": update.message.text, 
    }
    birthdays.insert_one(newReminder)
    """
def copia(update, context):
    response_message = update.message.text
    print("update> ", update, "\n\n")
    print(update.message.from_user.id)
    print(update.message.text)

    newReminder = {
        "author_id": update.message.from_user.id ,
        "author_name": update.message.from_user.first_name ,
        "text": update.message.text, 
    }
    birthdays.insert_one(newReminder)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message+"!"
    )

#Funções teste conversa

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
    ['Diretorias', 'Tecnologias', 'Outros'],
    ['Cancelar']
  ]
  markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
  update.message.reply_text(text=text, reply_markup = markup)

  return SELECTING_THEME

def selectQuestion(update, context):
  reply_keyboard = [
    ['Pergunta 1', 'Pergunta 2'],
    ['Pergunta 3', 'Outra'],
    ['Cancelar']
  ]
  markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
  text="Perguntas comuns desse tema:"
  update.message.reply_text(text=text, reply_markup = markup)

  return SELECTING_QUESTION

def showAnswer(update, context):
  pergunta = update.message.text
  if pergunta == 'Cancelar':
    return STOPPING
  
  text = f'Resposta da pergunta: {pergunta}'
  update.message.reply_text(text=text)

def stopNested(update, context):
  return STOPPING

def stop(update, context):
  return END



def main():
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher

    faq_conv = ConversationHandler(
      entry_points=[MessageHandler(Filters.regex('FAQ'), selectTheme)],
      states={
        SELECTING_THEME: [MessageHandler(Filters.text(['Diretorias', 'Tecnologias', 'Outros']), selectQuestion)],
        SELECTING_QUESTION: [MessageHandler(Filters.text, showAnswer)],
        STOPPING: [CommandHandler('start', start)]
      },
      fallbacks=[MessageHandler(Filters.text('Cancelar'), stopNested)]
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
