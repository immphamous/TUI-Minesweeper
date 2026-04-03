# TUI-Minesweeper
A recreation of minesweeper made in python. Z is to click the current block and C is to toggle the flag. Arrow keys for movement.

ℹ️ This code could be improved with just setting the console cursor coordinates instead of clearing and redrawing the screen.
Also it was made for linux, but I'm sure you can easy port it by running `os.system("cls")` instead of `os.system("clear")`, and maybe changing mmlib to do windows read_key instead of linux.
