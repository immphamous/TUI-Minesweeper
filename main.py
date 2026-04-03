import random, mmlib, os

WIDTH = 16
HEIGHT = 16
MINE_AMOUNT = 20

grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
covered = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
flagged = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

pos_x = int(WIDTH/2)
pos_y = int(HEIGHT/2)



def populate(amount, id):
    i = amount
    while i > 0:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if grid[y][x] == 0:
            i -= 1
            grid[y][x] = id

populate(MINE_AMOUNT, 1)

def count_mines(x, y):
    count = 0
    for xx in range(-1, 2):
        for yy in range(-1, 2):
            if in_range(x + xx, y + yy):
                index = grid[yy + y][xx + x]
                if index == 1:
                    count += 1
    return count

def is_covered(x, y):
    return covered[y][x] == 1
def is_flagged(x, y):
    return flagged[y][x] == 1

def set_range(x, y, id):
    for xx in range(-1, 2):
        for yy in range(-1, 2):
            if in_range(x + xx, y + yy):
                grid[y + yy][x + xx] = id

def in_range(x, y):
    if x < 0 or y < 0:
        return False
    if x >= WIDTH or y >= HEIGHT:
        return False
    return True

def uncover(x, y, stop=False):
    if not is_flagged(x, y) and not is_mine(x, y):
        covered[y][x] = 0

    if not stop and not count_mines(x, y) > 0:
        for xx in range(-1, 2):
            for yy in range(-1, 2):
                if in_range(x + xx, y + yy):
                    if is_covered(xx + x, yy + y):
                        if count_mines(xx + x, yy + y) == 0:
                            uncover(xx + x, yy + y)
                        else:
                            uncover(xx + x, yy + y, stop=True)

def flag(x, y):
    flagged[y][x] = 1 - flagged[y][x]

def is_mine(x, y):
    return grid[y][x] == 1

def render():
    print("+" + "-" * (WIDTH * 2 + 1) + "+")
    for y in range(HEIGHT):
        print("| ", end="")
        for x in range(WIDTH):


            tile = grid[y][x]
            count = count_mines(x, y)
            
            if is_covered(x, y):
                if is_flagged(x, y):
                        print(f"⚑", end="")
                else:
                    if pos_x == x and pos_y == y:
                        print(f"■", end="")
                    else:
                        print(f"□", end="")
            else:
                if tile == 0:
                    if count != 0:
                        print(f"{count}", end="")
                    else:
                        print(f".", end="")
                else:
                    print(f"!", end="")
            
            if x == pos_x and y == pos_y and not is_covered(x, y):
                print("<", end="")
            else:
                print(" ", end="")
        print("|")
    print("+" + "-" * (WIDTH * 2 + 1) + "+")

def flagged_all_correctly():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if is_flagged(x, y) and not is_mine(x, y):
                return False
            if not is_flagged(x, y) and is_mine(x, y):
                return False
    return True

def draw():
    os.system("clear")
    render()

first_time_uncovering = True

while True:
    draw()
    command = mmlib.read_key()
    if command == "D": pos_x -= 1
    if command == "C": pos_x += 1
    if command == "A": pos_y -= 1
    if command == "B": pos_y += 1
    
    pos_x = mmlib.clamp(pos_x, 0, WIDTH - 1)
    pos_y = mmlib.clamp(pos_y, 0, HEIGHT - 1)
    
    if command == "z":
        if first_time_uncovering:
            set_range(pos_x, pos_y, 0)
            first_time_uncovering = False
        uncover(pos_x, pos_y)
        if is_mine(pos_x, pos_y):
            draw()
            print("YOU ARE DEAD. NOT BIG SUPRISE.")
            break
    if command == "c":
        if is_covered(pos_x, pos_y):
            flag(pos_x, pos_y)
        if flagged_all_correctly():
            draw()
            print("YOU WON. BIG SUPRISE.")
            break
