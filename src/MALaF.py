from time import sleep
from sys import exit
from traceback import print_exc
from datetime import datetime
import platform
import random
import re
import os

systemRoot = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
paths = []
fileToEdit = ''
filePath = ''
lines = []
ignoreLines = ['END OF ACTION', 'P1', 'ABC', '\{Level\}']
ignoreLetters = ['%', '~', ' ', '$', '²']
running = True

version = '1.2.1'
asobo = "ASOBO LANGUAGE FILE MODIFIER v" + version

welcomeText = """
Make sure you have the language file you want to edit on the current drive / you have the path to the file.
"""

pathQuestion = "Automatic 'search', 'new' file or a path?: "

helpQuestion = "Command or 'general' help? : "

generalHelp = """General help

    Help: get help
    Colorize: colorize the text lines
    Randomize: randomize the text lines
"""

colorizeHelp = """Colorize

    Usage: colorize
    RGB Color / 'rainbow'
    'lines' / 'letters' (to be fixed)

    RGB code example: 909, 000, 356, 888 (colors may be funky, beware)
    Basic colors: Red = 900, Yellow = 980, Green = 090, Blue = 109, Purple = 509, White = 999, Black = 000

    Changes every line's color to a specific color OR
    Randomizes every line's color to a random color
"""

randomizeHelp = """Randomize

    Usage: randomize

    Mixes up every line in the language file
"""

defaultHelp = """Default

    Usage: default
    
    Removes every modification and sets the language file to english (copies a file basically)
"""

quitHelp = """Quit

    Usage: quit

    Quits the script
"""

exceptionText = """--An exception has occurred!--
The exception has been written to 'error_output.txt'.
Report this to https://github.com/PizzArt/MALaF/issues"""

systemInfo = """Platform: {}
Python version: {}
Script version: {}""".format(platform.platform(), platform.python_version(), version)

report = """========Reporting========
Please report this to https://github.com/PizzArt/MALaF/issues. Thanks.
"""

helpTexts = {
    "general": generalHelp,
    "colorize": colorizeHelp,
    "randomize": randomizeHelp,
    "default": defaultHelp,
    "quit": quitHelp,
}

def clearCL():
    os.system('cls' if os.name=='nt' else 'clear')

def stop(time):
    print("Quitting.")
    sleep(time)
    clearCL()
    exit(0)

def search():
    global paths
    global filePath
    for root, dirs, files in os.walk(systemRoot):
        for file in files:
            if re.search("tt[0-9][0-9]\.p[sc]", file, re.IGNORECASE):
                full = os.path.join(root, file)
                paths.append(full)
                print(full + " - " + str(paths.index(full)))
    if len(paths) == 0:
        print("No files were found.")
        stop(1)
    else:
        fileNumber = input("Which file by number do you want to edit?: ")
        try:
            fileNumber = int(fileNumber)
        except:
            print("Failed to convert input to an integer.")
            stop(1)
        else:
            filePath = paths[fileNumber]

def path(path):
    if os.path.isfile(path):
        global filePath
        filePath = path
    elif os.path.isdir(path):
        print("The path you provided is a directory, not file.")
        stop(1)
    else:
        print("The path you provided doesn't exist or has errors.")
        stop(1)

def newFile():
    global filePath
    global fileToEdit
    global lines
    filePath = 'tt01.pc'
    lines = open("files/default.txt", 'r', encoding='utf8').read()
    fileToEdit = open(filePath, 'w+', encoding='utf8')
    fileToEdit.write(lines)
    fileToEdit.close()

def getFile():
    path = input(pathQuestion)
    if path.lower() == 'search':
        search()
    elif path.lower() == 'new':
        newFile()
    else:
        path(path)

def readLines():
    global fileToEdit
    global filePath
    global lines
    fileToEdit = open(filePath, "r", encoding='utf8')
    lines = fileToEdit.read().splitlines()
    fileToEdit.close()

def clean():
    global lines
    useless = ['""', '"$"', '"^940 ^000"', '" "']
    for line in lines:
        splitLine = line.split(' ', 2)
        if splitLine[0] == "TT":
            if splitLine[2] in useless:
                lines.remove(line)

def quitScript():
    global running
    running = False

def decolorize(line):
    return re.sub("\^\d\d\d", "", line)

