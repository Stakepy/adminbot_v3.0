from telegram import ChatPermissions
from telegram.ext import Updater, MessageHandler, Filters
from datetime import datetime, timedelta

TOKEN = '5856175367:AAEjtX5_wjkt8NhuwBnUhBediloa14X5U6A'
LIMIT = 8 # количество сообщений в течение временного окна
TIME_WINDOW = 10 # временное окно в секундах
BAN_TIME = 10 # время бана в минутах

users = {}

def handle_message(update, context):
    user_id = update.message.from_user.id
    now = datetime.now()
    if user_id not in users:
        users[user_id] = [now]
    else:
        users[user_id].append(now)
        recent_messages = [msg_time for msg_time in users[user_id] if now - msg_time < timedelta(seconds=TIME_WINDOW)]
        users[user_id] = recent_messages
        if len(recent_messages) > LIMIT:
            context.bot.restrict_chat_member(
                update.message.chat.id,
                user_id,
                until_date=now + timedelta(minutes=BAN_TIME),
                permissions=ChatPermissions(can_send_messages=False)
            )
            update.message.reply_text(f'Вы заблокированы на {BAN_TIME} минут за спам.')
    # Дополнительная проверка для всех видов документов
    if update.message.document:
        users[user_id].append(now)
        recent_messages = [msg_time for msg_time in users[user_id] if now - msg_time < timedelta(seconds=TIME_WINDOW)]
        users[user_id] = recent_messages
        if len(recent_messages) > LIMIT:
            context.bot.restrict_chat_member(
                update.message.chat.id,
                user_id,
                until_date=now + timedelta(minutes=BAN_TIME),
                permissions=ChatPermissions(can_send_messages=False)
            )
            update.message.reply_text(f'Вы заблокированы на {BAN_TIME} минут за спам.')

updater = Updater(TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
updater.start_polling()
updater.idle()