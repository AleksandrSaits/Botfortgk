import telebot
from telebot import types
import datetime

TOKEN = "8755271111:AAHlLq4hW2um6b97kjLdmyO7du6yv0ODTzo"
ADMIN_ID = 8559107011
CHANNEL = "@alex_ai_devel"

bot = telebot.TeleBot(TOKEN)

users = set()
orders = []

# ===== ПРОВЕРКА ПОДПИСКИ =====
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status != "left"
    except:
        return False

# ===== ГЛАВНОЕ МЕНЮ =====
def menu():
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("📦 Заказать бота", callback_data="order")
    btn2 = types.InlineKeyboardButton("💰 Прайс", callback_data="price")
    btn3 = types.InlineKeyboardButton("📂 Портфолио", callback_data="portfolio")
    btn4 = types.InlineKeyboardButton("⭐ Отзывы", callback_data="reviews")
    btn5 = types.InlineKeyboardButton("🎁 Бесплатный бот", callback_data="freebot")
    btn6 = types.InlineKeyboardButton("📞 Связаться", callback_data="contact")

    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    markup.add(btn5)
    markup.add(btn6)

    return markup


# ===== СТАРТ =====
@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.from_user.id)

    if not check_sub(message.from_user.id):

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(
            "Подписаться",
            url="https://t.me/alex_ai_devel"
        )
        markup.add(btn)

        bot.send_message(
            message.chat.id,
            "❌ Для использования бота подпишись на канал",
            reply_markup=markup
        )
        return

    bot.send_message(
        message.chat.id,
        "🤖 *Alex AI Development*\n\n"
        "Я помогу тебе заказать Telegram бота.\n"
        "Выбери действие:",
        parse_mode="Markdown",
        reply_markup=menu()
    )


# ===== ОБРАБОТКА КНОПОК =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "price":

        bot.edit_message_text(
            "💰 *Прайс*\n\n"
            "🤖 Простой бот — 10$\n"
            "⚙️ Средний бот — 25$\n"
            "🚀 Сложный бот — от 50$\n\n"
            "Цена зависит от задачи.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=menu()
        )

    if call.data == "portfolio":

        bot.edit_message_text(
            "📂 *Портфолио*\n\n"
            "✔️ Магазин боты\n"
            "✔️ Автоворонки\n"
            "✔️ Боты с оплатой\n"
            "✔️ Игровые боты\n\n"
            "Больше работ в канале.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=menu()
        )

    if call.data == "reviews":

        bot.edit_message_text(
            "⭐ *Отзывы*\n\n"
            "🗣 'Сделал бота за 1 день'\n"
            "🗣 'Очень качественная работа'\n"
            "🗣 'Бот работает идеально'\n\n"
            "Спасибо всем клиентам ❤️",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=menu()
        )

    if call.data == "freebot":

        bot.edit_message_text(
            "🎁 *Бесплатный бот*\n\n"
            "Подпишись на канал и получи\n"
            "исходник простого Telegram бота.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=menu()
        )

    if call.data == "contact":

        bot.edit_message_text(
            "📞 *Связь*\n\n"
            "Напиши мне в Telegram:\n"
            "@твой_username",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=menu()
        )

    if call.data == "order":

        msg = bot.send_message(
            call.message.chat.id,
            "📝 Опиши какого бота ты хочешь:"
        )

        bot.register_next_step_handler(msg, get_order)


# ===== ПОЛУЧЕНИЕ ЗАКАЗА =====
def get_order(message):

    order_text = message.text

    msg = bot.send_message(
        message.chat.id,
        "💰 Укажи бюджет:"
    )

    bot.register_next_step_handler(msg, get_budget, order_text)


def get_budget(message, order_text):

    budget = message.text
    user = message.from_user

    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    order_data = f"""
Новая заявка

Пользователь: @{user.username}
ID: {user.id}

Заказ:
{order_text}

Бюджет:
{budget}

Дата: {date}
"""

    orders.append(order_data)

    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(order_data + "\n\n")

    bot.send_message(
        ADMIN_ID,
        order_data
    )

    bot.send_message(
        message.chat.id,
        "✅ Заявка отправлена!"
    )


# ===== СТАТИСТИКА (ТОЛЬКО АДМИН) =====
@bot.message_handler(commands=['stats'])
def stats(message):

    if message.from_user.id != ADMIN_ID:
        return

    bot.send_message(
        message.chat.id,
        f"📊 Статистика\n\n"
        f"Пользователей: {len(users)}\n"
        f"Заявок: {len(orders)}"
    )


print("Бот запущен...")
bot.infinity_polling()# ================== ОБРАБОТКА КНОПОК ==================
user_data = {}

@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = message.from_user.id

    # Проверка подписки
    if not check_sub(user_id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Подписаться", url=f"https://t.me/{CHANNEL[1:]}")
        markup.add(btn)

        bot.send_message(
            message.chat.id,
            "❌ Подпишись на канал, чтобы пользоваться ботом:",
            reply_markup=markup
        )
        return

    text = message.text

    # ===== ЗАКАЗ =====
    if text == "📦 Заказать бота":
        bot.send_message(message.chat.id, "Опиши, какого бота ты хочешь:")
        user_data[user_id] = "waiting_order"

    elif user_data.get(user_id) == "waiting_order":
        bot.send_message(message.chat.id, "💰 Укажи примерный бюджет:")
        user_data[user_id] = {"order": message.text}

    elif isinstance(user_data.get(user_id), dict):
        order_info = user_data[user_id]["order"]
        budget = message.text

        bot.send_message(message.chat.id, "✅ Заявка отправлена! Я скоро свяжусь с тобой.")

        # Отправка админу
        bot.send_message(
            ADMIN_ID,
            f"📩 Новая заявка!\n\n"
            f"👤 @{message.from_user.username}\n"
            f"📝 Заказ: {order_info}\n"
            f"💰 Бюджет: {budget}"
        )

        user_data[user_id] = None

    # ===== ПРАЙС =====
    elif text == "💰 Прайс":
        bot.send_message(
            message.chat.id,
            "💰 Прайс:\n\n"
            "🤖 Простой бот — от 10$\n"
            "⚙️ Средний — от 25$\n"
            "🚀 Сложный — от 50$\n\n"
            "Точная цена зависит от задачи."
        )

    # ===== ПРИМЕРЫ =====
    elif text == "📁 Примеры":
        bot.send_message(
            message.chat.id,
            "📁 Примеры работ:\n\n"
            "— Боты для магазинов\n"
            "— Автоворонки\n"
            "— Боты с оплатой\n\n"
            "Подробнее в канале 👇"
        )

    # ===== СВЯЗЬ =====
    elif text == "📞 Связь":
        bot.send_message(
            message.chat.id,
            "📞 Напиши мне: @твой_юзернейм"
        )

    else:
        bot.send_message(message.chat.id, "Выбери кнопку 👇", reply_markup=main_menu())


# ================== ЗАПУСК ==================
print("Бот запущен...")
bot.infinity_polling(skip_pending=True)
