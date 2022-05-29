import telebot
from config import BOT_TOKEN
from botrequests.lowprice import CmdLowprice

bot = telebot.TeleBot(BOT_TOKEN)
list_commands = ['start', 'help', 'lowprice', 'highprice', 'bestdeal', 'history', 'reset']

states_users = {}  # user


def add_user(user_id: int, command: str, step: str):
    states_users[user_id] = {
        'command': command,
        'step': step,
        'data': {}
    }


def current_command(user_id: int):
    return states_users[user_id]['command']


def current_step(user_id: int):
    return states_users[user_id]['step']


def change_step(user_id: int, step: str):
    states_users[user_id]['step'] = step


def add_data(user_id: int, key, value):
    states_users[user_id]['data'][key] = value


def check_command_step(user_id: int, command: str, step: str):
    return current_command(user_id) == command and current_step(user_id) == step


@bot.message_handler(commands=['reset'])
def reset_state(message):
    bot.send_message(message.chat.id, 'Сброс состояния')


@bot.message_handler(commands=list_commands, func=lambda x: False)
def block_enter_commands(message):
    bot.send_message(message.chat.id, 'Проверка состояния')


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Привет! Ты запустили бота, который производит поиск отлей.\n'
                                      'Ознакомься с его командами - /help.')


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, 'Инструкция по работе бота.\n'
                                      '/lowprice - поиск топ самых дешёвых отелей в городе\n'
                                      '/highprice - поиск топ самых дорогих отелей в городе\n'
                                      '/bestdeal - поиск отелей наиболее подходящих по цене и расположению от центра\n'
                                      '/history - вывод истории поиска отелей\n'
                                      '/reset - сброс текущего поиска')


@bot.message_handler(commands=['lowprice'])
def lowprice_start(message):
    user_id = message.chat.id
    add_user(user_id, CmdLowprice.COMMAND_NAME, CmdLowprice.SCENARIO['start_step'])
    msg = CmdLowprice().get_msg(current_step(user_id))
    bot.send_message(user_id, msg)


@bot.message_handler(func=lambda message: check_command_step(
    message.chat.id, CmdLowprice.COMMAND_NAME, CmdLowprice.SCENARIO['start_step']))
def lowprice_city(message):
    user_id = message.chat.id
    add_data(user_id, 'city', message.text)
    change_step(user_id, CmdLowprice().get_next_step(current_step(user_id)))
    msg = CmdLowprice().get_msg(current_step(user_id))
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: check_command_step(
    message.chat.id, CmdLowprice.COMMAND_NAME, 'date_from'))
def lowprice_date_from(message):
    user_id = message.chat.id
    add_data(user_id, 'date_from', message.text)
    change_step(user_id, CmdLowprice().get_next_step(current_step(user_id)))
    msg = CmdLowprice().get_msg(current_step(user_id))
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: check_command_step(
    message.chat.id, CmdLowprice.COMMAND_NAME, 'date_to'))
def lowprice_date_to(message):
    user_id = message.chat.id
    add_data(user_id, 'date_to', message.text)
    change_step(user_id, CmdLowprice().get_next_step(current_step(user_id)))
    msg = CmdLowprice().get_msg(current_step(user_id))
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: check_command_step(
    message.chat.id, CmdLowprice.COMMAND_NAME, 'count_hotels'))
def lowprice_count_hotels(message):
    user_id = message.chat.id
    add_data(user_id, 'count_hotels', message.text)
    change_step(user_id, CmdLowprice().get_next_step(current_step(user_id)))
    msg = CmdLowprice().get_msg(current_step(user_id))
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: check_command_step(
    message.chat.id, CmdLowprice.COMMAND_NAME, 'need_photo'))
def lowprice_need_photos(message):
    user_id = message.chat.id
    add_data(user_id, 'need_photo', message.text)
    steps = CmdLowprice().get_next_step(current_step(user_id))
    print(steps)
    if message.text.lower() == 'да':
        change_step(user_id, steps[0])
    else:
        change_step(user_id, steps[1])
    msg = CmdLowprice().get_msg(current_step(user_id))
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: check_command_step(
    message.chat.id, CmdLowprice.COMMAND_NAME, 'count_photo'))
def lowprice_count_photos(message):
    user_id = message.chat.id
    add_data(user_id, 'count_photo', message.text)
    change_step(user_id, CmdLowprice().get_next_step(current_step(user_id)))
    msg = CmdLowprice().get_msg(current_step(user_id))
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: check_command_step(
    message.chat.id, CmdLowprice.COMMAND_NAME, 'get_results'))
def lowprice_get_result(message):
    user_id = message.chat.id
    change_step(user_id, CmdLowprice().get_next_step(current_step(user_id)))
    print(states_users)


if __name__ == '__main__':
    bot.infinity_polling()
