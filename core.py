import requests
import vk_api
import datetime
from interface import *
from config import access_token, offset
from vk_api.exceptions import ApiError



class VkTools:
    def __init__(self):
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
                    return find_sex

    def get_age_from(self, profile_info):
        for i in profile_info:
            b_date = i.get('bdate')
            date_list = b_date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                age_from = year_now - year - 2
                return age_from

    def get_age_to(self, profile_info):
        for i in profile_info:
            b_date = i.get('bdate')
            date_list = b_date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                age_to = year_now - year + 2
                return age_to

    def user_serch(self, user_id, profile_info):
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
                                            'count': 300})
        except ApiError:
            return
        profiles = profiles['items']
        dict_user_serch = []
        for profile in profiles:
            if profile['is_closed'] == False:
                dict_user_serch.append(
                    {'name': profile['first_name'] + ' ' + profile['last_name'], 'id': profile['id']})
        return dict_user_serch

    def pop_person_id(self, user_id, dict_user_serch):  # выталкивает одну анкету из dict_user_serch
        if dict_user_serch == []:
            return
        else:
            worksheet_info = dict_user_serch.pop()
            worksheet_id = worksheet_info['id']
            from_bd = select_of_unviewed(user_id)  # получили все ID просмотренные пользователем
            from_bd_list = []
            for i in from_bd:
                from_bd_list.append(i[0])
            if worksheet_id in from_bd_list:
                return
            else:
                insert_data_viewed(user_id, worksheet_id)
                return worksheet_id

    def found_person_link(self, worksheet_id):
        worksheet_link = 'vk.com/id' + str(worksheet_id)
        return worksheet_link

    def get_photos_id(self, worksheet_id):
        info_photo_dict = self.ext_api.method('photos.get',
                                              {'album_id': 'profile',
                                               'owner_id': worksheet_id,
                                               'extended': 1,
                                               'count': 50})
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

    def get_id_photo_1(self, list_of_ids):
        count = 0
        for i in list_of_ids:
            count += 1
            return i[1]

    def get_id_photo_2(self, list_of_ids):
        count = 0
        for i in list_of_ids:
            count += 1
            if count == 2:
                return i[1]

    def get_id_photo_3(self, list_of_ids):
        count = 0
        for i in list_of_ids:
            count += 1
            if count == 3:
                return i[1]
