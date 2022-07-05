from loader import bot
from telebot.types import Message, InputMediaPhoto, ReplyKeyboardRemove
from utils.parsers import parser_hotels, parser_urls_photos
from keyboards import inline


def send_results(message: Message, sort_order) -> None:
    bot.send_message(message.from_user.id, 'Ищу отели...\nПодожди немного')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['sort_order'] = sort_order
        hotels = parser_hotels.find_hotels(**data)

        for hotel in hotels:
            msg_text = f'Название отеля: {hotel["name"]}\n' \
                       f'Адрес: {hotel["address"]}\n' \
                       f'Стоимость одних суток: {hotel["rate"]}\n' \
                       f'Стоимость за весь период проживания: {hotel["rate_all"]}\n'
            markup = inline.url.get_markup(text=hotel['name'], url=hotel['url'])
            bot.send_message(message.from_user.id, msg_text, disable_web_page_preview=True, reply_markup=markup)
            if data['need_photos'].lower() == 'да':
                urls_photos = parser_urls_photos.find_urls_photos(hotel['id'], data['count_photos'])
                medias = [InputMediaPhoto(url_photo) for url_photo in urls_photos]
                bot.send_media_group(message.from_user.id, medias)

    bot.send_message(message.from_user.id, 'Поиск закончен!', reply_markup=ReplyKeyboardRemove())
    bot.set_state(message.from_user.id, None, message.chat.id)
