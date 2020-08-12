from traceback import print_exc
from datetime import datetime
from time import sleep
import platform
import random
import sys
import re
import os

system_root = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
paths = []
base_path = getattr(sys, '_MEIPASS', os.path.dirname(
    os.path.abspath(__file__)))
default_text_path = os.path.join(base_path, "files/default.txt")
file_to_edit = ''
file_path = ''
lines = []
ignored_patterns = ['END OF ACTION', 'P1', 'ABC', '\{Level\}']
ignored_characters = ['%', '~', ' ', '$', '²']
running = True

version = 'v1.3.1'
asobo = "ASOBO LANGUAGE FILE MODIFIER " + version

welcome_text = """
Make sure you have the language file you want to edit on the current drive / you have the path to the file.
"""

file_question = "Automatic 'search', 'new' file or a path?: "

help_question = "Command or 'general' help? : "

basic_help = """    Basic help

Help: get help
Colorize: colorize each line/character
Randomize: randomize each line
Clean: clean up the file
Default: remove modifications from the file
Quit: save the changes and quit
"""

colorize_help = """    Colorize

RGB color code example: 909, 000, 356, 888
Basic colors: Red = 900, Yellow = 980, Green = 090, Blue = 109, Purple = 509, White = 999, Black = 000

Changes every line's color to a specific color OR
Randomizes each line's color OR
Randomizes each character's color in a line
    [NOTE: if the line is more than about 120 characters, the line will not be colorized, the reason being:
        "Asobo games cannot accept more than ~1020 characters in a single string in a language file,
            otherwise the game will crash on startup."]
"""

randomize_help = """    Randomize

Mixes up every line in the language file
"""

default_help = """    Default
    
Removes every modification and sets the language file to english (copies a file basically)
"""

clean_help = """    Clean

Cleans up the language file (removes unnecessary lines)"""

exception_text = """--An exception has occurred!--
The exception has been written to 'error_output.txt'.
Report this to https://github.com/PizzArt/MALaF/issues"""

frozen = ('Yes' if hasattr(sys, '_MEIPASS') else 'No')

system_info = """Platform: {}
Python version: {}
Script version: {}
Frozen: {}""".format(platform.platform(), platform.python_version(), version, frozen)

report = "Please report this to https://github.com/PizzArt/MALaF/issues. Thanks."

helpTexts = {
    "general": basic_help,
    "colorize": colorize_help,
    "randomize": randomize_help,
    "default": default_help,
    "clean": clean_help,
}


def clear_cmdline():
    os.system('cls' if os.name == 'nt' else 'clear')


def stop(time):
    time *= 10
    time_len = len(str(time))
    while time > -0.1:
        time_str = str(time)
        time_str = '0' * (time_len - len(time_str)) + time_str
        print("Quitting in {}.{}".format(time_str[0], time_str[1].replace('.', '0')), end='\r')
        sleep(0.1)
        time -= 1
    try:
        sys.exit()
    except SystemExit:
        pass


def prompt(cmd, cmd_start):
    return cmd.lower().strip().startswith(cmd_start)


def select_file():
    fileNumber = input("Choose a file to edit by its number: ")
    try:
        fileNumber = int(fileNumber)
    except TypeError:
        print("Failed to convert input to an integer.")
        select_file()
    else:
        global file_path
        file_path = paths[fileNumber]


def search():
    global paths
    for root, dirs, files in os.walk(system_root):
        for file in files:
            if re.search("tt\d\d\.p[sc]", file, re.IGNORECASE):
                full = os.path.join(root, file)
                paths.append(full)
                print(full + " - " + str(paths.index(full)))
    if not paths:
        print("No files were found, let's try again.")
        get_file()
    else:
        select_file()


def set_file_path(path):
    if os.path.isfile(path):
        global file_path
        file_path = path
    elif os.path.isdir(path):
        print("The path you provided is a directory, not file, let's try again.")
        get_file()
    else:
        print("The path you provided doesn't exist or has errors, let's try again.")
        get_file()


def new_file():
    global file_path
    global file_to_edit
    global lines
    file_path = 'tt01.pc'
    lines = open(default_text_path, 'r', encoding='utf8').read()
    file_to_edit = open(file_path, 'w', encoding='utf8')
    file_to_edit.write(lines)
    file_to_edit.close()


def get_file():
    path = input(file_question)
    if prompt(path, 'sea'):
        search()
    elif prompt(path, 'new'):
        new_file()
    else:
        set_file_path(path)


def read_lines():
    global file_path
    global lines
    lines = open(file_path, "r", encoding='utf8').read().splitlines()


def remove_lines(lines, count, useless):
    for line in lines:
        splitLine = line.split(' ', 2)
        if splitLine[0] == 'TT':
            if splitLine[2] in useless:
                lines.remove(line)
                count += 1
    return count


def clean():
    global lines
    useless = ['""', '"$"', '"^940 ^000"', '" "']
    removed_count = 0
    i = 10
    while i:
        removed_count = remove_lines(lines, removed_count, useless)
        i -= 1
    print("Cleaned up {} lines".format(str(removed_count)))


