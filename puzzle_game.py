'''
Kirby Jiang
CS 5001, Fall 2022
Final Project
'''
from leaderboards import update_leaderboards
from solvable import solvable
from error_log import log_error

import turtle
import random
import os

# declares the screen, two turtle objects, max tile size (with starting_tile)
screen = turtle.Screen()

t = turtle.Turtle()
t.hideturtle()
t.up()
t.speed(0)

t2 = turtle.Turtle()
t2.hideturtle()
t2.up()
t2.speed(0)

MAX_TILE_SIZE = 110
STARTING_TILE = [-(MAX_TILE_SIZE + 4) * 3, (MAX_TILE_SIZE + 4) * 3 - 100]

def get_metadata(filename):
    '''
    Function: get_metadata
        Creates a dictionary with (metadata, data) as the (keys, values)
    Parameters:
        filename -- name of the file to get metadata from
    Returns the metadata dictionary
    '''
    
    with open(filename) as puzzle_file:
        lines = puzzle_file.read().strip().split("\n")
        metadata = {}
        for line in lines:
            line = line.split(": ")
            if line[0].isdigit():
                metadata[int(line[0])] = line[1]
            else:
                metadata[line[0]] = line[1]
    metadata["number"] = int(metadata["number"])

    # adds to the size so the gifs don't overlap the lines drawn
    if int(metadata["size"]) % 2 == 0:
        metadata["size"] = int(metadata["size"]) + 2
    else:
        metadata["size"] = int(metadata["size"]) + 1
    return metadata

def draw_square(myTurtle, side_length, x, y):
    '''
    Function: draw_square
        Draws a square at center (x, y) given side length
    Parameters:
        myTurtle -- turtle object that will draw
        side_length -- side length of square
        x -- x-coordinate of center
        y -- y-coordinate of center
    Does not return anything
    '''
    myTurtle.setpos(x - side_length/2, y + side_length/2)
    myTurtle.down()
    myTurtle.forward(side_length)
    myTurtle.right(90)
    myTurtle.forward(side_length)
    myTurtle.right(90)
    myTurtle.forward(side_length)
    myTurtle.right(90)
    myTurtle.forward(side_length)
    myTurtle.right(90)
    myTurtle.up()
    myTurtle.setpos(x, y)

def draw_leaderboard(metadata, leaderboard_position, thumbnail_position):
    '''
    Function: draw_leaderboard
        Sets up the scores on the leaderboard and the puzzle thumbnail picture
    Parameters:
        metadata -- metadata of current puzzle
        leaderboard_position -- (x, y) coordinates of where to write scores
        thumbnail_position -- (x, y) coordinates of where to put thumbnail gif
    Does not return anything
    '''
    t.pencolor("blue")
    t.setpos(leaderboard_position)
    t.write("Leaders:", move=False, align="left",
            font=("Arial", 16, "normal"))

    # opens leaderboard.txt to access scores
    # if file not found, displays error and appends it to error_log.txt
    try:
        with open("leaderboard.txt") as leaderboard_file:
            leaderboards = [x for x in leaderboard_file.read().strip()\
                .split("Puzzle: ") if x != ""]
            leaderboard = {}
            for each in leaderboards:
                each = [x for x in each.split("\n") if x != ""]
                leaderboard[each[0]] = each[1:]
    except FileNotFoundError:
        t2.setpos(0, 0)
        screen.addshape("Resources/leaderboard_error.gif")
        t2.shape("Resources/leaderboard_error.gif")
        t2.stamp()
        screen.ontimer(undo_twice, 3000)
        log_error("Could not open leaderboard.txt.")

    t.forward(15)
    t.right(90)
    t.forward(25)

    # writes scores, and if there are currently no scores, pass
    try:
        for score in leaderboard[f"{metadata['name']}.puz"]:
            t.write(score, move=False, align="left",
                    font=("Arial", 14, "normal"))
            t.forward(25)
    except KeyError:
        pass
    
    t.left(90)
    t.pencolor("black")

    # adds thumbnail image
    t.setpos(thumbnail_position)
    screen.addshape(metadata["thumbnail"])
    t.shape(metadata["thumbnail"])
    t.stamp()

