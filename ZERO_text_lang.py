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

replace_done_eng = '''You have checked "Change files in game" option.
Original files will be renamed to "weapon_ORIG.json" and "w_mod_ORIG.json".
New files will be copied to game directory, no actions needed.
                Have fun !!!  
'''
replace_done_rus = '''Вы отметили опцию «Заменить файлы в игре».
Исходные файлы будут переименованы в «weapon_ORIG.json» и «w_mod_ORIG.json».
Новые файлы будут скопированы в каталог игры, никаких действий не требуется.
             Веселитесь !!!!
'''

err_replace_eng = '''Something went wrong.
You have to replace files "weapon.json" and "w_mod.json" manually.
Files with new names are in THIS program folder.\n
Your Zero Sievert folder is: 
'''

err_replace_rus = '''Что-то пошло не так.
Вам необходимо вручную заменить файлы "weapon.json" и "w_mod.json".
Файлы с измененными названиями находятся в папке ЭТОЙ программы.\n
Директория Zero Sievert:
'''

err_rename_eng = '''Files "weapon_ORIG.json" and "w_mod_ORIG.json" already exists in game folder.
It looks like you've already run the program before.
Do you want to delete these files and continue?
'''
err_rename_rus = '''Файлы "weapon_ORIG.json" и "w_mod_ORIG.json" уже существуют в директории игры.
Похоже вы уже запускали программу до этого.
Хотите удалить их и продолжить ?
'''

no_del_eng = '''The files were not deleted.
You need to manually replace the files "weapon.json" and "w_mod.json".
The files with the changed names are in the folder of THIS program.
'''

no_del_rus = '''Файлы не были удалены. 
Вам необходимо вручную заменить файлы "weapon.json" и "w_mod.json".
Файлы с измененными названиями находятся в папке ЭТОЙ программы.
'''


text_box_dict = {
    'default': [def_text_eng, def_text_ru]
}

# Статические элементы интерфейса (кнопки и чекбоксы).
# Ключи словаря совпадают с названиями элементов, поэтому
# можно использовать для цикла
static_chbx_dict = {
    '-RENAME_chbx-': ['Rename weapons and mods',
                      'Переименовать оружие и моды'],
    '-ALLMODSVINTAR_chbx-': ['Open all mods for Vintar BC',
                             'Включить модификации для Vintar BC'],
    '-CHANGE_FILES_chbx-': ['Change files in game',
                            'Заменить файлы в  игре']}

static_btn_dict = {
    '-EXEC_btn-': ['Execute', 'Выполнить'],
    '-EXIT-': ['Exit', 'Выход']
}

title_comon__dict = {
    'default': ['Weapon real names', 'Реальные названия оружия']
}

title_popup__dict = {
    'done': ['Done', 'Выполнено'],
    'wrong_copy': ['Something went wrong.', 'Что-то пошло не так.'],
    'warning': ['Warning', 'Внимание']
}

window_msg_dict = {
    'info_done': [replace_done_eng, replace_done_rus],
    'err_rename': [err_rename_eng, err_rename_rus],
    'err_replace': [err_replace_eng, err_replace_rus],
    'err_del': ['Can`t delete "weapon_ORIG.json" and "w_mod_ORIG.json" file. You can do it manually.',
                'Невозможно удалить файлы "weapon_ORIG.json" и "w_mod_ORIG.json". Вы можете сделать этой вручную'],
    'no_del': [no_del_eng, no_del_rus ],
    'cant_rename': ['Can`t rename "weapon.json" and "w_mod.json". You need to manually replace this files.'
                    'The files with the changed names are in the folder of THIS program.',
                    'Невозможно переименовать. Вам необходимо вручную заменить файлы "weapon.json" и "w_mod.json".'
                    'Файлы с измененными названиями находятся в папке ЭТОЙ программы. ']
}

status_dict = dict(default=['StatusBar : No info', 'Строка состояния : Нет информации'],
                   update=['Starting update', 'Начинаем обновление'],
                   done=['Done', 'Готово'],
                   no_options=['No options to execute', 'Нет выбранных опций'],
                   no_file_mod=['No file "w_mod_real.txt"', 'Нет файла "w_mod_real.txt"'],
                   no_file_weap=['No file "weapon_real.txt"', 'Нет файла "weapon_real.txt"'],
                   found=['Files found', 'Файлы найдены'],
                   not_found=['Files not found. Choose directory and click "Execute" again',
                              'Файлы не найдены. Выберите директорию и нажмите "Выполнить" повторно'])
