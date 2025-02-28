# libraries & constant values
from constants import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0
player_pos = pygame.Vector2(0, 0)


first_line = ""


# Define a function to read the text file
def read_text_file(file_path):
    try:
        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            return file.read()
    except FileNotFoundError:
        return "File not found."


# Load the text from the file
text = read_text_file("input-01.txt")
# Set up font and color
font = pygame.font.Font(None, CELL_SIZE)
# Read the input file
with open("input-01.txt", "r") as f:
    next(f)  # skip the first line
    # grid = [list(line.strip()) for line in f.readlines()]
    text = f.read()
# Split the text into lines
lines = text.split("\n")


# map symbols
symbol_colors = {
    "#": BLACK,  # Black for walls
    " ": WHITE,  # White for free spaces
    "$": GRAY,  # Gray for stones
    "@": RED,  # Red for player
}


# Map symbols to colors based on their position in the text file
def symbol_to_color(symbol, row, col):
    if symbol == "#":  # Wall
        return BLACK
    elif symbol == " ":  # Empty space
        return WHITE
    elif symbol == "$":  # Stone
        return GRAY
    elif symbol == "@":  # Ares the Player
        return GREEN
    elif symbol == ".":  # Switch
        return RED
    elif symbol == "*":  # Stone placed on switch
        return BLUE
    elif symbol == "+":  # Ares the Player on a switch
        return YELLOW
    # Default to black if symbol is not recognized
    return BLACK


# Define a color board
color_board = {
    "#": BLACK,  # Walls
    " ": WHITE,  # Free spaces
    "$": GRAY,  # Stones
    "@": GREEN,  # Ares the Player
    ".": RED,  # Switch
    "*": BLUE,  # Stone placed on switch
    "+": YELLOW,  # Ares on a switch
}

# game loop
running = True
while running:
    # poll for events
    # pygame.QUIT = user clicked X to close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill screen to clean frame
    screen.fill("purple")

    # draw the grid
    x = 0
    y = 0
    for line in lines:
        for char in line:
            # Set player starting position
            # if char == "@":
            #     player_pos.x +=CELL_SIZE* x
            #     player_pos.y +=CELL_SIZE* y
            # else:
            color = color_board[char]
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            x += CELL_SIZE
        x = 0
        y += CELL_SIZE

    # Update the display
    pygame.display.flip()

    # Draw the player
    pygame.draw.rect(screen, "green", (player_pos.x, player_pos.y, CELL_SIZE, CELL_SIZE))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        # if player_pos.y >= 0 and color_board[lines[player_pos.y // CELL_SIZE][player_pos.x // CELL_SIZE]] != WHITE:
        #             player_pos.y -= CELL_SIZE
        player_pos.y -= CELL_SIZE
    if keys[pygame.K_s]:
        # if player_pos.y < SCREEN_HEIGHT and color_board[lines[player_pos.y // CELL_SIZE][player_pos.x // CELL_SIZE]] != WHITE:
        #             player_pos.y = player_pos.y
        player_pos.y += CELL_SIZE
    if keys[pygame.K_a]:
        # if player_pos.x >= 0 and color_board[lines[player_pos.y // CELL_SIZE][player_pos.x // CELL_SIZE]] != WHITE:
        #             player_pos.x = player_pos.x
        player_pos.x -= CELL_SIZE
    if keys[pygame.K_d]:
        # if player_pos.x < SCREEN_WIDTH and color_board[lines[player_pos.y // CELL_SIZE][player_pos.x // CELL_SIZE]] != WHITE:
        #             player_pos.x = player_pos.x
        player_pos.x += CELL_SIZE

    # Update the display
    pygame.display.flip()

    # limits FPS to constant
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(FPS) / 1000

pygame.quit()