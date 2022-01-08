import telebot
import config
import stratz_requests

bot = telebot.TeleBot(config.BOT_TOKEN)

all_heroes = config.all_heroes


commands_list = '/hero_info - get statistic about hero\n' \
                '/help - list of commands'


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Welcome, {0}'.format(message.from_user.first_name))


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, commands_list)


@bot.message_handler(commands=['hero_info'])
def cmd_hero_info(message):
    bot.send_message(message.chat.id, 'Send hero name')
    bot.register_next_step_handler(message, get_hero_message)


def get_hero_message(message):
    if message.text == 'cancel':
        return
    for hero in all_heroes['heroName']:
        if hero == message.text:
            msg = stratz_requests.find_hero_info(message.text)
            bot.send_message(message.chat.id, text='{heroName} winrate for last 2 months is {msg}%'.format(heroName=message.text, msg=msg))
            return
    msg = bot.send_message(message.chat.id, text='Wrong hero name, try again or type "cancel" ')
    bot.register_next_step_handler(msg, get_hero_message)


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     try:
#         if call.message:
#             if call.data == 'cancel':
#                 bot.send_message(call.message.chat.id, 'Canceled')
#                 bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
#     except Exception as e:
#         print(repr(e))


# RUN
bot.polling(none_stop=True)