def quit_script():
    global running
    running = False


def decolorize(line):
    return re.sub("\^\d\d\d", "", line)


def color_lines(lines, rainbow, color='000'):
    for i, line in enumerate(lines):
        splitLine = line.split(' ', 2)
        if splitLine[0] == 'TT':
            splitLine[2] = decolorize(splitLine[2])
            if any(re.search(ignored, line) for ignored in ignored_patterns):
                continue
            if rainbow:
                color = str(random.randint(100, 999))
            text = splitLine[2].replace('"', '')
            text = '"^' + color + text + '^000"'
            lines[i] = 'TT ' + splitLine[1] + ' ' + text


def color_letters(lines):
    for i, line in enumerate(lines):
        splitLine = line.split(' ', 2)
        if splitLine[0] == 'TT':
            splitLine[2] = decolorize(splitLine[2])
            if (re.search(ignored, line) for ignored in ignored_patterns):
                continue
            text = splitLine[2].replace('"', '')
            if len(text) * 8 <= 1020:
                textList = list(text)
                for letterI, letter in enumerate(textList):
                    if letter not in ignored_characters:
                        if textList[letterI - 1] != "%":
                            color = str(random.randint(100, 999))
                            textList[letterI] = '^' + \
                                color + letter + '^000'
                            lines[i] = 'TT ' + splitLine[1] + \
                                ' "' + ''.join(textList) + '"'
            else:
                color = str(random.randint(100, 999))
                text = splitLine[2].replace('"', '')
                text = '"^' + color + text + '^000"'
                lines[i] = 'TT ' + splitLine[1] + ' ' + text


def colorize():
    global lines
    color = input("Color in RGB or 'rainbow'?: ")
    if prompt(color, 'rain'):
        symbols_question = input("Colorize by each 'line' or 'character'?: ")
        if prompt(symbols_question, 'lin'):
            color_lines(lines, True)
        elif prompt(symbols_question, 'char'):
            color_letters(lines)
        else:
            print("Invalid selection.")
    else:
        try:
            int(color)
        except:
            print("The color code is not an integer / invalid selection.")
        else:
            color_lines(lines, False, color)


def randomize():
    global lines
    gameLines = []
    for line in lines:
        splitLine = line.split(' ', 2)
        if splitLine[0] == 'TT':
            text = splitLine[2].replace('"', '')
            gameLines.append(text)
    random.shuffle(gameLines)
    for i, line in enumerate(lines):
        splitLine = line.split(' ', 2)
        if splitLine[0] == 'TT':
            lines[i] = splitLine[0] + ' ' + \
                splitLine[1] + ' "' + gameLines[i - 1] + '"'


def default():
    sure = input(
        "Do you want to remove all modifications? [Y]es/[N]o: ")
    if prompt(sure, 'y'):
        global lines
        lines = open(default_text_path, 'r',
                     encoding='utf8').read().splitlines()


def get_help():
    help = input(help_question)
    if help in helpTexts:
        print(helpTexts[help])


commands = {
    "quit": quit_script,
    "colorize": colorize,
    "randomize": randomize,
    "default": default,
    "help": get_help,
    "clean": clean,
}


def get_command():
    command = input('>>> ')
    command = command.lower().strip()
    found_command = [key for key in commands if re.search(key[:3], command)]
    if found_command:
        commands[found_command[0]]()
    elif command != '':
        print("No such command.")


def write():
    global file_to_edit
    global file_path
    global lines
    toChange = {
        "15718": '"END OF ACTION"',
        "15721": '"END OF ACTION"',
        "15730": '"END OF ACTION"',
        "374": '"P1"',
        "1": '"WALL-E"',
        "2": '"WALL-E"',
        "3": '"WALL-E"',
        "4": '"WALL-E"',
        "15500": '"WALL-E"',
    }
    for i, line in enumerate(lines):
        splitLine = line.split(' ', 2)
        if splitLine[0] == 'TT':
            if splitLine[1] in toChange:
                lines[i] = splitLine[0] + ' ' + \
                    splitLine[1] + ' ' + toChange[splitLine[1]]
        lines[i] = line + '\n'
    file_to_edit = open(file_path, 'w', encoding='utf8')
    file_to_edit.writelines(lines)
    file_to_edit.close()


def main():
    clear_cmdline()
    print(asobo)
    print(welcome_text)
    get_file()
    read_lines()
    clear_cmdline()
    while running:
        get_command()
    write()
    stop(0.25)


try:
    main()
except KeyboardInterrupt:
    print("\nReceived a keyboard interrupt.")
    stop(1)
except Exception:
    current_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    print(exception_text)
    error_output = open('error_output.txt', 'a+', encoding='utf8')
    error_output.write("{}\n{}\n\n".format(current_time, system_info))
    print_exc(file=error_output)
    error_output.write("\n\n" + report + "\n\n\n\n")
    error_output.close()
    stop(7.5)
