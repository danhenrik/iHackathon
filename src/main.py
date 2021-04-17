from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackQueryHandler
from config.config import TOKEN
import json

FAQ, DIRETORIAS, TECNOLOGIAS, SELECTING_ACTION, SELECTING_THEME, SELECTING_QUESTION = map(chr, range(6))

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

def copia(update, context):
    response_message = update.message.text

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message+"!"
    )

#Funções teste conversa

def start(update, context):
  buttons = [
    InlineKeyboardButton(text='Diretorias', callback_data=str(DIRETORIAS)),
    InlineKeyboardButton(text='Tecnologias', callback_data=str(TECNOLOGIAS))
  ]
  keyboard = InlineKeyboardMarkup(buttons)
  update.message.reply_text(reply_markup = keyboard)

def selectTheme(update, context):
  buttons = [
    InlineKeyboardButton(text='Diretorias', callback_data=str(DIRETORIAS)),
    InlineKeyboardButton(text='Tecnologias', callback_data=str(TECNOLOGIAS))
  ]
  keyboard = InlineKeyboardMarkup(buttons)
  update.message.reply_text(reply_markup = keyboard)

def selectQuestion(update, context):
  update.message.reply_text(text="Perguntas:")

def showAnswer(update, context):
  update.message.reply_text(text="Resposta")



def main():
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher

    faq_conv = ConversationHandler(
      entry_points=[CallbackQueryHandler(selectTheme, pattern=f'^{FAQ}$')],
      states={
        SELECTING_THEME: [CallbackQueryHandler(selectQuestion, pattern=f'^{DIRETORIAS}$|^{TECNOLOGIAS}$')],
        SELECTING_QUESTION: [MessageHandler(Filters.regex('^[0-9]+$') ^ Filters.regex('Outra'), showAnswer)]
      },
      #fallbacks=[CommandHandler('stop', stopNested)]
      fallbacks=[]
    )

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
        SELECTING_ACTION: selectionHandlers
      },
      fallbacks=[]
    )

    # Quando usar o comando com a palavra chave (primeiro parametro) da trigger na função (segundo parametro)
    dispatcher.add_handler(starting_conv)
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
