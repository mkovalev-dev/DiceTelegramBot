import time
import sqlite3
import telebot

bot = telebot.TeleBot("5575562113:AAEBdNcwZZ_qDXC2iUvxEsvl04jvJNpHFkQ")


def get_user(username, chat_id):
    conn = sqlite3.connect("db")
    data = conn.execute(
        f"SELECT username, rating FROM users WHERE username = '{username}' AND chat_id='{chat_id}'"
    ).fetchone()
    conn.close()
    return data


def create_user(username, chat_id):
    conn = sqlite3.connect("db")
    conn.execute(
        f"INSERT INTO USERS (USERNAME,RATING,MONEY, CHAT_ID) \
            VALUES ('{username}', 0, 20000,'{chat_id}')"
    )
    conn.commit()
    conn.close()


def update_raiting(username, chat_id, value):
    conn = sqlite3.connect("db")
    conn.execute(
        f"UPDATE users SET rating = '{value}' WHERE username = '{username}' AND chat_id='{chat_id}'"
    )
    conn.commit()
    conn.close()


@bot.message_handler(commands=["start"])
def start_message(message):
    user = get_user(message.from_user.username, message.chat.id)
    if user is None:
        create_user(message.from_user.username, message.chat.id)
        bot.send_message(message.chat.id, "Поздравляю, ты в игре!")
    else:
        bot.send_message(message.chat.id, "Ты уже в игре!")


@bot.message_handler(content_types=["dice"])
def dice(message):
    user = get_user(message.from_user.username, message.chat.id)
    if user:
        rating = message.dice.value + user[1]
        update_raiting(message.from_user.username, message.chat.id, rating)
        bot.send_message(message.chat.id, f"Количество очков @{user[0]} {rating}")
    else:
        bot.send_message(
            message.chat.id, "Ты еще не в игре! Чтобы начать игру выполни /start"
        )


# Запускаем бота
bot.polling(none_stop=True, interval=0)
