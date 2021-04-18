from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

(SELECTING_ACTION, RESTART) = map(chr, range(2))

def say(update, context, message):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message
    )

def start(update, context):
    if update.message.chat.type != 'private':
        text = 'Desculpe, mas só podemos ter uma conversa no privado! ^-^'
        update.message.reply_text(text=text)
        return ConversationHandler.END

    reply_keyboard = [
        ['FAQ', 'Sugestão'],
        ['Segfault', 'Justificativa'],
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

def restart(update, context):
    context.user_data[RESTART] = True
    start(update, context)
    return ConversationHandler.END

def end(update, context):
    say(update, context, 'Tudo bem! Até a próxima! Qualquer coisa é só chamar! ^-^')
    return ConversationHandler.END

def getHelp(update, context):
    if(update.message.chat.type == "group"):
        response_message = "Commands:\n/mybirthday\n/birthdaylist\n/FAQ"
    else:
        response_message = "Commands:\n\n/birthdaylist"
    say(update, context, response_message)