import os
import re
import shutil
import pandas as pd
import PySimpleGUI as sg

def_path = r'C:\Program Files (x86)\Steam\steamapps\common\ZERO Sievert\ZS_vanilla\gamedata'
path = ''


def status(text: str, text_color=None):
    # При обновлении текста в StstusBar, если новая строка длиннее предыдущей, то
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
    global wep_df, wep_mod_df
    wep_df = pd.read_json(os.path.join(path, 'weapon.json'), typ='series')
    wep_mod_df = pd.read_json(os.path.join(path, 'w_mod.json'), typ='series')


def export_json():
    # Экспорт в JSON файлов с изменениями
    wep_df.to_json('weapon.json', orient="index", indent=4)
    wep_mod_df.to_json('w_mod.json', orient="index", indent=4)


def change_names():
    # Открываем JSON файлы с оружием и модами
    global wep_df, wep_mod_df
    # Открываем файл weapon_real и w_mod_real.txt с реальными названиями и делаем из них словари.
    # Для это необходимо в txt писать в виде словаря !!!
    with open('weapon_real.txt') as f:
        wep_rename = f.read()
    wep_rename = eval(wep_rename.replace('\n', ''))
    with open('w_mod_real.txt') as f:
        wep_mod_rename = f.read()
    wep_mod_rename = eval(wep_mod_rename.replace('\n', ''))
    # Пробегаем по всему оружию в JSON и смотрим есть ли такие названия в txt. Если есть, то заменяем
    # При этом ключом служит название оружия в игре !!! А значение уже реальное название
    for old_name in wep_df['data'].keys():
        if wep_df['data'][old_name]['basic']['name'] in wep_rename:
            wep_df['data'][old_name]['basic']['name'] = wep_rename[wep_df['data'][old_name]['basic']['name']]
    # замена названий в модах (всех кроме ЕС который АК)
    for old_name in wep_mod_df['data'].keys():
        for new_name in wep_mod_rename.keys():
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
            if 'as_val' in wep_mod_df['data'][old_name]['weapon_mod']['weapon_id']:
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
    # Смотрим какие опции выбраны
    if values['-RENAME_CB-'] | values['-ALLMODSVINTAR_CB-']:
        status('Starting update', '#c2ffa7')
        open_json(path)
        if values['-RENAME_CB-']:
            change_names()
        if values['-ALLMODSVINTAR_CB-']:
            make_vintar_customizable()
            add_mods_for_vintar()
        export_json()
        if values['-CHANGE_FILES-']:
            replace_files(path)
        status('Done', '#c2ffa7')
    else:  # Если не выбрана ни одна опция, выдаем сообщение в статус
        status('No options to execute', '#FFFF00')


def change():
    if not check_files('w_mod_real.txt'):
        status('No file w_mod_real.txt', text_color='#FFFF00')
        sg.popup_ok('No file "w_mod_real.txt" in app folder. Can`t continue.', title='No file')
        return
    if not check_files('weapon_real.txt'):
        status('No file "weapon_real.txt"', text_color='#FFFF00')
        sg.popup_ok('No file "weapon_real.txt" in app folder. Can`t continue.', title='No file')
        return
    global path
    if not path:
        # Проверка наличия файлов в папке игры по умолчанию (если путь path пуст)
        if check_files(os.path.join(def_path, 'w_mod.json')) and check_files(os.path.join(def_path, 'weapon.json')):
            path = def_path
            status('Files found', text_color='#c2ffa7')
            update(path)
        else:  # Если не нашли файлы в каталоге по умолчанию, то запрашиваем у пользователя
            status('Files not found. Choose directory and click "Execute" again', text_color='#FFFF00')
            path = find_folder()
    else:
        # Повторная проверка наличия файлов игры (имеется путь path)
        if check_files(os.path.join(path, 'w_mod.json')) and check_files(os.path.join(path, 'weapon.json')):
            status('Files found', text_color='#c2ffa7')
            update(path)
        else:  # Если не нашли файлы в каталоге по умолчанию, то запрашиваем у пользователя
            status('Files not found. Choose directory and click "Execute" again', text_color='#FFFF00')
            path = find_folder()


def replace_files(path):
    try:
        os.rename(os.path.join(path, 'weapon.json'), os.path.join(path, 'weapon_ORIG.json'))
        os.rename(os.path.join(path, 'w_mod.json'), os.path.join(path, 'w_mod_ORIG.json'))
    except FileExistsError:
        sg.popup_ok('Files "weapon_ORIG.json" and "w_mod_ORIG.json" already exists in game folder. '
                    'They will not be changed', title='Warning')
    except:
        pass

    try:
        shutil.copyfile('weapon.json', os.path.join(path, 'weapon.json'))
        shutil.copyfile('w_mod.json', os.path.join(path, 'w_mod.json'))
    except:
        sg.popup_ok(err_msg + path, title='Something went wrong.')
    else:
        sg.popup_ok(replace_msg, title='Done')


