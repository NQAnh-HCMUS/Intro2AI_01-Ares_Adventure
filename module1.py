# libraries & constant values
from constants import *
from player import Player
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





# # Create player
player = Player()

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

    player.update()

    # Draw player
    pygame.draw.circle(screen, (255, 0, 0), (int(player.position.x), int(player.position.y)), 10)


    # Update the display
    pygame.display.flip()

    # limits FPS to constant
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(FPS) / 1000

pygame.quit()