"""
You can click anywhere in the screen to start the game. Then use the right, left, up, and down to control
the snake's move. Try to avoid collide into the monster before consume all the food.
The program performs the following steps:
step1: Create screen, and show the introduction.Create snake, monsters, and store the position of snake,
        turtle of monsters in distinct lists. Detect click motion.
step2: Use onkey() to detect the input, and change the moving direction of the snake. At the meantime,
        by using the g_screen.ontimer(), move the snake, food, monster and calculate the time at the same time.
step3: Each time the snake move detect the consumption of food. Each time the monster move, detect whether the
        monster collides into the snake's tail.
step4: If the snake eats all of the food, or the monster collides into the snake's head, the game is over,
        and a corresponding subtitle will appear on the screen.
"""
import turtle
import random
from functools import partial

g_screen = None
g_snake = None  # snake's head
g_monster = None
g_snake_sz = 5  # size of the snake's tail
g_intro = None
g_key_pressed = None
g_status = None
g_total_time = 0
g_start_game = False
g_snake_items = []
g_food_items = []
g_monster_items = []
g_movement = "Paused"
g_contact = 0
g_food_consumption = 0
g_game_state = True

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"
FONT_INTRO = ("Arial", 18, "normal")
FONT_STATUS = ("Arial", 17, "normal")
TIMER_SNAKE = 200  # refresh rate for snake
SZ_SQUARE = 20  # square size in pixels
FOOD_NUMBER = 5

DIM_PLAY_AREA = 500
DIM_STAT_AREA = 60
DIM_MARGIN = 30

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
    "Up", "Down", "Left", "Right", "space"
former_key_pressed = None

HEADING_BY_KEY = {KEY_UP: 90, KEY_DOWN: 270, KEY_LEFT: 180, KEY_RIGHT: 0}


def create_turtle(x: int, y: int, color="red", border="black") -> turtle.Turtle:
    """
    Creates a new turtle object with the specified position, color, and border.

    Args:
        x (int): The x-coordinate of the turtle's initial position.
        y (int): The y-coordinate of the turtle's initial position.
        color (str, optional): The color of the turtle's body. Defaults to "red".
        border (str, optional): The color of the turtle's border. Defaults to "black".

    Returns:
        turtle.Turtle: The newly created turtle object.
    """
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x, y)
    return t