def_text_ru = '''
Эта программа предназначена замены названий оружия в ZeroSievert на реальные.\n
Также она позволяет:
 - добавить моды для Vintar BC (по умолчанию можно ставить только магазин и прицел);
 - сделать Vintar BC кастомизируемым (при этом происходит замена спрайта оружия т.к. иначе они накладываются друг на друга).
Вся информация хранится в файлах weapon_real.txt и w_mod_real.txt (они должны находится в одной папке с исполняемым файлом).
В эту же папку будут помещены файлы JSON с новыми именами (если опция замены файлов включена, то и скопированы в папку с игрой).\n
При появлении в игре нового оружия и модов можно добавить их в эти txt файлы по принципу 'что поменять' : 'на что поменять'.
Кавычки и двоеточие обязательны !!! 
'''

def_text_eng = '''
This program is designed to replace the names of weapons in Zero Sivert with real ones.\n
It also allows you:
 - to add mods for Vintar BC (by default, you can only install a magazine and scope).
 - to make Vintar BC customizable (this replaces the weapon sprite, because otherwise they overlap each other)
All information is stored in the files weapon_real.txt and w_mod_real.txt (they should be located in the same folder as the executable file).
JSON files with new names will be placed in this folder (if the option to replace files is enabled, then they will be copied to the game folder).\n
When a new weapon or mod appears in the game, you can add them to these files according to the principle 'what to change': 'what to change to'.
Quotation marks and colons are required!!!
'''

rename_rus = 'Переименовать оружие и моды'
rename_eng = 'Rename weapons and mods'
mods_rus = 'Добавить моды для Vintar BC'
mods_eng = 'Add mods to Vintar BC'
all_vintar_rus = 'Включить модификации для Vintar BC'
all_vintar_eng = 'Open all mods for Vintar BC'
exec_rus = 'Выполнить'
exec_eng = 'Execute'
exit_rus = 'Выход'
exit_eng = 'Exit'
replace_rus = 'Заменить файлы в  игре'
replace_eng = 'Change files in game'
replace_msg = '''You have checked "Change files in game" option.
Original files will be renamed to "weapon_ORIG.json" and "w_mod_ORIG.json".
New files will be copied to game directory, no actions needed.
                Have fun !!!  
'''
err_msg = '''Something went wrong.
You have to replace files "weapon.json" and "w_mod.json" manually.
Files with new names are in THIS program folder.\n
Your Zero Sievert folder is: 
'''

layout = [
    [sg.StatusBar('StatusBar : No info' + ' ' * 95, k='-STAT_BAR-')], # Необходимо заполнить для правильного отображения
    [sg.Column([[sg.Checkbox(rename_eng, default=True, k='-RENAME_CB-')],
                [sg.Checkbox(all_vintar_eng, k='-ALLMODSVINTAR_CB-')],
                [sg.HorizontalSeparator()],
                [sg.Checkbox(replace_eng, default=True, k='-CHANGE_FILES-')]]),
     sg.Multiline(def_text_eng, write_only=True, size=(80, 7), k='-TEXT_BOX-')],
    [sg.Button(exec_eng, k='-EXEC-'), sg.Exit(k='-EXIT-'), sg.Push(), sg.Button('Pyc'), sg.Button('Eng')]
]

window = sg.Window('Weapon real names', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '-EXIT-':  # if user closes window or clicks cancel
        break
    if event == 'Eng':
        window['-TEXT_BOX-'].update(value=def_text_eng)
        window['-RENAME_CB-'].update(text=rename_eng)
        window['-ALLMODSVINTAR_CB-'].update(text=all_vintar_eng)
        window['-EXEC-'].update(text=exec_eng)
        window['-EXIT-'].update(text=exit_eng)
        window['-CHANGE_FILES-'].update(text=replace_eng)
        window.set_title('Weapon real names')
    if event == 'Pyc':
        window['-TEXT_BOX-'].update(value=def_text_ru)
        window['-RENAME_CB-'].update(text=rename_rus)
        window['-ALLMODSVINTAR_CB-'].update(text=all_vintar_rus)
        window['-EXEC-'].update(text=exec_rus)
        window['-EXIT-'].update(text=exit_rus)
        window['-CHANGE_FILES-'].update(text=replace_rus)
        window.set_title('Реальные названия оружия')
    if event == '-EXEC-':
        change()

window.close()
