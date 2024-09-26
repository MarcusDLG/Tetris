import pygame
import random

pygame.font.init()  # Initialize fonts

# Global Variables
BLOCK_SIZE = 30
COLUMNS = 10
ROWS = 20

PLAY_WIDTH = BLOCK_SIZE * COLUMNS    # 300
PLAY_HEIGHT = BLOCK_SIZE * ROWS      # 600

# Increase SCREEN_WIDTH to provide space on both sides
SCREEN_WIDTH = PLAY_WIDTH + 400      # Increased width for next piece and score display
SCREEN_HEIGHT = PLAY_HEIGHT + 100    # Extra height for additional UI elements

# Position of the top-left corner of the play area
top_left_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2
top_left_y = SCREEN_HEIGHT - PLAY_HEIGHT - 50   # Leave space at the top

# Colors (R, G, B)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 85, 85)
GREEN = (100, 200, 115)
BLUE = (120, 108, 245)
YELLOW = (255, 255, 85)
CYAN = (85, 255, 255)
ORANGE = (255, 170, 0)
PURPLE = (223, 75, 223)

# Shapes and their rotations
SHAPES = [
    [['.....',
      '.....',
      '..O..',
      '..O..',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.....',
      'OOOO.',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '.....',
      '.OO..',
      '.OO..',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '..O..',
      '.OO..',
      '.O...',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '.OO..',
      '..OO.',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '..O..',
      '..OO.',
      '...O.',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '.OO..',
      'OO...',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '.O...',
      '.OOO.',
      '.....',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '..OO.',
      '..O..',
      '..O..',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '.....',
      '.OOO.',
      '...O.',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '...O.',
      '.OOO.',
      '.....',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '..O..',
      '..O..',
      '..OO.',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '.....',
      '.OOO.',
      '.O...',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '.OO..',
      '..O..',
      '..O..',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '..O..',
      '.OOO.',
      '.....',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....',
      '.....']],
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, ORANGE, BLUE]

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLUMNS):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid

class Piece:
    def __init__(self, x, y, shape):
        self.x = x  # Column position
        self.y = y  # Row position
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(COLUMNS) if grid[i][j] == BLACK] for i in range(ROWS)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(COLUMNS // 2, 0, random.choice(SHAPES))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + PLAY_WIDTH / 2 - (label.get_width() / 2),
                         top_left_y + PLAY_HEIGHT / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface, GRAY, (sx, sy + i * BLOCK_SIZE), (sx + PLAY_WIDTH, sy + i * BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, GRAY, (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT))

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    return increment

def draw_window(surface, grid, score=0):
    surface.fill(BLACK)

    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, WHITE)
    surface.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2, 30))

    # Current Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, WHITE)
    sx = top_left_x + PLAY_WIDTH + 50
    sy = top_left_y + PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx, sy + 160))

    # Draw the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * BLOCK_SIZE, top_left_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw grid lines
    draw_grid(surface, grid)

    # Draw border around play area
    pygame.draw.rect(surface, RED, (top_left_x, top_left_y, PLAY_WIDTH, PLAY_HEIGHT), 5)

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = top_left_x - 200  # Position to the left of the play area
    sy = top_left_y + PLAY_HEIGHT / 2 - 100

    surface.blit(label, (sx + 10, sy - 30))

    # Draw the next piece
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    score = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Handle piece falling
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -=1
                change_piece = True

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -=1
                    if not valid_space(current_piece, grid):
                        current_piece.x +=1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x +=1
                    if not valid_space(current_piece, grid):
                        current_piece.x -=1
                elif event.key == pygame.K_DOWN:
                    current_piece.y +=1
                    if not valid_space(current_piece, grid):
                        current_piece.y -=1
                elif event.key == pygame.K_UP:
                    current_piece.rotation +=1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -=1

        shape_pos = convert_shape_format(current_piece)

        # Add piece to the grid
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # Lock the piece and generate a new one
        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # Clear rows and update score
            increment = clear_rows(grid, locked_positions)
            if increment > 0:
                line_clear_scores = {1: 40, 2: 100, 3: 300, 4: 1200}
                score += line_clear_scores.get(increment, 0)

        draw_window(screen, grid, score)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        # Check if the game is over
        if check_lost(locked_positions):
            run = False
            draw_text_middle(screen, "You Lost", 80, WHITE)
            pygame.display.update()
            pygame.time.delay(2000)

    pygame.quit()

if __name__ == '__main__':
    main()
