from vk_api.longpoll import VkEventType
from core import *

for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = str(event.user_id)
        msg = event.text.lower()
        if event.text.lower() == 'привет':
            bot.message_send(user_id, f'Привет, чат-бот найдет ваших ровесников противоположного пола в вашем городе. введите слово ПОИСК')
        elif event.text.lower() == 'поиск':
            creating_database()
            bot.user_serch(user_id)
            bot.find_persons(user_id, offset)
            bot.message_send(event.user_id, f' {bot.get_profile_name(event.user_id)}, для продолжения поиска введите слово ДАЛЕЕ')
        elif event.text.lower() == 'далее':
            for i in line:
                offset += 1
                bot.find_persons(user_id, offset)
                break

        else:
            bot.message_send(event.user_id, 'Неизвестная команда. Если хотите начать поиск, введите слово ПОИСК')