def update_player_moves(player_moves_position, the_moves):
    '''
    Function: update_player_moves
        Writes how many moves the player has left
    Parameters:
        player_moves_position: (x, y) coordinates of where to write moves made
        the_moves: contains [moves made so far, max moves]
    Does not return anything
    '''
    t2.setpos(player_moves_position)
    t2.forward(25)
    t2.write(f"Player moves: {the_moves[0]} ({the_moves[1] - the_moves[0]} " +
             "left)", move=False, align="left", font=("Arial", 14, "normal"))

def draw_puzzle(metadata, tile_order):
    '''
    Function: draw_puzzle
        Draws the puzzle with the gifs as stamps in the given tile order
    Parameters:
        metadata -- metadata of current puzzle
        tile_order -- order to place gif puzzle pieces
    Returns two lists: the tile order as well as the stamp IDs in order
    '''
    number = metadata["number"]
    size = metadata["size"] # actual size of square being drawn
    square_length = int(metadata["number"] ** (1/2))
    stamp_id = []
    on_tile = 0

    # draws the square given the square side length from metadata
    for i in range(square_length):
        for j in range(square_length):
            draw_square(t, size, STARTING_TILE[0] + (j * (size + 2)),
                        STARTING_TILE[1] - (i * (size + 2)))
            
            screen.addshape(metadata[tile_order[on_tile]])
            t.shape(metadata[tile_order[on_tile]])
            stamp_id.append(t.stamp())
            on_tile += 1
            
    set_blank(metadata, tile_order) # sets turtle to center of blank tile
    return tile_order, stamp_id

