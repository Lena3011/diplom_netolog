import requests
import vk_api
import datetime
from vk_api.utils import get_random_id
from interface import *
from config import access_token
from vk_api.exceptions import ApiError


class VkTools:
    def __init__(self):
        print('VkTools запущен')
        self.ext_api = vk_api.VkApi(token=access_token)
        self.bot = vk_api.VkApi(token=comunity_token)

    def get_profile_info(self, user_id):
        try:
            profile_info = self.ext_api.method('users.get',
                                               {'user_id': user_id,
                                                'fields': 'bdate,city,sex,relation'})
        except ApiError:
            return print('get_profile_info! ошибка! access_token')
        return profile_info

    def get_profile_city(self, profile_info):
        for i in profile_info:
            if 'city' in i:
                city = i.get('city')
                profile_city_id = str(city.get('id'))
                print(profile_city_id)
                return profile_city_id

    def get_profile_sex(self, profile_info):
        for i in profile_info:
            for value in i.items():
                if i.get('sex') == 2:
                    find_sex = 1
                    print(find_sex)
                    return find_sex
                elif i.get('sex') == 1:
                    find_sex = 2
                    print(find_sex)
                    return find_sex

    def get_age_from(self, profile_info):
        for i in profile_info:
            b_date = i.get('bdate')
            date_list = b_date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                age_from = year_now - year - 2
                print(age_from)
                return age_from

    def get_age_to(self, profile_info):
        for i in profile_info:
            b_date = i.get('bdate')
            date_list = b_date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                age_to = year_now - year + 2
                print(age_to)
                return age_to

    def user_serch(self, user_id, profile_info, offset):
        # profile_info = self.get_profile_info(user_id)
        print(f'def user_serch - offset - {offset}')
        if profile_info:
            print(self.get_profile_info(user_id))
        else:
            print('информация о пользователе не получена')
        try:
            profiles = self.ext_api.method('users.search',
                                           {'city_id': self.get_profile_city(profile_info),
                                            'age_from': self.get_age_from(profile_info),
                                            'age_to': self.get_age_to(profile_info),
                                            'sex': self.get_profile_sex(profile_info),
                                            'count': 50,
                                            'offset': offset})
        except ApiError:
            return
        profiles = profiles['items']
        dict_user_serch = []
        for profile in profiles:
            if profile['is_closed'] == False:
                dict_user_serch.append(
                    {'name': profile['first_name'] + ' ' + profile['last_name'], 'id': profile['id']})
        print(f'сработал - def user_serch')
        print(f'dict_user_serch - {dict_user_serch}')
        return dict_user_serch

    def found_person_info(self, user_id, dict_user_serch):  # выталкивает одну анкету из dict_user_serch
        print(f'в found_person_info пришло - {dict_user_serch}')
        try:
            worksheet_info = dict_user_serch.pop()
            print(f'worksheet_info - из dict_user_serch достали: {worksheet_info}')
            return worksheet_info
        except KeyError:
            bot.message_send(user_id, 'Вы просмотрели всех возможных кандидатов!')


    def found_person_id(self, worksheet_info):
        worksheet_id = worksheet_info['id']
        print(f'worksheet_id - {worksheet_id}')
        return worksheet_id

    def found_person_name(self, worksheet_info):
        worksheet_name = worksheet_info['name']
        print(f'worksheet_name - {worksheet_name}')
        return worksheet_name

    def found_person_link(self, worksheet_info):
        worksheet_link = 'vk.com/id' + str(worksheet_info['id'])
        print(f'worksheet_link - {worksheet_link}')
        return worksheet_link

    def get_photos_id(self, worksheet_id):
        info_photo_dict = self.ext_api.method('photos.get',
                                              {'album_id': 'profile',
                                               'owner_id': worksheet_id,
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
            print(f'list_of_ids - {list_of_ids}')
            return list_of_ids
        except KeyError:
            return print('photos_get! ошибка!')

    def get_id_photo_1(self, list_of_ids):
        count = 0
        for i in list_of_ids:
            count += 1
            return i[1]

    def get_id_photo_2(self,  list_of_ids):
        count = 0
        for i in list_of_ids:
            count += 1
            if count == 2:
                return i[1]

    def get_id_photo_3(self,  list_of_ids):
        count = 0
        for i in list_of_ids:
            count += 1
            if count == 3:
                return i[1]