def configure_play_area() -> turtle.Screen:
    """
    Configures the play area for the snake game,
    including the motion border, status border,
    introduction text, and status text.
    The motion border and status border are based on square shape
    resized according to the specified dimensions.

    Returns:
        tuples: A tuple containing the introduction text turtle and
        the status text turtle.
    """

    # motion border
    m = create_turtle(0, 0, "", "black")
    sz = DIM_PLAY_AREA // SZ_SQUARE
    m.shapesize(sz, sz, 3)
    m.goto(0, -DIM_STAT_AREA // 2 + 10)  # shift down half the status

    # status border
    s = create_turtle(0, 0, "", "black")
    sz_w, sz_h = DIM_STAT_AREA // SZ_SQUARE, DIM_PLAY_AREA // SZ_SQUARE
    s.shapesize(sz_w, sz_h, 3)
    s.goto(0, DIM_PLAY_AREA // 2 + 10)  # shift up half the motion

    # turtle to write introduction
    intro = create_turtle(-200, 0)
    intro.hideturtle()
    intro.write("Snake by A\n\n" +
                "Click any where to start,have fun!\n\n",
                font=FONT_INTRO)

    # turtle to write status
    status = create_turtle(0, 0, "", "black")
    status.hideturtle()
    status.goto(-230, s.ycor() - 20)

    return intro, status


def configure_screen() -> turtle.Screen:
    """
    Configures the Turtle screen for the snake game,
    the screen width and height are calculated based
    on the play area, status bar and margin.

    Returns:
        turtle.Screen: The configured Turtle screen.
    """
    s = turtle.Screen()
    s.tracer(0)  # disable auto screen refresh, 0=disable, 1=enable
    s.title("Snake by A")
    w = DIM_PLAY_AREA + DIM_MARGIN * 2
    h = DIM_PLAY_AREA + DIM_MARGIN * 2 + DIM_STAT_AREA
    s.setup(w, h)
    s.mode("standard")
    return s


def update_status() -> None:
    """
    Updates the status display on the screen with
    the current key press and snake tail length.
    """
    if not g_game_state:
        return
    g_status.clear()
    if g_movement == "Move" and g_key_pressed is None:
        motion = "Paused"
    elif g_movement == "Paused":
        motion = "Paused"
    else:
        motion = g_key_pressed
    status = f'Contact-{g_contact}    Time-{g_total_time}    Motion-{motion}'
    g_status.write(status, font=FONT_STATUS)
    g_screen.update()


def total_time() -> None:
    """
    Return to write the total time at the upper status area.

    Will be returned every one second.

        e.g. Time: 2
    """
    if not g_game_state:
        return
    global g_total_time

    if g_start_game is True:
        g_total_time += 1
    update_status()
    turtle.ontimer(total_time, 1000)


def on_arrow_key_pressed(key: str) -> None:
    """
    Handles the user's arrow key press event and
    updates the global `g_key_pressed` variable with the pressed key.
    It then calls the `update_status()` function to update
    the status display on the screen.

    Args:
        key (str): The key that was pressed, one of 'Up', 'Down', 'Left', or 'Right'.
    """

    global g_key_pressed, former_key_pressed, g_movement
    g_key_pressed = key
    if g_movement == "Paused":
        g_movement = "Move"
        former_key_pressed = g_key_pressed
    former_key_pressed = g_key_pressed
    g_key_pressed = key
    update_status()


def if_paused() -> None:
    """
    Decide the movement (move or pause) when the spaced is slicked.

    """
    global g_key_pressed, former_key_pressed, g_movement
    if g_movement == "Paused":
        g_key_pressed = former_key_pressed
        g_movement = "Move"
        update_status()
    else:
        g_movement = "Paused"
        update_status()


def movable(heading: int, item: turtle.Turtle) -> bool:
    """
    Detect whether the snake can move to the certain place and doesn't collide into the Margin.

     Args:
        heading (int): The direction of the turtle want to go. 0,1,2,3,
                        represent for right, up, left, down respectively.
        item (turtle.Turtle): Item represent for the turtle of the snake's head.

    """
    # if heading is up or right, which the value of coordinate will increase, then forward is positive.
    # if heading is down or left, which the value of coordinate will decrease, then forward is negative.
    forward = 1.5 - heading
    # direction is the sign of forward -1 or +1.
    direction = int(forward / abs(forward))
    x = int(item.pos()[0] + (heading + 1) % 2 * SZ_SQUARE * direction)
    y = int(item.pos()[1] + heading % 2 * SZ_SQUARE * direction)
    if -DIM_PLAY_AREA // 2 <= x <= DIM_PLAY_AREA // 2 and \
            -DIM_PLAY_AREA // 2 - 20 <= y <= DIM_PLAY_AREA // 2 - 20:
        return True
    else:
        return False


def on_timer_snake() -> None:
    """
    Advances the snake's movement on a timer. This function is called repeatedly
    by the Turtle screen's `ontimer` method to update the snake's position.

    If no key has been pressed, the function simply schedules itself to be called
    again after the `TIMER_SNAKE` interval. Otherwise, it performs the following steps:

    1. Clones the snake's head as a new body segment by setting the color to `COLOR_BODY`
        and stamping it on the screen.
    2. Sets the snake's color back to `COLOR_HEAD`.
    3. Advances the snake's position by setting the heading based
        on the last key pressed (`g_key_pressed`),
        moving the snake forward by `SZ_SQUARE` units,
        and store the snake's position in a list.
    4. If the number of stamped segments exceeds the current snake size (`g_snake_sz`),
        removes the last segment by clearing the oldest stamp.
    5. detect whether the snake consumes food, if it consumes
        food then slow down the snake and change the snake's size.
    6. Updates the Turtle screen to reflect the changes.
    7. Schedules the function to be called again after the `TIMER_SNAKE` interval.
    """
    if not g_game_state:
        return
    if (g_key_pressed is None) or g_movement == "Paused":
        g_screen.ontimer(on_timer_snake, TIMER_SNAKE)
        return
    heading = (HEADING_BY_KEY[g_key_pressed]) // 90

    if movable(heading, g_snake):
        # Clone the head as body
        g_snake.color(*COLOR_BODY)
        g_snake.stamp()
        g_snake.color(COLOR_HEAD)

        # Advance snake
        g_snake.setheading(HEADING_BY_KEY[g_key_pressed])
        g_snake.forward(SZ_SQUARE)
        g_snake_items.append(g_snake.pos())
        consume_food()
        global g_food_consumption

        # Shifting or extending the tail.
        # Remove the last square on Shifting.

        if len(g_snake.stampItems) > g_snake_sz:
            g_snake.clearstamps(1)
            g_snake_items.pop(0)
    if len(g_snake.stampItems) == 20:
        game_state("Winner !!")

    g_screen.update()
    delay = 200
    if g_food_consumption > 0:
        g_food_consumption -= 1
        g_screen.ontimer(on_timer_snake, TIMER_SNAKE + delay)
    else:
        g_screen.ontimer(on_timer_snake, TIMER_SNAKE)


def on_timer_monster() -> None:
    """
    Advances the monster's movement on a timer.
    This function is called repeatedly
    by the Turtle screen's `ontimer` method to update the monster's position.

    The function performs the following steps:

    1. Randomly choice the monster(s) to move.
    2. Calculates the heading for the monster to move towards the snake,
        snapping to the nearest 45-degree angle.
    3. Sets the monster's heading to the calculated value.
    4. Moves the monster forward by `SZ_SQUARE` units,
        and detect whether the monster will contact with the snake's tail.
    5. Updates the Turtle screen to reflect the changes.
    6. Schedules the function to be called again after a random delay
        between `TIMER_SNAKE-200` and `TIMER_SNAKE+500` milliseconds.
    """
    if not g_game_state:
        return
    number = random.randint(0, 3)
    move_monster = random.sample(g_monster_items, number)
    for monster in move_monster:

        angle = monster.towards(g_snake)
        qtr = angle // 45  # (0,1,2,3,4,5,6,7)
        heading = qtr * 45 if qtr % 2 == 0 else (qtr + 1) * 45
        if movable(heading, monster):
            monster.setheading(heading)
            monster.forward(SZ_SQUARE)
            x, y = monster.pos()
            detect_contact(x, y)
        g_screen.update()
    delay = random.randint(TIMER_SNAKE - 200, TIMER_SNAKE + 500)
    g_screen.ontimer(on_timer_monster, delay)


def food_item() -> None:
    """
    Create certain food with the designed number.
    """
    for i in range(FOOD_NUMBER):
        x_position = -DIM_PLAY_AREA // 2 + random.randint(1, -1 + 500 // 20) * 20 + 10
        y_position = -DIM_PLAY_AREA // 2 + random.randint(1, -1 + 500 // 20) * 20 - 20
        g_food = turtle.Turtle('square')
        g_food.color("black")
        g_food.penup()
        g_food.goto(x_position, y_position)
        g_food.pendown()
        g_food.write(i + 1, align="center", font=("Arial", 10, "normal"))
        g_food_items.append([i + 1, g_food])
        g_food.hideturtle()


def on_timer_food() -> None:
    """
    Advances the food's movement on a timer.
    This function is called repeatedly
    by the Turtle screen's `ontimer` method to update the food's position.

    The function performs the following steps:

    1. Calculates whether the intended mover will out of scope.
    2. Moves the food by 40 to the intended position.
    4. Updates the Turtle screen to reflect the changes.
    5. Schedules the function to be called again after a random delay
        between `5000` and `10000` milliseconds.
    """
    global food
    if len(g_food_items) == 0:
        return
    flag = False
    while not flag:
        number = random.randint(1, len(g_food_items))
        food = random.sample(g_food_items, number)
        count = 0
        for single_food in food:
            if -DIM_PLAY_AREA // 2 + 40 <= single_food[1].pos()[0] <= DIM_PLAY_AREA // 2 - 40 and \
                    -DIM_PLAY_AREA // 2 + 20 <= single_food[1].pos()[1] <= DIM_PLAY_AREA // 2 - 80:
                count += 1
        if count == number:
            flag = True
    for single_food in food:
        x_food, y = single_food[1].pos()
        single_food[1].clear()
        heading = random.randint(0, 3)
        forward = 1.5 - heading
        direction = int(forward / abs(forward))
        x_food = int(x_food + (heading + 1) % 2 * 40 * direction)
        y = int(y + heading % 2 * 40 * direction)
        single_food[1].penup()
        single_food[1].goto(x_food, y)
        single_food[1].pendown()
        single_food[1].write(single_food[0], align="center", font=("Arial", 10, "normal"))
    g_screen.update()
    delay = random.randint(5000, 10000)
    g_screen.ontimer(on_timer_food, delay)


def consume_food() -> bool:
    """
    Simulate the action when the snake consumes the given food item num.
    Increase the length of the snake's tail by the given num value.


    Modifies:
        g_snake_sz (int): Increments the size of the snake's body by the specified number.
        update_status(): Updates the game status display to reflect the new snake size.
    """

    if not g_game_state:
        return
    for food in g_food_items:
        if abs(int(g_snake_items[len(g_snake_items) - 1][0] - food[1].pos()[0])) <= 2 and \
                abs(int(g_snake_items[len(g_snake_items) - 1][1] - 10 - food[1].pos()[1])) <= 2:
            food[1].clear()
            global g_snake_sz, g_food_consumption
            g_snake_sz += food[0]
            g_food_items.remove(food)
            g_food_consumption += food[0]
            update_status()
            return True
    return False


def detect_contact(x: float, y: float) -> None:
    """
        Detect whether the monster collides into snake's tail when the monster moves.

        Args:
        x (float) the x coordinate of the monster.
        y (float) the y coordinate of the monster.

        Modifies:
        g_contact (int): Increments the number of contact by one.


        """
    not_contact = 0
    for i in range(len(g_snake_items)):
        dict_x = int(abs(g_snake_items[i][0] - x))
        dict_y = int(abs(g_snake_items[i][1] - y))
        global g_contact
        if dict_y + dict_x > SZ_SQUARE - 2:
            not_contact += 1
    if not_contact < len(g_snake_items):
        g_contact += 1
        update_status()


def on_timer_game_over_contact() -> None:
    """
        Detect whether the snake collides into monster(s).

        """
    if not g_game_state:
        return
    for j in range(len(g_monster_items)):
        x_position, y_position = g_monster_items[j].pos()
        dict_x = int(abs(g_snake_items[len(g_snake_items) - 1][0] - x_position))
        dict_y = int(abs(g_snake_items[len(g_snake_items) - 1][1] - y_position))
        if dict_y + dict_x <= SZ_SQUARE - 2:
            game_state("Game over !!")
    g_screen.ontimer(on_timer_game_over_contact, TIMER_SNAKE // 2)


def game_state(state: str) -> None:
    """
    Show the subtitle when the game is over and stop refresh the screen.

    Args:
    state (str): The subtitle which want to show on the screen

    """
    subtitle = create_turtle(0, 0)
    subtitle.hideturtle()
    subtitle.pencolor('red')
    subtitle.write(state, align="center", font=("Arial", 50, "normal"))
    global g_game_state
    g_game_state = False


def cb_start_game(x, y):
    """
    Starts the game by setting up the initial game state and event handlers.

    This function is called when the user clicks on the screen to start the game.
    It performs the following steps:

    1. Clears the on-screen click handler to prevent further clicks from starting the game.
    2. Clears the introductory message.
    3. Registers key event handlers for the arrow keys to handle player movement.
    4. Starts the timer-based updates for the snake, monster movements, food and detect contact with the snake's head.
    """
    g_screen.onscreenclick(None)
    global g_start_game
    g_start_game = True
    g_intro.clear()
    food_item()
    global g_movement
    g_movement = "Move"
    update_status()
    g_screen.onkey(if_paused, KEY_SPACE)
    for key in (KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT):
        g_screen.onkey(partial(on_arrow_key_pressed, key), key)
    on_timer_snake()
    on_timer_monster()
    on_timer_food()
    on_timer_game_over_contact()


if __name__ == "__main__":
    """
    It performs the following steps:
    1. Create screen, and show the introduction.
    3. Create snake, monsters, and store the position of snake, turtle of monsters in distinct lists.
    3. detect click motion.

    """
    g_screen = configure_screen()
    g_intro, g_status = configure_play_area()
    update_status()
    for i in range(4):
        x = random.choice([1, -1]) * random.randint(6, 9) * 20
        y = random.choice([1, -1]) * random.randint(6, 9) * 20 - 30

        g_monster = create_turtle(x, y, COLOR_MONSTER, "black")
        g_monster_items.append(g_monster)
    g_snake = create_turtle(0, 0, COLOR_HEAD, "black")
    g_snake_items.append(g_snake.pos())
    total_time()
    g_screen.onscreenclick(cb_start_game)  # set up a mouse-click call back
    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()
