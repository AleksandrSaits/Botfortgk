import telebot
from telebot import types

TOKEN = "8755271111:AAEi6jCO2sMh9A3A6Cmpn4SDK69uT8cuJBo"
ADMIN_ID = 8559107011  # твой Telegram ID
CHANNEL = "@alex_ai_devel"  # твой канал

bot = telebot.TeleBot(TOKEN)

# ================== КНОПКИ ==================
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📦 Заказать бота")
    btn2 = types.KeyboardButton("💰 Прайс")
    btn3 = types.KeyboardButton("📁 Примеры")
    btn4 = types.KeyboardButton("📞 Связь")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# ================== СТАРТ ==================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет!\n\nЯ помогу тебе заказать Telegram-бота 🤖\n\nВыбери действие:",
        reply_markup=main_menu()
    )

# ================== ПРОВЕРКА ПОДПИСКИ ==================
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status != "left"
    except:
        return False

# ================== ОБРАБОТКА КНОПОК ==================
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
bot.infinity_polling()
