import random
import curses


# Initialize the screen.
c = curses.initscr()
# Set cursor to 0, so that it will not display on the screen.
curses.curs_set(0)
# Get height and width of the screen.
screen_height, screen_width = c.getmaxyx()
# Creates a new window, using screen height and width, and starts it at top-left corner of the screen.
window = curses.newwin(screen_height, screen_width, 0, 0)
# Allow window to accept keypad input.
window.keypad(1)
# Makes window refresh every 100 milliseconds.
window.timeout(100)

# Set snake's default position.
snake_x = screen_width / 4
snake_y = screen_height / 2
# Creates snake's default body parts.
# Snake head, then one body part to the left, and one more to the left of that.
snake = [
	[snake_y, snake_x],
	[snake_y, snake_x - 1],
	[snake_y, snake_x - 2]
]

# Creates default food and sets its default position.
food = [screen_height / 2, screen_width / 2]
# Adds food to the window.
window.addch(food[0], food[1], curses.ACS_PI)

# Set snake's default direction (right).
key = curses.KEY_RIGHT

# Start an infinite loop for each snake movement.
while True:
	# Get next key that the user inputs.
	next_key = window.getch()
	key = key if next_key == -1 else next_key

	# Check if user has lost the game.
	# If snake hits one of the walls or hits itself.
	if snake[0][0] in [0, screen_height] or \
		snake[0][1] in [0, screen_width] or \
		snake[0] in snake[1:]:
		# Close the window, and quit the application.
		curses.endwin()
		quit()

	# Create new head of the snake (default, set old head of snake as starting point).
	new_snake_head = [snake[0][0], snake[0][1]]

	# Figure out what the key currently being used is.
	if key == curses.KEY_DOWN:
		new_snake_head[0] += 1
	if key == curses.KEY_UP:
		new_snake_head[0] -= 1
	if key == curses.KEY_LEFT:
		new_snake_head[1] -= 1
	if key == curses.KEY_RIGHT:
		new_snake_head[1] += 1

	# Insert the new snake head to the snake.
	snake.insert(0, new_snake_head)

	# Determine if snake has run into food, and create new food afterward.
	if snake[0] == food:
		food = None
		while food is None:
			# Creates new food and sets its default location on the screen.
			new_food = [
				random.randint(1, screen_height - 1),
				random.randint(1, screen_width - 1)
			]
			# Check if new food is not in snake already, and loops again if it already is.
			food = new_food if new_food not in snake else None
		# Once new food has been created, add it to the window.
		window.addch(food[0], food[1], curses.ACS_PI)
	# If the snake has not run into food.
	else:
		# Get tail, and add space at the end of the snake where the tail was.
		tail = snake.pop()
		window.addch(tail[0], tail[1], " ")

	# In any case, add the head of the snake to the screen.
	window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
