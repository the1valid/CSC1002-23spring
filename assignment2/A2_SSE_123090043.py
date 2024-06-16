'''
step1: Use the prompt_player() to get the size of the sliding puzzle.
step2: Use a list called puzzle to store the solvable puzzle, and find the index of the empty.
step3: Generate and display the initial statement of the game to players. Use len_board**2-2 turtles in total.
step4: Use onclick() to receive the user's input with mouse clicking and run the mouse_click().
step5: Find which tile the player clicked. If the tile is valid to move, then execute the move_tile() to move the turtle
and execute the move_empty() to move the puzzle. Step 5 will be repeated until the puzzle is solved.
step6: When the puzzle is solved, namely the return of is_solved() is true, change the color of the tiles to red.
'''


import random
import turtle


def generate_new_puzzle(len_board: int) -> list:
    """
    Generate a solvable puzzle for players.

    Args:
    len_board (int): the size of the puzzle

    Returns:
    list: the puzzle
    """
    while True:
        puzzle = [i for i in range(len_board ** 2)]
        random.shuffle(puzzle)
        if is_solvable(puzzle) and not is_solved(puzzle):
            return puzzle


def is_solvable(puzzle: list) -> bool:
    """
    Check whether the puzzle is solvable.

    Args:
    puzzle (list): A list containing the numbers in the sliding puzzle.

    Returns:
    bool: If the puzzle is solvable, return True. If the puzzle isn't solvable, return False.
    """
    count = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] > puzzle[j] != 0 and puzzle[i] != 0:
                count += 1
    # n is odd, inverse logarithm is even
    if len_board % 2 == 1:
        return count % 2 == 0
    # n is even, the inverse-order logarithm is parity with the row distance between the initial and final position of
    # the empty tile.
    else:
        empty_dist = abs((len_board ** 2 - puzzle.index(0) - 1) // len_board)
        return (count % 2 == 0) == (empty_dist % 2 == 0)


def is_solved(puzzle: list) -> bool:
    """
    Check whether the puzzle is solved.

    Args:
    puzzle (list): A list containing the numbers in the sliding puzzle.

    Returns:
    bool: If the puzzle is solved, return True. If the puzzle isn't solved, return False.
    """
    ordered_puzzle = [i + 1 for i in range(len_board ** 2)]
    ordered_puzzle[len_board ** 2 - 1] = 0
    if puzzle == ordered_puzzle:
        return True
    else:
        return False


def move_empty(new_empty: int) -> None:
    """
    change the empty in the list of puzzle.

    Args:
    new_empty (int): A list containing the numbers in the sliding puzzle.
    """
    puzzle[empty], puzzle[new_empty] = puzzle[new_empty], puzzle[empty]


'''
GUI Kinley's Puzzle
'''


def prompt_player() -> int:
    """
    Prompt the user to enter the size of the game

    Returns:
    int: The size of the game board
    """
    screen.bgcolor("lightblue")
    screen.title("Kinley's Puzzle")
    game_size = screen.numinput("Kinley's Puzzle", "Puzzle Dimension >", default=3, minval=3, maxval=5)
    try:
        game_size = int(game_size)
    except:
        exit(0)
    return game_size


def create_a_tile(color: str = "blue", sz: int = 4, border: int = 5) -> turtle.Turtle:
    """
    Creates a turtle object configured as a square tile.

    Args:
    color (str): The color of the tile.
    sz (int): The size of the tile.
    border (int): The width of the tile border.

    Returns:
    turtle.Turtle: A turtle object configured as a square tile with the given size and border width.
    """
    t_a_tile = turtle.Turtle('square')
    t_a_tile.up()
    t_a_tile.pencolor(color)
    t_a_tile.color(color)
    t_a_tile.shapesize(sz, sz, border)
    return t_a_tile


def create_a_number(color: str = "black") -> turtle.Turtle:
    """
    Creates a turtle object configured as a number.

    Args:
    color (str): The color of the number.

    Returns:
    turtle.Turtle: A turtle object is going to be configured as a number with given color.
    """
    t_a_number = turtle.Turtle('square')
    t_a_number.color(color)
    return t_a_number


def display_tiles(color: str = "green", space: int = 10) -> tuple:
    """
    Displays a grid of tile and number objects on the screen.

    Args:
    color (str): The color of the number.
    space (int): spacing between tiles in pixels

    Returns:
    tuple:The first list is a list of the Turtle objects created for the tiles.
        The second list is a list of the Turtle objects created for the printed numbers.
    """
    t = create_a_tile()
    t_number = create_a_number()
    tiles_number = []
    sz = 80 + space
    tiles = []
    turtle.delay(0)
    count = 0
    # create tiles and numbers from top to bottom, left to right.
    for cy in range(y_origin, y_origin - sz * len_board, - sz):
        for cx in range(x_origin, x_origin + sz * len_board, sz):
            if count != empty:
                t.color(color)
                t.goto(cx, cy)
                tiles.append(t)
                t = t.clone()
                t_number.penup()
                t_number.goto(cx, cy - 35)
                t_number.pendown()
                t_number.hideturtle()
                # Display number on tile with custom text color
                t_number.write(puzzle[count], align="center", font=("Arial", 48, "normal"))
                tiles_number.append(t_number)
                t_number = t_number.clone()
                count += 1
            else:
                tiles.append(0)
                count += 1
                tiles_number.append(0)
            tile_positions.append([cx, cy])
    t.hideturtle()
    turtle.delay(2)
    return tiles, tiles_number


def move_tile(new_empty: int) -> None:
    """
    move a tile object on the screen.

    Args:
    new_empty (int): new_empty (int): A list containing the numbers in the sliding puzzle.
    """
    tiles_number[new_empty].undo()
    tiles[new_empty].goto(tile_positions[empty])
    tiles[new_empty], tiles[empty] = tiles[empty], tiles[new_empty]
    tiles_number[new_empty].penup()
    tiles_number[new_empty].goto(tile_positions[empty][0], tile_positions[empty][1] - 35)
    tiles_number[new_empty].pendown()
    tiles_number[new_empty].write(puzzle[new_empty], align="center", font=("Arial", 48, "normal"))
    tiles_number[new_empty], tiles_number[empty] = tiles_number[empty], tiles_number[new_empty]


def mouse_click(x: float, y: float) -> None:
    """
        Handles mouse click events during the game.

        Args:
        x (int): the x coordinate of the mouse click.
        y (int): the y coordinate of the mouse click.
    """
    global empty
    turtle.onscreenclick(None)
    for i in range(len_board ** 2):
        if tile_positions[i][0] - 40 <= x <= tile_positions[i][0] + 40 \
                and tile_positions[i][1] + 40 >= y >= tile_positions[i][1] - 40:
            dist_x = abs(empty % len_board - i % len_board)
            dist_y = abs(empty // len_board - i // len_board)
            if dist_x + dist_y == 1:
                move_tile(i)
                move_empty(i)
                empty = i
    if is_solved(puzzle):
        display_tiles(color="red")
    else:
        screen.onclick(mouse_click)


if __name__ == "__main__":
    screen = turtle.Screen()
    tile_positions = []
    len_board = prompt_player()
    puzzle = generate_new_puzzle(len_board)
    empty = puzzle.index(0)
    x_origin, y_origin = -80 - len_board * 20, 100 + len_board * 10
    tiles, tiles_number = display_tiles()
    # Bind mouse click events.
    screen.onclick(mouse_click)
    # Enter the main event loop and wait for user action.
    screen.mainloop()
