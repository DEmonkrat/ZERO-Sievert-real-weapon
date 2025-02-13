import os
import re
import shutil
import pandas as pd
import PySimpleGUI as sg
from ZERO_text_lang import *

def_path = r'C:\Program Files (x86)\Steam\steamapps\common\ZERO Sievert\ZS_vanilla\gamedata'
path = ''
# Переменная cur_lang отвечает за текущий язык интерфейса
# 0 - английский (по умолчанию)
# 1 - русский
cur_version = '1.1'
cur_lang = 0
status_text = status_dict['default']
status_text_color = None


def status(text: str, text_color=None):
    # При обновлении текста в StatusBar, если новая строка длиннее предыдущей, то
    # она выводится не полностью
    # Поэтому функция status заполняет ее пробелами
    if text_color is not None:
        window['-STAT_BAR-'].update(text + ' ' * (110 - len(text)), text_color=text_color)
    else:
        window['-STAT_BAR-'].update(text + ' ' * (110 - len(text)))


def find_folder():
    return sg.popup_get_folder('Find your "weapon.json" and "w_mod.json" files folder. Then press "Execute" again.',
                               'Find your "weapon.json" and "w_mod.json" folder')


def check_files(path):
    return os.path.isfile(path)


def open_json(path):
    # Открываем JSON файлы с оружием и модами
    global wep_df, wep_mod_df
    wep_df = pd.read_json(os.path.join(path, 'weapon.json'), typ='series')
    wep_mod_df = pd.read_json(os.path.join(path, 'w_mod.json'), typ='series')


def export_json():
    # Экспорт в JSON файлов с изменениями
    wep_df.to_json('weapon.json', orient="index", indent=4)
    wep_mod_df.to_json('w_mod.json', orient="index", indent=4)


def change_names():
    # Открываем файл weapon_real и w_mod_real.txt с реальными названиями и делаем из них словари.
    # Для это необходимо в txt писать в виде словаря !!!
    with open('weapon_real.txt') as f:
        wep_rename = f.read()
    wep_rename = eval(wep_rename.replace('\n', ''))
    with open('w_mod_real.txt') as f:
        wep_mod_rename = f.read()
    wep_mod_rename = eval(wep_mod_rename.replace('\n', ''))
    # Пробегаем по всему оружию в экспортированном JSON игры и смотрим есть ли такие названия в txt.
    # Если есть, то заменяем
    # При этом ключом служит название оружия в игре !!! А значение уже реальное название
    for old_name in wep_df['data'].keys():
        if wep_df['data'][old_name]['basic']['name'] in wep_rename:
            wep_df['data'][old_name]['basic']['name'] = wep_rename[wep_df['data'][old_name]['basic']['name']]
    # замена названий в модах (всех кроме ЕС который АК)
    for old_name in wep_mod_df['data'].keys():
        for new_name in wep_mod_rename.keys():
            # Для поиска используем регулярное выражение
            reg = r'\b' + new_name + r'\s'
            if re.search(reg, wep_mod_df['data'][old_name]['basic']['name']):
                wep_mod_df['data'][old_name]['basic']['name'] = re.sub(reg, wep_mod_rename[new_name] + ' ',
                                                                       wep_mod_df['data'][old_name]['basic']['name'])
    # замена ЕС (в модах)
    string = 'EC'
    # Ищем ЕС (начало слова; в конце без букв, цифр и символов подчеркивания. Например, ЕС-74 найдет, а ЕСМ нет)
    reg = r'\b' + string + r'\W'
    for old_name in wep_mod_df['data'].keys():
        if re.search(reg, wep_mod_df['data'][old_name]['basic']['name']):
            wep_mod_df['data'][old_name]['basic']['name'] = wep_mod_df['data'][old_name]['basic']['name'].replace('EC',
                                                                                                                  'AK')


