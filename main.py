import telebot
from telebot import types
import re

TOKEN = '6829707656:AAEgJHF1x6_gAWKZoQBylsbPmFye5VFKqPc'
bot = telebot.TeleBot(TOKEN)

# Функция для отправки сообщения с помощью команды /help
def send_help(message):
    help_text = (
        "📚 Команды бота:\n\n"
        "/start - Начать работу с ботом и узнать доступные функции.\n"
        "/help - Получить помощь по использованию бота.\n"
        "/set_description - Установить новое описание для группы (только в группах).\n"
        "/set_title - Установить новое название для группы (только в группах).\n"
        "/set_media - Управление разрешениями на использование эмодзи, гифок и стикеров.\n"
        "🛠️ Используйте команды, чтобы управлять вашим ботом и группой."
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text="Команда /start", callback_data="start"),
        types.InlineKeyboardButton(text="Команда /set_description", callback_data="set_description"),
        types.InlineKeyboardButton(text="Команда /set_title", callback_data="set_title"),
        types.InlineKeyboardButton(text="Команда /set_media", callback_data="set_media")
    )
    
    bot.send_message(message.chat.id, help_text, reply_markup=markup)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Используйте команду /help для получения списка команд.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):
    send_help(message)

# Обработчик callback_data
@bot.callback_query_handler(func=lambda call: True)
def callback_help(call):
    if call.data in ["start", "set_description", "set_title", "set_media"]:
        send_help(call.message)

# Обработчик команд на изменение описания группы
@bot.message_handler(commands=['set_description'])
def set_description(message):
    if message.chat.type in ['group', 'supergroup']:
        bot.send_message(message.chat.id, "Введите новое описание для группы:")
        bot.register_next_step_handler(message, process_description)
    else:
        bot.send_message(message.chat.id, "Эта команда доступна только в группах.")

def process_description(message):
    description = message.text
    bot.set_chat_description(message.chat.id, description)
    bot.send_message(message.chat.id, "Описание успешно изменено.")

# Обработчик команд на изменение названия группы
@bot.message_handler(commands=['set_title'])
def set_title(message):
    if message.chat.type in ['group', 'supergroup']:
        bot.send_message(message.chat.id, "Введите новое название для группы:")
        bot.register_next_step_handler(message, process_title)
    else:
        bot.send_message(message.chat.id, "Эта команда доступна только в группах.")

def process_title(message):
    title = message.text
    bot.set_chat_title(message.chat.id, title)
    bot.send_message(message.chat.id, "Название успешно изменено.")

# Обработчик команд на изменение разрешений
@bot.message_handler(commands=['set_media'])
def set_media(message):
    if message.chat.type in ['group', 'supergroup']:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        markup.add(
            types.KeyboardButton(text="Разрешить эмодзи"),
            types.KeyboardButton(text="Разрешить гифки"),
            types.KeyboardButton(text="Разрешить стикеры")
        )
        bot.send_message(message.chat.id, "Выберите, что вы хотите изменить:", reply_markup=markup)
        bot.register_next_step_handler(message, process_media)
    else:
        bot.send_message(message.chat.id, "Эта команда доступна только в группах.")

def process_media(message):
    if message.text == "Разрешить эмодзи":
        # Логика для разрешения эмодзи
        bot.send_message(message.chat.id, "Эмодзи разрешены.")
    elif message.text == "Разрешить гифки":
        # Логика для разрешения гифок
        bot.send_message(message.chat.id, "Гифки разрешены.")
    elif message.text == "Разрешить стикеры":
        # Логика для разрешения стикеров
        bot.send_message(message.chat.id, "Стикеры разрешены.")
    else:
        bot.send_message(message.chat.id, "Выберите корректный вариант.")

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    if message.text and re.search(r'[^\w\s,]', message.text):
        bot.reply_to(message, "Ваше сообщение содержит недопустимые символы.")

# Запуск бота
bot.polling(none_stop=True)
