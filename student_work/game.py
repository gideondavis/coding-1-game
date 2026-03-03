
# The goals for this phase include:
# - Pick out some icons for your game
# - Establish a starting position for each icon
# - Pick a size for your playing space
# - Print your playing space with starting position of each icon

# To make this work, you may have to type this into the terminal --> pip install curses
import curses
import random
import time

game_data = {
    'width': 15,
    'height': 15,
    'player': {"x": 14, "y": 14, "score": 0, "energy": 10, "max_energy": 10},
    'eagle_pos': {"x": 7, "y": 0},
    'obstacles': [
        {"x": 1, "y": 13},
        {"x": 2, "y": 13},
        {"x": 3, "y": 13},
        {"x": 6, "y": 13},
        {"x": 7, "y": 13},
        {"x": 8, "y": 13},
        {"x": 11, "y": 13},
        {"x": 12, "y": 13},
        {"x": 13, "y": 13},
    ],

    # ASCII icons
    'turtle': "🛸",
    'eagle_icon': "👾",
    'obstacle': "🟩",
    'empty': "  "
}

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.clear()
    for y in range(game_data['height']):
        row = ""
        for x in range(game_data['width']):
            # Player
            if x == game_data['player']['x'] and y == game_data['player']['y']:
                row += game_data['turtle']
            # Eagle
            elif x == game_data['eagle_pos']['x'] and y == game_data['eagle_pos']['y']:
                row += game_data['eagle_icon']
            # Obstacles
            elif any(o['x'] == x and o['y'] == y for o in game_data['obstacles']):
                row += game_data['obstacle']
            else:
                row += game_data['empty']
            
        stdscr.addstr(y, 0, row, curses.color_pair(1))

    stdscr.refresh()

def move_player(key):
    x = game_data['player']['x']
    y = game_data['player']['y']

    new_x, new_y = x, y
    key = key.lower()

    if key == "a" and x > 0:
        new_x -= 1
    elif key == "d" and x < game_data['width'] - 1:
        new_x += 1
    else:
        return  # Invalid key or move off board

    # Check for obstacles
    if any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
        return

    # Update position and increment score
    game_data['player']['x'] = new_x
    game_data['player']['y'] = new_y

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key:
            if key.lower() == "q":
                break

            move_player(key)
            draw_board(stdscr)

def move_eagle():
    directions = [(0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    ex, ey = game_data['eagle_pos']['x'], game_data['eagle_pos']['y']

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy
        if 0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']:
            if not any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
                game_data['eagle_pos']['x'] = new_x
                game_data['eagle_pos']['y'] = new_y
                break

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key:
            if key.lower() == "q":
                break
            move_player(key)

            move_eagle()


            draw_board(stdscr)
            time.sleep(0.2)
curses.wrapper(main)