def set_blank(metadata, tile_order):
    '''
    Function: set_blank
        Determines (x, y) coordinates of center of blank tile
        and sets turtle position to it
    Parameters:
        metadata -- metadata of current puzzle
        tile_order -- order to place gif puzzle pieces
    Does not return anything
    '''
    number = metadata["number"]
    size = metadata["size"] # actual size of square being drawn
    square_length = int(metadata["number"] ** (1/2))
    t.setpos((STARTING_TILE[0] + \
              ((tile_order.index(number) % square_length)) * \
              (size + 2)),
             (STARTING_TILE[1] - \
              ((tile_order.index(number) // square_length) * \
              (size + 2))))

def determine_possible_moves(metadata, tile_order):
    '''
    Function: determine_possible_moves
        Creates dictionary of [possible moves, index shift] as [keys, value]
    Parameters:
        metadata -- metadata of current puzzle
        tile_order -- order to place gif puzzle pieces
    Returns the dictionary of possible moves
    '''
    number = metadata["number"]
    size = metadata["size"] + 2 # size between centers of squares
    square_length = int(metadata["number"] ** (1/2))
    blank = tile_order.index(number)
    possible_moves = {} # center of possible tiles to move

    # if direction to swap tile is possible, it's added to dict
    if 0 <= (blank - square_length) <= metadata["number"] - 1: # up
        possible_moves[t.xcor(), t.ycor() + size] = -square_length
    if 0 <= (blank + square_length) <= metadata["number"] - 1: # down
        possible_moves[t.xcor(), t.ycor() - size] = square_length
    if (blank % square_length) - 1 != -1: # left
        possible_moves[t.xcor() - size, t.ycor()] = -1
    if (blank % square_length) + 1 != square_length: #right
        possible_moves[t.xcor() + size, t.ycor()] = 1
    return possible_moves

def undo_twice():
    '''
    Function: undo_twice
        Allows the undo function to be called twice, which can be put on timer
    Does not return anything
    '''
    t2.undo()
    t2.undo()

def update_puzzle(metadata, tiles_list, possible_moves, buttons, the_moves,
                  leaderboard_position, player_moves_position,
                  thumbnail_position, player_name):
    '''
    Function: update_puzzle
        Handles all changes to puzzle, including buttons
    Parameters:
        metadata -- metadata of current puzzle
        tiles_list -- two lists returned by draw_puzzle
        possible_moves -- dictionary returned by determine_possible_moves
        buttons -- list of coordinates of all button centers
        the_moves -- contains [player moves made, max moves allowed]
        leaderboard_position -- (x, y) coordinates of where to write scores
        player_moves_position: (x, y) coordinates of where to write moves made
        thumbnail_position -- (x, y) coordinates of where to put thumbnail gif
        player_name -- name of user playing
    Does not return anything
    '''
    number = metadata["number"]
    size = metadata["size"] # actual size of square being drawn
    tile_order = tiles_list[0]
    stamp_id = tiles_list[1]

    def reset():
        '''
        Function: reset
            Resets all puzzle tiles into correct order
        Does not return anything
        '''
        screen.tracer(0, 0)
        new_tiles_list = draw_puzzle(metadata, list(range(1, number + 1)))
        new_possible_moves = determine_possible_moves(metadata,
                                                      new_tiles_list[0])
        screen.tracer(1, 10)
        update_puzzle(metadata, new_tiles_list, new_possible_moves, buttons,
                      the_moves, leaderboard_position, player_moves_position,
                      thumbnail_position, player_name)

    def load():
        '''
        Function: load
            Loads puzzle of user's choice
        Does not return anything
        '''
        # searches for all .puz files in directory
        puzzle_files = [file for file in os.listdir() if file[-4:] == ".puz"]
        load_puzzle_files = ""
        for puzzle in puzzle_files[:10]:
            load_puzzle_files += puzzle + "\n"

        # will only show at most 10 .puz files available
        if len(puzzle_files) > 10:
            t2.setpos(0, 0)
            screen.addshape("Resources/file_warning.gif")
            t2.shape("Resources/file_warning.gif")
            t2.stamp()
            screen.ontimer(undo_twice, 3000)
        user_choice = screen.textinput("Load Puzzle",
                                       "Enter the name of the puzzle you wish"
                                       "to load. Choices are:\n" +
                                       load_puzzle_files)

        # tries to find and load user's puzzle of choice
        try:
            new_metadata = get_metadata(user_choice)
            if new_metadata["number"] not in [4, 9, 16]:
                raise FileNotFoundError
            t.clearstamps()
            t.clear()

            draw_leaderboard(new_metadata, leaderboard_position,
                             thumbnail_position)
            the_moves[0] = 0
            t2.undo()
            update_player_moves(player_moves_position, the_moves)
            
            tile_order = generate_solvable_tile_order(new_metadata["number"])
            
            tiles_list = draw_puzzle(new_metadata, tile_order)
            possible_moves = determine_possible_moves(new_metadata,
                                                      tiles_list[0])
            update_puzzle(new_metadata, tiles_list, possible_moves, buttons,
                          the_moves, leaderboard_position,
                          player_moves_position, thumbnail_position,
                          player_name)
        # if .puz file not found, displays error and logs error
        except FileNotFoundError:
            t2.setpos(0, 0)
            screen.addshape("Resources/file_error.gif")
            t2.shape("Resources/file_error.gif")
            t2.stamp()
            screen.ontimer(undo_twice, 3000)
            log_error(f"File {user_choice} does not exist.")
        
    def show_credits():
        '''
        Function: show_credits
            Shows the game's credits and exits on click
        Does not return anything
        '''
        screen.addshape("Resources/credits.gif")
        t2.shape("Resources/credits.gif")
        t2.stamp()
        screen.exitonclick()
    
    def onclick_check(x, y):
        '''
        Function: onclick_check
            Given click coordinates and determines what to do
        Parameters:
            x -- x-coordinate of clicked location
            y -- y-coordinate of clicked location
        Does not return anything
        '''
        blank = tile_order.index(number)
        # determines if user has clicked on any possible tile moves
        # swaps tile stamps as well as their orders in tile_order and stamp_id
        for move in possible_moves:
            if move[0] - (size / 2) <= x <= move[0] + (size / 2) and \
                move[1] - (size / 2) <= y <= move[1] + (size / 2):
                screen.tracer(0, 0)
                t.clearstamp(stamp_id[(blank + possible_moves[move])])
                t.clearstamp(stamp_id[blank])
                t.shape(metadata[tile_order[blank + possible_moves[move]]])
                t.stamp()
                tile_order[blank], \
                tile_order[blank + possible_moves[move]] = \
                                   tile_order[blank + possible_moves[move]], \
                                   tile_order[blank]
                stamp_id[blank], stamp_id[blank + possible_moves[move]] = \
                                 stamp_id[blank + possible_moves[move]], \
                                 stamp_id[blank]
                set_blank(metadata, tile_order)
                t.shape(metadata[number])
                t.stamp()
                the_moves[0] += 1
                t2.undo()
                update_player_moves(player_moves_position, the_moves)

                # lose condition
                if the_moves[0] > the_moves[1]:
                    t2.setpos(0, 0)
                    screen.addshape("Resources/lose.gif")
                    t2.shape("Resources/lose.gif")
                    t2.stamp()
                    screen.onclick(None)
                    screen.ontimer(show_credits, 3000)
                    return

                # win condition
                if tile_order == sorted(tile_order):
                    # leaderboard is updated
                    update_leaderboards(f"{metadata['name']}.puz",
                                        the_moves[0], player_name)
                    t2.setpos(0, 0)
                    screen.addshape("Resources/winner.gif")
                    t2.shape("Resources/winner.gif")
                    t2.stamp()
                    screen.onclick(None)
                    screen.ontimer(show_credits, 3000)
                    return

                # if user hasn't lost/won yet, updates puzzle
                new_possible_moves = determine_possible_moves(metadata,
                                                              tile_order)
                screen.tracer(1, 10)
                update_puzzle(metadata, tiles_list, new_possible_moves,
                              buttons, the_moves, leaderboard_position,
                              player_moves_position, thumbnail_position,
                              player_name)

        # determines if user has clicked on any of the buttons
        for button in buttons:
            # reset button
            if button == "reset":
                screen.tracer(0, 0)
                current_position = t.pos()
                t.setpos(buttons[button])
                if t.distance(x, y) <= 40:
                    reset()
                else:
                    t.setpos(current_position)
                    screen.tracer(1, 10)
            # load button
            if button == "load":
                if buttons[button][0] - 40 <= x <= buttons[button][0] + 40 \
                    and \
                    buttons[button][1] - 38 <= y <= buttons[button][1] + 38:
                    load()
            # quit button
            if button == "quit":
                if buttons[button][0] - 40 <= x <= buttons[button][0] + 40 \
                    and \
                    buttons[button][1] - 26.5 <= y <= buttons[button][1] \
                        + 26.5:
                    t2.setpos(0, 0)
                    screen.addshape("Resources/quitmsg.gif")
                    t2.shape("Resources/quitmsg.gif")
                    t2.stamp()
                    screen.onclick(None)
                    screen.ontimer(show_credits, 3000)

    screen.onclick(onclick_check)

def draw_everything():
    '''
    Function: draw_everything
        Draws all the game's borders
    Returns list of button coordinates, leaderboard position to write scores
        thumbnail position to place thumbnail gif, and player moves position
        to show number of player moves made
    '''
    t2.pensize(5)

    # initial box drawn
    draw_square(t2, (MAX_TILE_SIZE + 4) * 4.1, -((MAX_TILE_SIZE + 4) * 1.5),
                ((MAX_TILE_SIZE + 4) * 1.5) - 100)

    # moves to and draws leaderboard box
    t2.forward((MAX_TILE_SIZE + 4) * 2.15)
    t2.left(90)
    t2.pencolor("blue")
    t2.down()
    t2.forward(((MAX_TILE_SIZE + 4) * 4.1) / 2)
    leaderboard_position = t2.pos()
    t2.right(90)
    t2.forward(((MAX_TILE_SIZE + 4) * 4.1) / 2)
    thumbnail_position = t2.pos()
    t2.right(90)
    t2.forward((MAX_TILE_SIZE + 4) * 4.1)
    t2.right(90)
    t2.forward(((MAX_TILE_SIZE + 4) * 4.1) / 2)
    t2.right(90)
    t2.forward(((MAX_TILE_SIZE + 4) * 4.1) / 2)
    t2.right(90)
    t2.up()

    # draws bottom box
    t2.setpos((-((MAX_TILE_SIZE + 4) * 1.5) - 
               ((MAX_TILE_SIZE + 4) * 4.1) / 2),
             (((MAX_TILE_SIZE + 4) * 1.5) - 
              ((MAX_TILE_SIZE + 4) * 2.15) - 100))
    t2.pencolor("black")
    t2.down()
    t2.forward((MAX_TILE_SIZE + 4) * 6.25)
    t2.right(90)
    t2.forward(100)
    t2.right(90)
    t2.forward((MAX_TILE_SIZE + 4) * 6.25)
    t2.right(90)
    t2.forward(50)
    player_move_position = t2.pos()
    t2.forward(50)
    t2.right(90)
    t2.up()

    # goes down 50 because button gif sizes are 80 (80/2 + 10)
    t2.right(90)
    t2.forward(50)
    t2.left(90)
    t2.setx((MAX_TILE_SIZE + 4) * 2.7)
    t2.backward(50)

    # adds all the buttons into a list of button coordinates
    buttons = {}
    screen.addshape("Resources/quitbutton.gif")
    t2.shape("Resources/quitbutton.gif")
    t2.stamp()
    buttons["quit"] = t2.pos()
    t2.backward(90)
    screen.addshape("Resources/loadbutton.gif")
    t2.shape("Resources/loadbutton.gif")
    t2.stamp()
    buttons["load"] = t2.pos()
    t2.backward(90)
    screen.addshape("Resources/resetbutton.gif")
    t2.shape("Resources/resetbutton.gif")
    t2.stamp()
    buttons["reset"] = t2.pos()
    
    return buttons, leaderboard_position, \
        thumbnail_position, player_move_position

def show_splash_screen():
    '''
    Function: show_splash_screen
        Displays splash screen, then moves onto main
    Does not return anything
    '''
    screen.addshape("Resources/splash_screen.gif")
    t.shape("Resources/splash_screen.gif")
    t.stamp()
    screen.ontimer(main, 3000)

def generate_solvable_tile_order(number):
    '''
    Function: generate_solvable_tile_order
        Generates and returns guaranteed solvable tile orders
    Parameters:
        number -- number of puzzle tile pieces
    Returns list of tile order
    '''
    # continues to generate tile orders until one is solvable
    while True:
        tile_numbers = list(range(1, number + 1))
        tile_order = []
        while len(tile_numbers) > 0:
            random_number = random.randrange(0, len(tile_numbers))
            tile_order.append(tile_numbers[random_number])
            tile_numbers.remove(tile_numbers[random_number])
        if solvable(number, tile_order):
            print("Random puzzle generated is solvable!")
            return tile_order
        print("Random puzzle generated is unsolvable... Retrying...")
    
    
def main():
    '''
    Function: main
        Initializes required variables and starts game
    Does not return anything
    '''
    t.clear()
    player_name = screen.textinput("CS5001 Puzzle Slide", "Your Name:")
    
    # makes sure user inputs valid number of moves (5-200)
    while True:
        try:
            max_moves = int(screen.textinput("5001 Puzzle Slide - Moves",
                                             "Enter the number of moves " + \
                                             "(chances) you want (5-200)?"))
            if 5 <= max_moves <= 200:
                break
        except (ValueError, TypeError):
            pass
    the_moves = [0, max_moves]

    # default puzzle is mario.puz
    metadata = get_metadata("mario.puz")
    buttons, leaderboard_position, thumbnail_position, player_moves_position \
        = draw_everything()
    leaderboard = draw_leaderboard(metadata, leaderboard_position,
                                   thumbnail_position)
    update_player_moves(player_moves_position, the_moves)

    tile_order = generate_solvable_tile_order(metadata["number"])
        
    tiles_list = draw_puzzle(metadata, tile_order)
    possible_moves = determine_possible_moves(metadata, tiles_list[0])
    update_puzzle(metadata, tiles_list, possible_moves, buttons, the_moves,
                  leaderboard_position, player_moves_position,
                  thumbnail_position, player_name)

if __name__ == "__main__":
    show_splash_screen()