def add_mods_for_vintar():
    # Открываем JSON файлы с оружием и модами
    global wep_df, wep_mod_df
    # добавляем моды для vintar_bc
    for old_name in wep_mod_df['data'].keys():
        try:
            # Смотрим наличие as_val и отсутствие vintar_bc (последнее - защита от дублирования, если несколько раз
            # запускалась программа)
            if ('as_val' in wep_mod_df['data'][old_name]['weapon_mod']['weapon_id'] and
                    not 'vintar_bc' in wep_mod_df['data'][old_name]['weapon_mod']['weapon_id']):
                wep_mod_df['data'][old_name]['weapon_mod']['weapon_id'].append('vintar_bc')
        except:
            pass


def make_vintar_customizable():
    # Открываем JSON файлы с оружием и модами
    global wep_df, wep_mod_df
    # кастомизация vintar_bc
    wep_df['data']['vintar_bc']['weapon']['mods'] = wep_df['data']['as_val']['weapon']['mods']
    # Замена дефолтного спрайта vintar_bc на стандартный as_val. Иначе получается наложение спрайтов
    wep_df['data']['vintar_bc']['basic']['sprite_inv'] = wep_df['data']['as_val']['basic']['sprite_inv']


def update(path):
    global status_text, status_text_color
    # Смотрим какие опции выбраны
    if values['-RENAME_chbx-'] | values['-ALLMODSVINTAR_chbx-']:
        status_text = status_dict['update']
        status(status_text[cur_lang],
               status_text_color := '#c2ffa7')
        open_json(path)
        if values['-RENAME_chbx-']:
            change_names()
        if values['-ALLMODSVINTAR_chbx-']:
            make_vintar_customizable()
            add_mods_for_vintar()
        export_json()
        if values['-CHANGE_FILES_chbx-']:
            replace_files(path)
        status_text = status_dict['done']
        status(status_text[cur_lang],
               status_text_color := '#c2ffa7')
    else:  # Если не выбрана ни одна опция, выдаем сообщение в статус
        status_text = status_dict['no_options']
        status(status_text[cur_lang],
               status_text_color := '#FFFF00')


def change():
    global status_text, status_text_color
    if not check_files('w_mod_real.txt'):
        status_text = status_dict['no_file_mod']
        status(status_text[cur_lang],
               status_text_color := '#FFFF00')
        sg.popup_ok('No file "w_mod_real.txt" in app folder. Can`t continue.', title='No file')
        return
    if not check_files('weapon_real.txt'):
        status_text = status_dict['no_file_weap']
        status(status_text[cur_lang],
               status_text_color := '#FFFF00')
        sg.popup_ok('No file "weapon_real.txt" in app folder. Can`t continue.', title='No file')
        return
    global path
    if not path:
        # Проверка наличия файлов в папке игры по умолчанию (если путь path пуст)
        if check_files(os.path.join(def_path, 'w_mod.json')) and check_files(os.path.join(def_path, 'weapon.json')):
            path = def_path
            status_text = status_dict['found']
            status(status_text[cur_lang],
                   status_text_color := '#c2ffa7')
            update(path)
        else:  # Если не нашли файлы в каталоге по умолчанию, то запрашиваем у пользователя
            status_text = status_dict['not_found']
            status(status_text[cur_lang],
                   status_text_color := '#FFFF00')
            path = find_folder()
    else:
        # Повторная проверка наличия файлов игры (имеется путь path)
        if check_files(os.path.join(path, 'w_mod.json')) and check_files(os.path.join(path, 'weapon.json')):
            status_text = status_dict['found']
            status(status_text[cur_lang],
                   status_text_color := '#c2ffa7')
            update(path)
        else:  # Если не нашли файлы в каталоге по умолчанию, то запрашиваем у пользователя
            status_text = status_dict['not_found']
            status(status_text[cur_lang],
                   status_text_color := '#FFFF00')
            path = find_folder()


