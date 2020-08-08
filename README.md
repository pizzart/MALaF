# Asobo Language File Modifier
## Modifier for Asobo Games Language Files, written in Python 3.
[Get Python here.](https://www.python.org)

## Usage
When you first start the program, you will be introduced to a command line (might change to a gui in the near future). The script will ask you to either automatically search for a language file, or input a valid path to the file. If you choose to search, the script will try to find any language files on the current drive (Windows) or any folder in the system (Linux, not sure about MacOS, give it a try and let me know)

(don't worry, i don't collect your data lol this is an open source project)

Once the script finds any files, it will show the paths to them. You will have to choose a language file by its number in the list, starting from 1.

After you choose the file, you can start messing with the language file!

### Commands
```
Help: get help
Colorize: colorize the text
Randomize: randomize the lines in the file
Quit: write the changes and quit

You can get descriptive help by using the `help` command.
```

## Understanding the script

###### warning: probably bad code

1. Import required modules.
```
import re
import os
import random
from getpass import getuser
```
2. Initialize the required variables, used later in the script.
```
systemRoot = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
paths = []
fileToEdit = ""
filePath = ""
lines = []
gameLines = []
running = True
user = getuser()
version = "2.0"
```
3. Initialize the string variables, used for help and script questions.
4. Initialize the functions.
    * `stop()`, used to stop the script if something goes wrong
    * `match()`, used to match commands, uses regex
    * `find()`, used to search for the language files, uses `os.walk()` to search
    * `getFile()`, used to set the `filePath` variable
    * `readLines()`, used to set the `fileToEdit` variable and read the lines from the file
    * `clean()`, kinda pointless, removes one unnecessary line from the file, might remove/edit functionality
    * `colorize()`, called when the command is `colorize`
    * `randomize()`, called when the command is `randomize`
    * `command()`, used in the main loop of the script
    * `writeLines()`, used to write the changes to the language file
5. Call the functions.
```
print(asobo.center(100))
print(welcomeText)
getFile()
readLines()
clean()
```
6. Start the main loop.
```
while running:
    command()
```
7. Write the changes once the loop is over.
```
elif match("quit", command):
    global running
    running = False
```

## Contributing
Feel free to contribute to the script, suggest new functions, report bugs if you find any, feedback is much appreciated.