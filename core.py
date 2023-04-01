from vk_api import ApiError
import vk_api
import datetime
from vk_api.longpoll import VkLongPoll
from random import randrange
from database import *


class VKBot:
    def __init__(self):
        print('Бот запущен')
        self.bot = vk_api.VkApi(token=comunity_token)
        self.ext_api = vk_api.VkApi(token=access_token)
        self.longpoll = VkLongPoll(self.bot)

    def message_send(self, user_id, message):
        self.bot.method('messages.send', {'user_id': user_id,
                                          'message': message,
                                          'random_id': randrange(10 ** 7)})

    def get_profile_name(self, user_id):
        try:
            info_dict = self.ext_api.method('users.get',
                                            {'user_id': user_id})
            for i in info_dict:
                for value in i.items():
                    profile_name = i.get('first_name')
                    return profile_name
        except ApiError:
            return print('get_profile_name! ошибка! access_token')

    def get_profile_sex(self, user_id):
        try:
            info_dict = self.ext_api.method('users.get',
                                            {'user_id': user_id,
                                             'fields': 'sex'})
            for i in info_dict:
                for value in i.items():
                    if i.get('sex') == 2:
                        find_sex = 1
                        return find_sex
                    elif i.get('sex') == 1:
                        find_sex = 2
                        return find_sex
        except ApiError:
            return

    def get_age_from(self, user_id):
        try:
            info_dict = self.ext_api.method('users.get', {'user_id': user_id, 'fields': 'bdate'})
            for i in info_dict:
                b_date = i.get('bdate')
                date_list = b_date.split('.')
                if len(date_list) == 3:
                    year = int(date_list[2])
                    year_now = int(datetime.date.today().year)
                    return year_now - year - 2
        except ApiError:
            return print('get_age_from! ошибка! access_token')

    def get_age_to(self, user_id):
        try:
            info_dict = self.ext_api.method('users.get', {'user_id': user_id, 'fields': 'bdate'})
            for i in info_dict:
                b_date = i.get('bdate')
                date_list = b_date.split('.')
                if len(date_list) == 3:
                    year = int(date_list[2])
                    year_now = int(datetime.date.today().year)
                    return year_now - year + 2
        except ApiError:
            return print('get_age_to! ошибка! access_token')

    def get_profile_city(self, user_id):
        try:
            info_dict = self.ext_api.method('users.get',
                                            {'user_id': user_id,
                                             'fields': 'city'})
            for i in info_dict:
                if 'city' in i:
                    city = i.get('city')
                    profile_city_id = str(city.get('id'))
                    return profile_city_id
        except ApiError:
            return print('get_profile_city! ошибка! access_token')

    def user_serch(self, user_id):
        try:
            profiles = self.ext_api.method('users.search',
                                           {'city_id': self.get_profile_city(user_id),
                                            'age_from': self.get_age_from(user_id),
                                            'age_to': self.get_age_to(user_id),
                                            'sex': self.get_profile_sex(user_id),
                                            'count': 30})

            list_1 = profiles['items']
            print('users.search отработал')
            for person_dict in list_1:
                if not person_dict.get('is_closed'):
                    first_name = person_dict.get('first_name')
                    last_name = person_dict.get('last_name')
                    vk_id = str(person_dict.get('id'))
                    vk_link = 'vk.com/id' + str(person_dict.get('id'))
                    insert_data_users(first_name, last_name, vk_id, vk_link)
                else:
                    continue
            return f'Поиск завершён'
        except ApiError:
            return print('users.search! ошибка! access_token')

    def get_photos_id(self, user_id):
        info_photo_dict = self.ext_api.method('photos.get',
                                              {'album_id': 'profile',
                                               'owner_id': user_id,
                                               'extended': 1,
                                               'count': 20})
        info_dict = dict()
        try:
            photos_dict_json = info_photo_dict['items']
            for i in photos_dict_json:
                photo_id = str(i.get('id'))
                i_likes = i.get('likes')
                if i_likes.get('count'):
                    likes = i_likes.get('count')
                    info_dict[likes] = photo_id
            list_of_ids = sorted(info_dict.items(), reverse=True)
            return list_of_ids
        except KeyError:
            return print('photos_get! ошибка!')

    def get_photo_1(self, user_id):
        list_photos_id = self.get_photos_id(user_id)
        count = 0
        for i in list_photos_id:
            count += 1
            if count == 1:
                return i[1]

    def get_photo_2(self, user_id):
        list_photos_id = self.get_photos_id(user_id)
        count = 0
        for i in list_photos_id:
            count += 1
            if count == 2:
                return i[1]

    def get_photo_3(self, user_id):
        list_photos_id = self.get_photos_id(user_id)
        count = 0
        for i in list_photos_id:
            count += 1
            if count == 3:
                return i[1]

    def send_photo_1(self, user_id, message, offset):
        self.bot.method('messages.send', {'user_id': user_id,
                                          'access_token': access_token,
                                          'message': message,
                                          'attachment': f'photo{self.person_id(offset)}_{self.get_photo_1(self.person_id(offset))}',
                                          'random_id': 0})

    def send_photo_2(self, user_id, message, offset):
        self.bot.method('messages.send', {'user_id': user_id,
                                          'access_token': access_token,
                                          'message': message,
                                          'attachment': f'photo{self.person_id(offset)}_{self.get_photo_2(self.person_id(offset))}',
                                          'random_id': 0})

    def send_photo_3(self, user_id, message, offset):
        self.bot.method('messages.send', {'user_id': user_id,
                                          'access_token': access_token,
                                          'message': message,
                                          'attachment': f'photo{self.person_id(offset)}_{self.get_photo_3(self.person_id(offset))}',
                                          'random_id': 0})

    def find_persons(self, user_id, offset):
        self.message_send(user_id, self.found_person_info(offset))
        self.person_id(offset)
        insert_data_viewed(self.person_id(offset), offset)
        self.get_photos_id(self.person_id(offset))
        self.send_photo_1(user_id, 'Фото 1', offset)
        if self.get_photo_2(self.person_id(offset)) != None:
            self.send_photo_2(user_id, 'Фото 2', offset)
            self.send_photo_3(user_id, 'Фото 3', offset)
        else:
            self.message_send(user_id, f'Фотографий больше нет!!')

    def found_person_info(self, offset):
        tuple_person = select_of_unviewed(offset)
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return f'{list_person[3]}'

    def person_id(self, offset):
        tuple_person = select_of_unviewed(offset)
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return str(list_person[2])


bot = VKBot()
