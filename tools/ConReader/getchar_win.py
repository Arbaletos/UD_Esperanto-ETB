from msvcrt import getch
import os

while True:
    key = ord(getch())
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'Keycode: {key}')
    if key == 27: #ESC
        break
    elif key == 13: #Enter
        print('Enter')
    if key == 80: #Down arrow
        print('Down')
    elif key == 72: #Up arrow
        print('Up')