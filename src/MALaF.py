import re
import os
import random
from getpass import getuser

systemRoot = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
paths = []
fileToEdit = ""
filePath = ""
lines = []
gameLines = []
running = True
user = getuser()
version = "1.1"

asobo = "//ASOBO LANGUAGE FILE MODIFIER v{}\\\\".format(version)

welcomeText = """
Make sure you have WALL-E installed / disc image unpacked in a folder or you have the path to the file you want to change.
//use 'help' to get help"""

pathQuestion = """
Do you want the script to ('search') for the file OR
Do you want to provide a (*path to the file*)?: """

helpQuestion = "(*command*) for help for a command or ('general') for general help: "

generalHelp = """General help

    Help: get help
    Colorize: colorize the text lines
    Randomize: randomize the text lines"""

colorizeHelp = """Colorize

    Usage: colorize
    RGB Color / 'rainbow'
    'lines' / 'letters' (to be fixed)

    RGB code example: 909, 000, 356, 888 (colors may be funky, beware)
    Basic colors: Red = 900, Yellow = 980, Green = 090, Blue = 109, Purple = 509, White = 999, Black = 000

    Changes every line's color to a specific color OR
    Randomizes every line's color to a random color"""

randomizeHelp = """Randomize

    Usage: randomize

    Mixes up every line in the language file"""

quitHelp = """Quit

    Usage: quit

    Quits the script (duh)."""

def stop():
    input("Exiting, try harder next time, " + user)
    quit()

def match(pattern, string):
    return re.match(pattern, string, re.IGNORECASE)

def find():
    global paths
    for root, dirs, files in os.walk(systemRoot):
        for file in files:
            if re.match("tt\d\d\.", file):
                full = os.path.join(root, file)
                print(full)
                paths.append(full)
    return paths

def getFile():
    global fileToEdit
    global filePath
    path = input(pathQuestion)
    if match("search", path):
        find()
        if len(paths) == 0:
            print("No files were found, " + user)
            stop()
        else:
            fileNumber = input("Which file by number (starting from 0) do you want to edit?: ")
            try:
                fileNumber = int(fileNumber)
            except:
                print("Failed to convert input to an integer, " + user)
                stop()
            else:
                fileToEdit = paths[fileNumber]
                filePath = paths[fileNumber]
    else:
        if os.path.isfile(path):
            fileToEdit += path
            filePath += path
        elif os.path.isdir(path):
            print("The path you provided is a directory, not file, " + user)
            stop()
        else:
            print("The path you provided probably doesn't exist, " + user)
            stop()

def readLines():
    global fileToEdit
    global filePath
    global lines
    fileToEdit = open(filePath, "r")
    lines = fileToEdit.read().splitlines()
    fileToEdit.close()

def clean():
    global lines
    for line in lines:
        splitLine = line.split(" ", 2)
        if splitLine[0] == "TT":
            if splitLine[2] == '""' or splitLine[2] == '"$"' or splitLine[2] == '"^940 ^000"':
                lines.remove(line)

def colorize():
    global lines
    color = input("Color in RGB or 'rainbow'?: ")
    if match("rainbow", color):
        lineLetter = input("'lines' or 'letters'?: ")
        if match("lines", lineLetter):
            for i, line in enumerate(lines):
                splitLine = line.split(" ", 2)
                if splitLine[0] == "TT":
                    color = str(random.randint(100, 999))
                    text = splitLine[2].replace('"', '')
                    text = '"^' + color + text + '^000"'
                    lines[i] = "TT " + splitLine[1] + " " + text
        elif match("letters", lineLetter):
            print("oops sorry {} i will fix that in the next update ok im too lazy".format(user))
            """
            for i, line in enumerate(lines):
                splitLine = line.split(" ", 2)
                if splitLine[0] == "TT":
                    text = splitLine[2].replace('"', '')
                    textList = list(text)
                    print(textList)
                    for i, letter in enumerate(textList):
                        color = str(random.randint(100, 999))
                        textList[i] = '^' + color + letter + '^000'
                    print(textList)
                    lines[i] = "TT " + splitLine[1] + ' "' + "".join(textList) + '"'
                    print(lines[i])
            """
        else:
            print("bruh you dum " + user)
            
    else:
        try:
            int(color)
        except:
            print("The color code is not an integer, " + user)
        else:
            if len(color) == 3:
                for i, line in enumerate(lines):
                    splitLine = line.split(" ", 2)
                    if splitLine[0] == "TT":
                        text = splitLine[2].replace('"', '')
                        text = '"^' + color + text + '^000"'
                        lines[i] = "TT " + splitLine[1] + " " + text
            else:
                print("Invalid color code (the color code you provided is not a 3 number integer), " + user)

def randomize():
    global lines
    global gameLines
    for line in lines:
        splitLine = line.split(" ", 2)
        if splitLine[0] == "TT":
            text = splitLine[2].replace('"', '')
            gameLines.append(text)
    random.shuffle(gameLines)
    for i, line in enumerate(gameLines):
        if line == "END OF ACTION":
            gameLines[i] = "cheese"
    for i, line in enumerate(lines):
        splitLine = line.split(" ", 2)
        if splitLine[0] == "TT":
            eoa = splitLine[0] + " " + splitLine[1] + ' "END OF ACTION"'
            cheese = splitLine[0] + " " + splitLine[1] + ' "cheese2 electric boogaloo"'
            if splitLine[1] == "15718":
                lines[i] = eoa
            elif splitLine[1] == "15721":
                lines[i] = eoa
            elif splitLine[1] == "15730":
                lines[i] = eoa
            elif splitLine[1] == "374":
                lines[i] = cheese
            else:
                lines[i] = splitLine[0] + " " + splitLine[1] + ' "' + gameLines[i-1] + '"'

def command():
    command = input("CMD: ")
    if match("help", command):
        help = input(helpQuestion)

        if match("general", help):
            print(generalHelp)
        elif match("colorize", help):
            print(colorizeHelp)
        elif match("randomize", help):
            print(randomizeHelp)
        elif match("quit", help):
            print(quitHelp)
    
    elif match("colorize", command):
        colorize()
    elif match("randomize", command):
        randomize()
    elif match("quit", command):
        global running
        running = False
    else:
        print("No such command, " + user)

def writeLines():
    global fileToEdit
    global filePath
    global lines
    for i, line in enumerate(lines):
        lines[i] = line + "\n"
    fileToEdit = open(filePath, "w")
    fileToEdit.writelines(lines)
    fileToEdit.close()

print(asobo.center(100))
print(welcomeText)
getFile()
readLines()
clean()
while running:
    command()
writeLines()