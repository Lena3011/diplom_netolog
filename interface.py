import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from config import comunity_token, offset
from core import *
from database import *


class BotInterface:

    def __init__(self, token):
        print('BotInterface запущен')
        self.bot = vk_api.VkApi(token=token)
        self.offset = offset

    def message_send(self, user_id, message=None, attachment=None):
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment})

    def handler(self):
        longpull = VkLongPoll(self.bot)
        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = str(event.user_id)
                profile_info = tools.get_profile_info(event.user_id)
                if event.text.lower() == 'привет':
                    self.message_send(event.user_id, f'Добрый день, введите слово ПОИСК')
                elif event.text.lower() == 'поиск':
                    create_table_viewed()
                    self.dict_user_serch = tools.user_serch(user_id, profile_info)
                    worksheet_id = tools.pop_person_id(user_id, self.dict_user_serch)
                    if worksheet_id:
                        self.handler_serch(user_id, worksheet_id)
                    else:
                        while worksheet_id is None:
                            self.dict_user_serch = tools.user_serch(user_id, profile_info)
                            worksheet_id = tools.pop_person_id(user_id, self.dict_user_serch)
                            if worksheet_id:
                                self.handler_serch(user_id, worksheet_id)
                elif event.text.lower() == 'далее':
                    worksheet_id = tools.pop_person_id(user_id, self.dict_user_serch)
                    if worksheet_id:
                        self.handler_serch(user_id, worksheet_id)
                    else:
                        print('далее - else')
                        while worksheet_id is None:
                            self.dict_user_serch = tools.user_serch(user_id, profile_info)
                            worksheet_id = tools.pop_person_id(user_id, self.dict_user_serch)
                            if worksheet_id:
                                self.handler_serch(user_id, worksheet_id)
                else:
                    self.message_send(event.user_id, 'Неизвестная команда. Введите слово ПОИСК или ДАЛЕЕ')

    def handler_serch(self, user_id, worksheet_id):
        self.message_send(user_id, f'ссылка - {tools.found_person_link(worksheet_id)}')
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
