# -*- coding: utf-8 -*-

import os, shutil
import logging
import urllib.request as request

class manip:
    def check_dir(self, path):
        """Метод проверяет наличие папки 'vkmusic' в директории в /home"""
        try:
            os.chdir(os.environ["HOME"])
            os.chdir('{0}'.format(path))
            logging.info('Переходим в папку {0}'.format(os.getcwd()))
            print('Переходим в папку {0}'.format(os.getcwd()))
            return os.getcwd()
        except FileNotFoundError:
            logging.warning('Папка {0} не существует!'.format(path))
            print('Папка {0} не существует!'.format(path))
            os.chdir(os.environ["HOME"])
            os.mkdir('{0}'.format(path))
            os.chdir(r'{0}'.format(path))
            logging.info('Создаем папку')
            print('Создаем папку')
            return os.getcwd()

    def check_track(self, name):
        """Проверяем не скачан ли данный файл"""
        if name + '.mp3' in os.listdir():
            logging.info('Данный файл уже загружен')
            print('Данный файл уже загружен')
            return True
        else:
            logging.info('Данный файл еще не загружен')
            print('Данный файл еще не загружен')
            return False

    def download(self, url, name, dirr):
        """Скачиваем файл и приводим его название в нормальный вид"""
        print('Скачиваем файл')
        file = request.URLopener()
        response = file.retrieve(url)
        response = list(response)[0]
        if os.path.exists(response):
            print('Перемещаем файл в директорию {0}'.format(dirr))
            shutil.move(response, dirr)
            if '\\' in response:
                os.rename(dirr+'\\{0}'.format(response.split('\\')[-1]), '{0}.mp3'.format(name))
            elif '/' in response:
                os.rename(dirr+'/{0}'.format(response.split('/')[-1]), '{0}.mp3'.format(name))
            print('Переименовываем файл {0}'.format(name))
            logging.info('Переименовываем файл {0}'.format(name))
        else:
            print('Произошла какая-то ошибка')
            logging.info('Произошла какая-то ошибка')
        del response
        file.close()