def colorize():
    global lines
    color = input("Color in RGB or 'rainbow'?: ")
    if color.lower() == "rainbow":
        lineLetter = input("'lines' or 'letters'?: ")
        if lineLetter.lower() == "lines":
            for i, line in enumerate(lines):
                skip = False
                splitLine = line.split(' ', 2)
                if splitLine[0] == "TT":
                    splitLine[2] = decolorize(splitLine[2])
                    for ignored in ignoreLines:
                        if re.search(ignored, line):
                            skip = True
                    if not skip:
                        color = str(random.randint(100, 999))
                        text = splitLine[2].replace('"', '')
                        text = '"^' + color + text + '^000"'
                        lines[i] = 'TT ' + splitLine[1] + ' ' + text
        elif lineLetter.lower() == "letters":
            for i, line in enumerate(lines):
                skip = False
                splitLine = line.split(' ', 2)
                if splitLine[0] == "TT":
                    splitLine[2] = decolorize(splitLine[2])
                    for ignored in ignoreLines:
                        if re.search(ignored, line):
                            skip = True
                    if not skip:
                        text = splitLine[2].replace('"', '')
                        if len(text) * 8 <= 1020:
                            textList = list(text)
                            for letterI, letter in enumerate(textList):
                                if letter not in ignoreLetters:
                                    try:
                                        if textList[letterI - 1] != "%":
                                            color = str(random.randint(100, 999))
                                            textList[letterI] = '^' + color + letter + '^000'
                                    except:
                                        pass
                            lines[i] = 'TT ' + splitLine[1] + ' "' + ''.join(textList) + '"'
                        else:
                            color = str(random.randint(100, 999))
                            text = splitLine[2].replace('"', '')
                            text = '"^' + color + text + '^000"'
                            lines[i] = 'TT ' + splitLine[1] + ' ' + text
        else:
            print("No such command.")
    else:
        try:
            int(color)
        except:
            print("The color code is not an integer.")
        else:
            if len(color) == 3:
                for i, line in enumerate(lines):
                    splitLine = line.split(' ', 2)
                    if splitLine[0] == 'TT':
                        splitLine[2] = decolorize(splitLine[2])
                        for ignored in ignoreLines:
                            if re.search(ignored, line):
                                skip = True
                        if not skip:
                            text = splitLine[2].replace('"', '')
                            text = '"^' + color + text + '^000"'
                            lines[i] = 'TT ' + splitLine[1] + ' ' + text
            else:
                print("Invalid color code (not a 3 number integer)")

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
            lines[i] = splitLine[0] + ' ' + splitLine[1] + ' "' + gameLines[i - 1] + '"'

def default():
    sure = input("Are you sure you want to remove all modifications? [Y/N]: ")
    if sure.lower() == 'y':
        global lines
        lines = open('files/default.txt', 'r', encoding='utf8').read().splitlines()
    clean()

def getHelp():
    help = input(helpQuestion)
    if help in helpTexts:
        print(helpTexts[help])

commands = {
    "quit": quitScript,
    "colorize": colorize,
    "randomize": randomize,
    "default": default,
    "help": getHelp,
}

def getCommand():
    command = input('>>> ')
    if command.lower() in commands:
        commands[command]()
    elif command != "":
        print("No such command.")

def write():
    global fileToEdit
    global filePath
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
                lines[i] = splitLine[0] + ' ' + splitLine[1] + ' ' + toChange[splitLine[1]]
        lines[i] = line + '\n'
    fileToEdit = open(filePath, 'w', encoding='utf8')
    fileToEdit.writelines(lines)
    fileToEdit.close()

def main():
    clearCL()
    print(asobo.center(120))
    print(welcomeText)
    getFile()
    readLines()
    clean()
    clearCL()
    while running:
        getCommand()
    write()
    clean()
    stop(0.25)

try:
    main()
except KeyboardInterrupt:
    print("\nReceived a keyboard interrupt.")
    stop(0.75)
except FileNotFoundError:
    print("While the script was running, the file was removed.")
    stop(1.25)
except:
    currentTime = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    print(exceptionText)
    errorOutput = open('error_output.txt', 'a+', encoding='utf8')
    errorOutput.write("OUTPUT START\n".center(120))
    errorOutput.write("Time: {}\n".format(currentTime))
    errorOutput.write(systemInfo)
    errorOutput.write("\n\nException Start\n".center(120))
    print_exc(file=errorOutput)
    errorOutput.write("Exception End\n\n".center(120))
    errorOutput.write(report)
    errorOutput.write("OUTPUT END\n".center(120))
    errorOutput.close()
    stop(7.5)
