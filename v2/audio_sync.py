#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""Данный скрипт предназначен для синхронизации плейлиста пользователя
    на локальный компьютер"""

import connect, manipulation, sys, os
import logging

#Директория по умолчанию
#path = 'vkmusic'
        
if __name__ == '__main__':
    if os.name == 'nt':
        tmp = os.environ["TMP"]
    elif os.name == 'posix':
        tmp = '/var/tmp'
    logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s', level = logging.INFO, filename = r'{0}/vk_audio_sync.log'.format(tmp))
    """Проверяем версию питона"""
    if sys.version.split(' ')[0].split('.')[0] == '3':
        print('Вы используете python3')
    elif sys.version.split(' ')[0].split('.')[0] == '2':
        print('Вы используете python2')
    if len(sys.argv) > 4:
        path = 'vkmusic'
        for i in list(range(1,len(sys.argv),2)):
            if sys.argv[i] == '-login':
                login = sys.argv[i+1]
            elif sys.argv[i] == '-pass':
                password = sys.argv[i+1]
            elif sys.argv[i] == '-dir':
                path = sys.argv[i+1]
        profile = connect.connect_vk(login, password)
        user = profile.my_id()
        counter = profile.audio_count(user)
        manip = manipulation.manip()
        dirr = manip.check_dir(path)
        for i in range(counter):
            print('-'*80)
            artist, title, url = profile.track_info(i)
            name = artist + '-' + title
            check = manip.check_track(name)
            if check == False:
                manip.download(url, name, dirr)
        del profile
    else:
        print("""Введены некорректные данные.
Необходимо указакать ./audio_sync.py -login Ваш_логин -pass Ваш_пароль -dir Директория_сохранения
""")
        exit()
