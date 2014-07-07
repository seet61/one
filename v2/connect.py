# -*- coding: utf-8 -*-

import vk
import logging

class connect_vk:
    def __init__(self, login, password):
        """Инициализация соединения"""
        self.connect = vk.API('4394430', '{0}'.format(login), '{0}'.format(password), scope=(+8))
        logging.info('Установлено соединение с vk для пользователя {0}'.format(login))
        print('Установлено соединение с vk для пользователя {0}'.format(login))

    def my_id(self):
        """Получавем id пользователя который зарегистрировался."""
        user = self.connect.users.get()[0]
        return user['id']
    
    def audio_count(self, user):
        """Метод возврашает счетчик колличества треков в плейлисте"""
        self.tracks = self.connect.audio.get(owner_id = user)
        counter = self.tracks["count"]
        print ("Треков:", counter)
        logging.info("Треков: {0}".format(counter))
        return counter

    def track_info(self, i):
        """Получаем необходимую информацию об i'ом треке"""
        for key in self.tracks["items"][i].keys():
            if key == 'artist':
                artist = self.tracks["items"][i][key]
            elif key == 'title':
                title = self.tracks["items"][i][key]
            elif key == 'url':
                url = self.tracks["items"][i][key]
        print('Получаем данные о track № {0}'.format(i))
        print('artist:' ,artist,'title:', title)
        logging.info('Получаем данные о track № {0}'.format(i))
        logging.info('{0} - {1}'.format(artist, title))
        return artist, title, url

    def __del__(self):
        """Закрытие соединения"""
        logging.info('Соединение с vk закрыто')
        print('Соединение с vk закрыто')
        input('Работа программы окончена. Для выхода нажмите Enter.')
