import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import access_token, comunity_token
from core import *
from database import *


class BotInterface:

    def __init__(self, token):
        print('BotInterface запущен')
        self.bot = vk_api.VkApi(token=token)

    def message_send(self, user_id, message=None, attachment=None):
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment
                         }
                        )

    def handler(self):
        offset = 0
        longpull = VkLongPoll(self.bot)
        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = str(event.user_id)
                profile_info = tools.get_profile_info(event.user_id)
                if event.text.lower() == 'привет':
                    if profile_info:
                        print(tools.get_profile_info(event.user_id))
                        for i in profile_info:
                            profile_name = i.get('first_name')
                            print(profile_name)
                            self.message_send(event.user_id, f'Добрый день, {profile_name}, введите слово ПОИСК')
                    else:
                        print('Информации о пользоввателе не получено')
                elif event.text.lower() == 'поиск':
                    Base.metadata.create_all(engine)  # создаем таблицу БД
                    self.dict_user_serch = tools.user_serch(user_id, profile_info, offset)  # запускаем первичный поиск user_serch
                    self.handler_serch(user_id, self.dict_user_serch, profile_info, offset)  # обработчик выдает первого кондидата, смотрит есть ли он в БД, если нет и записывает его в БД
                elif event.text.lower() == 'далее':
                    print('Введено Далее')
                    if not self.dict_user_serch:
                        self.dict_user_serch = tools.user_serch(user_id, profile_info, offset)
                    for i in range(0, 1000):
                        offset += 1
                        self.handler_serch(user_id, self.dict_user_serch, profile_info, offset)
                        break

                else:
                    self.message_send(event.user_id, 'Неизвестная команда. Введите слово ПОИСК или ДАЛЕЕ')

    def handler_serch(self, user_id, dict_user_serch, profile_info, offset):
        print(f'def handler_serch - offset - {offset}')
        worksheet_info = tools.found_person_info(user_id, dict_user_serch)
        worksheet_id = tools.found_person_id(worksheet_info)
        # ТУТ ДОЛЖНА БЫТЬ ПРОВЕРКА СОВПОДЕНИЯ ID С ЧЕЛОВЕКОМ В БД
        # insert_data_viewed(user_id, worksheet_id) # НАЛАДИТЬ ОБРАЩЕНИЕ К БД
        self.message_send(user_id, f'{tools.found_person_name(worksheet_info)}, ссылка - {tools.found_person_link(worksheet_info)}')
        list_of_ids = tools.get_photos_id(worksheet_id)
        tools.get_id_photo_1(list_of_ids)
        media_1 = f'photo{worksheet_id}_{tools.get_id_photo_1(list_of_ids)}'
        self.message_send(user_id, 'фото 1', attachment=media_1)
        media_2 = f'photo{worksheet_id}_{tools.get_id_photo_2(list_of_ids)}'
        media_3 = f'photo{worksheet_id}_{tools.get_id_photo_3(list_of_ids)}'
        if tools.get_id_photo_2(list_of_ids) is not None:
            self.message_send(user_id, 'фото 2', attachment=media_2)
            self.message_send(user_id, 'фото 3', attachment=media_3)
        else:
            self.message_send(user_id, f'У пользователя фотографий больше нет')
        self.message_send(user_id, f'Для просмотра следущих анкет, введите слово ДАЛЕЕ')


if __name__ == '__main__':
    bot = BotInterface(comunity_token)
    tools = VkTools()
    bot.handler()
