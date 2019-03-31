#
# Caroline is a telegram chatbot
# Nyhilo 2019-3-30
#

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging
from random import choice

import config

###########
# logging #
###########

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger()

###########
# Globals #
###########
DefaultConfigFile = 'caroline.config'
DefaultDialogFile = 'dialog.json'

Config = config.Config(DefaultConfigFile)
Dialog = config.Config(DefaultDialogFile)

#bot = telegram.Bot(token=Config.get("token"))


#####################
# Utility Functions #
#####################

def getDialog(section, *args):
    dialog = choice(Dialog.get(section))
    if args:
        return dialog.format(*args)
    else:
        return dialog


def authorize(update):
    authorizedRoomIds =  [room["id"] for room in Config.get("chatrooms") if room["name"] == "self"]
    log.info("Authorized room ids are {}".format(authorizedRoomIds))
    return str(update.message.chat_id) in authorizedRoomIds

#####################
# Service Functions #
#####################

def pickKeywords(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="You said Bot!")


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


###########################
# Demo Handlers/Functions #
###########################


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

############
# Handlers #
############

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=getDialog("start_greeting", Config.get("owner")))
    
    room_ids = [room["id"] for room in Config.get("chatrooms")]
    chat_id = str(update.message.chat_id)
    
    if context.args:
        if chat_id in room_ids:
            context.bot.send_message(chat_id=update.message.chat_id, text=getDialog("start_roomNameAlreadySet", Config.get("owner")))
        else:
            roomname = context.args[0]
            rooms = Config.get("chatrooms")
            rooms.append({
                "name": roomname,
                "id": chat_id
                })
            Config.set("chatrooms", rooms)
            context.bot.send_message(chat_id=update.message.chat_id, text=getDialog("start_roomNameSet", roomname))
    else:
        if chat_id in room_ids:
            roomname = [room["name"] for room in Config.get("chatrooms") if room["id"] == chat_id][0]
            context.bot.send_message(chat_id=update.message.chat_id, text=getDialog("start_roomKnowledge", roomname))
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=getDialog("error_roomNotSet"))
            

def resetDialog(update, context):
    if not authorize(update):
        return log.info("This command is unauthorized from this chatroom")

    if context.args:
        filename = context.args[0] + ".json"
        try:
            Dialog.loadConfig(filename)
        except FileNotFoundError:
            context.bot.send_message(chat_id=update.message.chat_id, text="No dialog file {} found. Use /resetDialog to reset to default setting".format(filename))

    else:
        Dialog.loadConfig()

    context.bot.send_message(chat_id=update.message.chat_id, text="Dialog updated to {}".format(Dialog.filename))

    

def listen(update, context):
    msg = update.message.text
    if "bot" in msg.lower():
        pickKeywords(update, context)
    else:
        echo(update, context)


########
# Main #
########

def main():
    updater = Updater(token=Config.get("token"), use_context=True)
    dispatcher = updater.dispatcher

    demoHandlers = [
        CommandHandler('start', start),
        CommandHandler('caps', caps),
        ]

    handlers = [
        CommandHandler('resetdialog', resetDialog),
        MessageHandler(Filters.text, listen),
        ]

    for handler in demoHandlers:
        dispatcher.add_handler(handler)

    for handler in handlers:
        dispatcher.add_handler(handler)


    updater.start_polling()


if __name__ == '__main__':
    main()