from django.core.management.base import BaseCommand
from ... import constants as text
from ... import models
from django.conf import settings
import telebot


bot = telebot.TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


@bot.message_handler(['start'])
def start(message):
    models.Telegram.objects.get_or_create(
        id=message.from_user.id,
        defaults={
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name
        }
    )

    bot.send_message(message.chat.id, text.START_MESSAGE)


@bot.message_handler(['test'])
def test(message):
    # markup = telebot.types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton(text='Testing', url='https://youtube.com/'))

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    website = telebot.types.KeyboardButton('Hello World!')
    start = telebot.types.KeyboardButton('Start')

    markup.add(website, start)

    bot.send_message(
        chat_id=message.chat.id,
        text='Testing',
        reply_markup=markup
    )


class Command(BaseCommand):
    help = 'Telegram bot setup command '

    def handle(self, *args, **kwargs):
        print('Telegram bot started')
        bot.infinity_polling()
