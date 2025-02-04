import os
import PySimpleGUI as sg

def_path = r'D:\Program Files (x86)\Steam\steamapps\common\ZERO Sievert\ZS_vanilla\gamedata'
path = ''
def check_files(path):
    return os.path.isfile(path)

def change_name():
    global path
    if not path:
        if check_files(os.path.join(def_path, 'w_mod.json')) and check_files(os.path.join(def_path, 'weapon.json')):
            window['-STAT_BAR-'].update('Files found', text_color='#c2ffa7')
        else:
            window['-STAT_BAR-'].update('Files not found', text_color='#FFFF00')
            path = sg.popup_get_folder('Find your weapon.json and w_mod.json files folder')
    else:
        if check_files(os.path.join(path, 'w_mod.json')) and check_files(os.path.join(path, 'weapon.json')):
            window['-STAT_BAR-'].update('Files found', text_color='#c2ffa7')
        else:
            window['-STAT_BAR-'].update('Files not found', text_color='#FFFF00')
            path = sg.popup_get_folder('Find your weapon.json and w_mod.json files folder')

def_text_ru = '''
Эта программа предназначена замены названий оружия в ZeroSievert на реальные.\n
Также она позволяет:
 - добавить моды для Vintar BC (по умолчанию можно ставить только магазин);
 - сделать доступными все модификации для Vintar BC (при этом происходит замена спрайта оружия т.к. иначе они накладываются друг на друга).
Вся информация хранится в файлах weapon_real.txt и w_mod_real.txt (они должны находится в одной папке с исполняемым файлом)
'''
def_text_eng = '''
This program is designed to replace the names of weapons in Zero Sivert with real ones.\n
It also allows you:
 - to add mods for Vintar BC (by default, you can only install a magazine).
 - to make all modifications available for Vintar BC (this replaces the weapon sprite, because otherwise they overlap each other)
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
        change_name()

window.close()