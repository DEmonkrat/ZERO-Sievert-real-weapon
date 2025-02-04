import os
import re
import pandas as pd
import PySimpleGUI as sg

def_path = r'C:\Program Files (x86)\Steam\steamapps\common\ZERO Sievert\ZS_vanilla\gamedata'
path = ''

def find_folder():
    return sg.popup_get_folder('Find your "weapon.json" and "w_mod.json" files folder. Then press "Execute" again.',
                               'Find your "weapon.json" and "w_mod.json" folder')
def check_files(path):
    return os.path.isfile(path)

def change_names(path):
    # Открываем JSON файлы с оружием и модами
    wep_df = pd.read_json(os.path.join(path, 'weapon.json'), typ='series')
    wep_mod_df = pd.read_json(os.path.join(path, 'w_mod.json'), typ='series')
    # Открываем файл weapon_real и w_mod_real.txt с рельаными названиями и делаем из них словари.
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
    # Ищем ЕС (начало слова; в конце без букв, цифр и символов подчеркивания. Например ЕС-74 найдет, а ЕСМ нет)
    reg = r'\b' + string + r'\W'
    for old_name in wep_mod_df['data'].keys():
        if re.search(reg, wep_mod_df['data'][old_name]['basic']['name']):
            wep_mod_df['data'][old_name]['basic']['name'] = wep_mod_df['data'][old_name]['basic']['name'].replace('EC',
                                                                                                                  'AK')
    # Экспорт в JSON файлов с измененными названиями
    wep_df.to_json('weapon.json', orient="index", indent=4)
    wep_mod_df.to_json('w_mod.json', orient="index", indent=4)
    window['-STAT_BAR-'].update('Done', text_color='#c2ffa7')

def add_mods_for_vintar(path):
    # Открываем JSON файлы с оружием и модами
    wep_mod_df = pd.read_json(os.path.join(path, 'w_mod.json'), typ='series')
    # добавляем моды для vintar_bc
    for old_name in wep_mod_df['data'].keys():
        try:
            if 'as_val' in wep_mod_df['data'][old_name]['weapon_mod']['weapon_id']:
                wep_mod_df['data'][old_name]['weapon_mod']['weapon_id'].append('vintar_bc')
        except:
            pass
    # Экспорт в JSON файлов с измененными названиями
    wep_mod_df.to_json('w_mod.json', orient="index", indent=4)
    window['-STAT_BAR-'].update('Done', text_color='#c2ffa7')

def make_vintar_customizable(path):
    # Открываем JSON файлы с оружием и модами
    wep_df = pd.read_json(os.path.join(path, 'weapon.json'), typ='series')
    # кастомизация vintar_bc
    wep_df['data']['vintar_bc']['weapon']['mods'] = wep_df['data']['as_val']['weapon']['mods']
    # замена дефолтного спрайта vintar_bc на стандартный as_val. Иначе получается наложение спрайтов
    wep_df['data']['vintar_bc']['basic']['sprite_inv'] = wep_df['data']['as_val']['basic']['sprite_inv']
    # Экспорт в JSON файлов с измененными названиями
    wep_df.to_json('weapon.json', orient="index", indent=4)
    window['-STAT_BAR-'].update('Done', text_color='#c2ffa7')

def change():
    global path
    if not path:
        if check_files(os.path.join(def_path, 'w_mod.json')) and check_files(os.path.join(def_path, 'weapon.json')):
            window['-STAT_BAR-'].update('Files found', text_color='#c2ffa7')
        else:
            window['-STAT_BAR-'].update('Files not found', text_color='#FFFF00')
            path = find_folder()
    else:
        if check_files(os.path.join(path, 'w_mod.json')) and check_files(os.path.join(path, 'weapon.json')):
            window['-STAT_BAR-'].update('Files found', text_color='#c2ffa7')
            if values['-RENAME_CB-']:
                change_names(path)
            if values['-MODS_CB-']:
                add_mods_for_vintar(path)
            if values['-ALLMODSVINTAR_CB-']:
                make_vintar_customizable(path)
        else:
            window['-STAT_BAR-'].update('Files not found', text_color='#FFFF00')
            path = find_folder()

def_text_ru = '''
Эта программа предназначена замены названий оружия в ZeroSievert на реальные.\n
Также она позволяет:
 - добавить моды для Vintar BC (по умолчанию можно ставить только магазин);
 - сделать Vintar BC кастомизируемым (при этом происходит замена спрайта оружия т.к. иначе они накладываются друг на друга).
Вся информация хранится в файлах weapon_real.txt и w_mod_real.txt (они должны находится в одной папке с исполняемым файлом)
'''
def_text_eng = '''
This program is designed to replace the names of weapons in Zero Sivert with real ones.\n
It also allows you:
 - to add mods for Vintar BC (by default, you can only install a magazine).
 - to make Vintar BC customizable (this replaces the weapon sprite, because otherwise they overlap each other)
All information is stored in the files weapon_real.txt and w_mod_real.txt (they should be located in the same folder as the executable file)
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

layout = [
    [sg.StatusBar('StatusBar : No info', k='-STAT_BAR-')],
    [sg.Column([[sg.Checkbox(rename_eng, default=True, k='-RENAME_CB-')],
              [sg.Checkbox(mods_eng, k='-MODS_CB-')],
              [sg.Checkbox(all_vintar_eng, k='-ALLMODSVINTAR_CB-')]]),
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
        window['-MODS_CB-'].update(text=mods_eng)
        window['-ALLMODSVINTAR_CB-'].update(text=all_vintar_eng)
        window['-EXEC-'].update(text=exec_eng)
        window['-EXIT-'].update(text=exit_eng)
        window.set_title('Weapon real names')
    if event == 'Pyc':
        window['-TEXT_BOX-'].update(value=def_text_ru)
        window['-RENAME_CB-'].update(text=rename_rus)
        window['-MODS_CB-'].update(text=mods_rus)
        window['-ALLMODSVINTAR_CB-'].update(text=all_vintar_rus)
        window['-EXEC-'].update(text=exec_rus)
        window['-EXIT-'].update(text=exit_rus)
        window.set_title('Реальные названия оружия')
    if event == '-EXEC-':
        change()

window.close()