import argparse
import random
import sys
import re
import os

ignoredChars = ['%', '~', ' ', '$', '²']

def parse():
    parser = argparse.ArgumentParser(prog="MALaF", description="Edit Asobo TT files")
    parser.add_argument("-c", "--colorize", metavar="UNIT", choices=["char", "word", "line"], action="store", help="colorize the file")
    parser.add_argument("-C", "--color", metavar="RGB", action="store", default=-1, type=int, help="sets every line to a color specified as RGB with values between 0 and 9")
    parser.add_argument("-r", "--randomize", metavar="UNIT", choices=["word", "line"], nargs="*", help="jumble up the lines/words (can be specified multiple times)")
    parser.add_argument("-i", "--input", metavar="FILE", help="input file (default: default.txt)", nargs="?", const="default.txt", default="default.txt")
    parser.add_argument("-o", "--output", metavar="FILE", help="destination (file/path) (default: out.txt)", nargs="?", const="out.txt", default="out.txt")
    return parser.parse_args()

def check_tt(spline):
    if spline[0] == "TT":
        num = int(spline[1])
        return not 15500 <= num <= 15731 and not num <= 99
    return False

def decolorize(line):
    return re.sub("\^\d\d\d", "", line)

def color_lines(lines, defcolor=None):
    newlines = lines.copy()
    for i, line in enumerate(newlines):
        splitLine = line.split(' ', 2)
        if check_tt(splitLine):
            splitLine[2] = decolorize(splitLine[2])

            if defcolor == None:
                color = str(random.randint(100, 999))
            else:
                color = defcolor

            newlines[i] = 'TT {} "^{}{}^000"'.format(splitLine[1], color, splitLine[2].replace('"', ''))
    return newlines

def color_words(lines):
    newlines = lines.copy()
    for i, line in enumerate(newlines):
        splitLine = line.split(' ', 2)
        if check_tt(splitLine):
            splitLine[2] = decolorize(splitLine[2])
            text = splitLine[2].replace('"', '')
            textList = text.split(' ')

            for wordi, word in enumerate(textList):
                if word not in ignoredChars:
                    color = str(random.randint(100, 999))
                    textList[wordi] = '^{}{}^000'.format(color, word)
                    newlines[i] = 'TT {} "{}"'.format(splitLine[1], ' '.join(textList))
    return newlines

def color_chars(lines):
    newlines = lines.copy()
    for i, line in enumerate(newlines):
        splitLine = line.split(' ', 2)
        if check_tt(splitLine):
            splitLine[2] = decolorize(splitLine[2])
            text = splitLine[2].replace('"', '')
            if len(text) * 8 <= 1020:
                textList = list(text)
                for letterI, letter in enumerate(textList):
                    if letter not in ignoredChars:
                        if textList[letterI - 1] != "%":
                            color = str(random.randint(100, 999))
                            textList[letterI] = '^{}{}^000'.format(color, letter)
                            newlines[i] = 'TT {} "{}"'.format(splitLine[1], ''.join(textList))
            else:
                newlines = color_lines(newlines)
    return newlines

def colorize(lines, unit, color):
    if unit != None:
        if color == -1:
            if unit == "line":
                return color_lines(lines)
            elif unit == "word":
                return color_words(lines)
            elif unit == "char":
                return color_chars(lines)
        else:
            return color_lines(lines, str(color))

    return lines

def randomize(lines, units):
    newlines = lines.copy()
    for unit in units:
        if unit == "line":
            gameLines = []
            for line in newlines:
                splitLine = line.split(' ', 2)
                if splitLine[0] == 'TT':
                    text = splitLine[2].replace('"', '')
                    gameLines.append(text)
            random.shuffle(gameLines)
            for i, line in enumerate(newlines):
                splitLine = line.split(' ', 2)
                if splitLine[0] == 'TT':
                    newlines[i] = 'TT {} "{}"'.format(splitLine[1], gameLines[i-1])

        if unit == "word":
            for i, line in enumerate(newlines):
                splitLine = line.split(' ', 2)
                if check_tt(splitLine):
                    shuffled = splitLine[2].replace('"', '').split(' ')
                    random.shuffle(shuffled)
                    newlines[i] = 'TT {} "{}"'.format(splitLine[1], ' '.join(shuffled))

    return newlines

def main():
    args = vars(parse())
    print(args)
    if args["colorize"] == None and args["randomize"] == None:
        print("no modifier options specified, quitting")
        return

    with open(args["input"], "r", encoding="utf8") as infile:
        lines = infile.read().splitlines()
        lines = colorize(lines, args["colorize"], args["color"])
        lines = randomize(lines, args["randomize"])
        newlines = lines.copy()
        for i in range(len(newlines)):
            newlines[i] += "\n"
        with open(args["output"], "w+", encoding="utf8") as outfile:
            outfile.writelines(newlines)

if __name__ == "__main__":
    main()