def replace_files(path):
    # 1. Сначала пробуем переименовать оригинальные файлы
    try:
        os.rename(os.path.join(path, 'weapon.json'), os.path.join(path, 'weapon_ORIG.json'))
        os.rename(os.path.join(path, 'w_mod.json'), os.path.join(path, 'w_mod_ORIG.json'))
    except FileExistsError:
        # Если файлы существуют, то ...
        delete = sg.popup_yes_no(window_msg_dict['err_rename'][cur_lang],
                                 title=title_popup__dict['warning'][cur_lang])
        if delete == 'Yes':
            # 1.1 Если файлы существуют и пользователь соглашается их удалить, то
            # пробуем удалить
            try:
                os.remove(os.path.join(path, 'weapon_ORIG.json'))
                os.remove(os.path.join(path, 'w_mod_ORIG.json'))
            except:
                sg.popup_ok(window_msg_dict['err_del'][cur_lang],
                            title=title_popup__dict['warning'][cur_lang])
        else:
            # 1.2 Если файлы существуют и пользователь НЕ соглашается их удалить, то
            # сообщаем ему и заканчиваем ВСЮ ФУНКЦИЮ
            sg.popup_ok(window_msg_dict['no_del'][cur_lang],
                        title=title_popup__dict['warning'][cur_lang])
            return
    except:
        # 1.3 Если невозможно переименовать файлы по неизвестной причине, то
        # сообщаем пользователю и заканчиваем ВСЮ ФУНКЦИЮ
        sg.popup_ok(window_msg_dict['cant_rename'][cur_lang])
        return

    else:
        # 2. Если оригинальные файлы переименованы успешно, то
        #    пробуем скопировать новые файлы в директорию игры
        try:
            shutil.copyfile('weapon.json', os.path.join(path, 'weapon.json'))
            shutil.copyfile('w_mod.json', os.path.join(path, 'w_mod.json'))
        except:
            # Если что-то пошло не так, выдаем сообщение об ошибке
            sg.popup_ok(window_msg_dict['err_replace'][cur_lang] + path,
                        title=title_popup__dict['wrong_copy'][cur_lang])
        else:
            # Если все хорошо, информируем, что файлы были заменены
            sg.popup_ok(window_msg_dict['info_done'][cur_lang],
                        title=title_popup__dict['done'][cur_lang])


def change_lang():
    window['-TEXT_BOX-'].update(value=text_box_dict['default'][cur_lang])
    window.set_title(title_comon__dict['default'][cur_lang])
    # Цикл для переименования статических элементов
    for key in static_btn_dict.keys():
        window[key].update(static_btn_dict[key][cur_lang])
    for key in static_chbx_dict.keys():
        window[key].update(text=static_chbx_dict[key][cur_lang])
    # Меняем язык панели Статуса от глобальных переменных
    status(status_text[cur_lang], status_text_color)


layout = [
    [sg.StatusBar(status_text[cur_lang] + ' ' * 95, k='-STAT_BAR-'),
     sg.Text('Ver ' + cur_version)],
    # StatusBar Необходимо полностью заполнить для правильного отображения
    # при изменении текста
    [sg.Column([[sg.Checkbox(static_chbx_dict['-RENAME_chbx-'][cur_lang],
                             default=True,
                             k='-RENAME_chbx-')],
                [sg.Checkbox(static_chbx_dict['-ALLMODSVINTAR_chbx-'][cur_lang],
                             k='-ALLMODSVINTAR_chbx-')],
                [sg.HorizontalSeparator()],
                [sg.Checkbox(static_chbx_dict['-CHANGE_FILES_chbx-'][cur_lang],
                             default=True,
                             k='-CHANGE_FILES_chbx-')]]),
     sg.Multiline(def_text_eng,
                  write_only=True,
                  size=(80, 7),
                  k='-TEXT_BOX-')],
    [sg.Button(static_btn_dict['-EXEC_btn-'][cur_lang],
               k='-EXEC_btn-'),
     sg.Exit(static_btn_dict['-EXIT-'][cur_lang],
             k='-EXIT-'),
     sg.Push(), sg.Button('Pyc'), sg.Button('Eng')]
]

window = sg.Window('Weapon real names', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '-EXIT-':  # if user closes window or clicks cancel
        break
    if event == 'Eng':
        cur_lang = 0
        change_lang()

    if event == 'Pyc':
        cur_lang = 1
        change_lang()

    if event == '-EXEC_btn-':
        change()

window.close()
