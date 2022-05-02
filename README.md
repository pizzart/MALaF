<h1 align=center>Modifier for Asobo Language Files</h1>
<h6 align=center><a href="https://pizzart.github.io/MALaF.html">Available on the web<a/> (half-borked for the time being)</h6>

## Usage
```
MALaF.py [-h] [-c UNIT] [-C RGB] [-r [UNIT ...]] [-i [FILE]] [-o [FILE]]

options:
  -h, --help            show the help message and exit
  -c UNIT, --colorize UNIT
                        colorize the file
  -C RGB, --color RGB   sets every line to a color specified as RGB with values between 0 and 9
  -r [UNIT ...], --randomize [UNIT ...]
                        jumble up the lines/words (can be specified multiple times)
  -i [FILE], --input [FILE]
                        input file (default: default.txt)
  -o [FILE], --output [FILE]
                        destination (file/path) (default: out.txt)
```

### Notes
Asobo games cannot accept more than ~1020 characters in a single string in a language file, otherwise the game will crash on startup. Because of this some lines might be white when using the --colorize flag

## Contributing
Much appreciated
