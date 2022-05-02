<h1 align=center>Modifier for Asobo Language Files</h1>
<h6 align=center><a href="https://pizzart.github.io/MALaF.html">Available on the web<a/> (half-borked for the time being)</h6>

## Usage
When you first start the program, you will be introduced to a command line (might change to a gui in the near future). The script will ask you to either automatically search for a language file, create a new file, or input a valid path to the file. If you choose to search, the script will try to find any language files on the current drive (Windows) or any folder in the system (Linux, not sure about MacOS, give it a try and let me know). Once the script finds any files, it will show the paths to them. You will have to choose a language file by its number in the list, starting from 0.

After you choose the file, you can start messing with the language file!

You can get help by using the "help" command.

### Notes
Asobo games cannot accept more than ~1020 characters in a single string in a language file, otherwise the game will crash on startup.

## Building the binary
Prerequisites: pyinstaller (`pip install pyinstaller --user`)
1. Get the repository: `git clone https://github.com/pizzart/MALaF` or download ZIP
2. Use PyInstaller: `pyinstaller --clean -n MALaF -F ./src/MALaF.py`

The executable should be in the `dist` folder

## Contributing
Much appreciated
