import pygame
from chess_engine import *
import os


pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
FPS = 60
WIDTH = 600
HEIGHT = 600
SQUARE_SIDE = WIDTH / 8

SQUARE_DIMENSIONS = (SQUARE_SIDE - 25, SQUARE_SIDE - 25)

GRID_OUTLINE_COLOR = (66, 34, 25)
GRID_OUTLINE = 30
MAIN_PIECE_IMAGE_DICT = {}
FONT = pygame.font.SysFont(None, 24)
BLUE_DOT_OFFSET = 25





def screen_to_chess_coords(coords:tuple) -> tuple:
    coords = coords[0] // SQUARE_SIDE, coords[1] // SQUARE_SIDE
    coords = coords[0] + 1, 7 - coords[1] + 1
    coords = int(coords[0]), int(coords[1])
    return coords

def back_to_default(selected_sqaure:Square, possible_moves:tuple):
    selected.back_to_default_color()
    [i.back_to_default_color() for i in possible_moves]



def display_check(screen:pygame.surface.Surface, color=RED):
    screen.blit(FONT.render("Check", False, color), (WIDTH//2 - 40, 20))

def display_checkmate(screen:pygame.surface.Surface, color=RED):
    screen.blit(FONT.render("Checkmate", False, color), (WIDTH//2 - 40, 20))

#order goes: Pawn, Bishop, Knight, Rook, Queen




current_possible_move_coords = []

class Pygame_Chess_Grid:
    def __init__(self, pos:tuple, size:float):
        self.pos = pos
        self.size = size
        self.square_size = size // 8
        self.chess_coords_transform = lambda t: t
        

    def screen_to_chess_coords(self, coords:tuple) -> tuple:

        coords = coords[0] - self.pos[0], coords[1] - self.pos[1]
        coords = coords[0] // self.square_size, coords[1] // self.square_size
        coords = coords[0] + 1, 7 - coords[1] + 1
        coords = int(coords[0]), int(coords[1])
        coords = self.chess_coords_transform(coords)
        return coords

    

    def handle_click(self, click_pos:tuple):
        
        coords = self.screen_to_chess_coords(click_pos)

        if in_grid(coords):
            return coords
        else:
            return None
        
    def render_grid(self, screen:pygame.surface.Surface, view_direction:str):

        pygame.draw.rect(screen, GRID_OUTLINE_COLOR, [self.pos[0] - GRID_OUTLINE, self.pos[1] - GRID_OUTLINE, 2 * GRID_OUTLINE + self.size, GRID_OUTLINE])
        pygame.draw.rect(screen, GRID_OUTLINE_COLOR, [self.pos[0] - GRID_OUTLINE, self.pos[1] + self.size, 2 * GRID_OUTLINE + self.size, GRID_OUTLINE])
        pygame.draw.rect(screen, GRID_OUTLINE_COLOR, [self.pos[0] - GRID_OUTLINE, self.pos[1], GRID_OUTLINE, self.size])
        pygame.draw.rect(screen, GRID_OUTLINE_COLOR, [self.pos[0] + self.size, self.pos[1], GRID_OUTLINE, self.size])

        match view_direction:
            case "w":
                self.chess_coords_transform = lambda t:t
            case "b":
                self.chess_coords_transform = lambda t: (t[0], 9-t[1])
        
        for n in range(64):
            y = (n // 8)
            x = n % 8

            coords = self.pos[0] + x * self.square_size, self.pos[1] + y * self.square_size

            chess_coords = self.screen_to_chess_coords(coords)


            square = grid.coords(chess_coords)
            
            pygame.draw.rect(screen, square.color, [coords[0], coords[1], self.square_size, self.square_size],0)


            if square.contains_piece:
                # screen.blit(FONT.render(square.piece.piece_identifier, True, BLACK), coords)
                screen.blit(MAIN_PIECE_IMAGE_DICT[square.piece.piece_identifier], coords)

            if chess_coords in current_possible_move_coords:
                pygame.draw.circle(screen, BLUE, (coords[0] + BLUE_DOT_OFFSET, coords[1] + BLUE_DOT_OFFSET), 10, 10)
    


pygame.display.set_caption("Easy Chess: White Turn")
pygame_chess_grid = Pygame_Chess_Grid((100, 100), 400)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock() 
selected = None
current_possible_moves = set()


FOLDER_NAME = 'assets'

BB_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'black_bishop.png'))
BK_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'black_king.png'))
BKN_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'black_knight.png'))
BP_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'black_pawn.png'))
BQ_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'black_queen.png'))
BR_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'black_rook.png'))

WB_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'white_bishop.png'))
WK_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'white_king.png'))
WKN_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'white_knight.png'))
WP_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'white_pawn.png'))
WQ_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'white_queen.png'))
WR_IMAGE = pygame.image.load(os.path.join(FOLDER_NAME, 'white_rook.png'))


MAIN_PIECE_IMAGE_DICT = {'BB': pygame.transform.scale(BB_IMAGE, SQUARE_DIMENSIONS),
                         'BK': pygame.transform.scale(BK_IMAGE, SQUARE_DIMENSIONS),
                         'BKn': pygame.transform.scale(BKN_IMAGE, SQUARE_DIMENSIONS),
                         'BP': pygame.transform.scale(BP_IMAGE, SQUARE_DIMENSIONS),
                         'BQ': pygame.transform.scale(BQ_IMAGE, SQUARE_DIMENSIONS),
                         'BR': pygame.transform.scale(BR_IMAGE, SQUARE_DIMENSIONS),

                         'WB': pygame.transform.scale(WB_IMAGE, SQUARE_DIMENSIONS),
                         'WK': pygame.transform.scale(WK_IMAGE, SQUARE_DIMENSIONS),
                         'WKn': pygame.transform.scale(WKN_IMAGE, SQUARE_DIMENSIONS),
                         'WP': pygame.transform.scale(WP_IMAGE, SQUARE_DIMENSIONS),
                         'WQ': pygame.transform.scale(WQ_IMAGE, SQUARE_DIMENSIONS),
                         'WR': pygame.transform.scale(WR_IMAGE, SQUARE_DIMENSIONS)}

MOVE_SOUND = pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'moving_piece.wav'))
CHECK_SOUND = pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'check.wav'))


def render_taken_piece_log(piece_list):

    for piece in piece_list:
        print (piece)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False

        elif event.type == pygame.MOUSEBUTTONDOWN: #MOUSE CLICK ACTIONS
            pos = pygame.mouse.get_pos()
            coords = pygame_chess_grid.handle_click(pos)
            if coords != None:

                this_square = grid.coords(coords)

                if this_square.contains_piece and this_square.piece.color == grid.current_turn: #SELECTING PIECE
                

                    this_square.clicked()
                    

                    if selected != None and selected != this_square:
                        selected.back_to_default_color()
                        for square in current_possible_moves:
                            square.back_to_default_color()

                    selected = this_square
                    current_possible_moves = []
                    current_possible_move_coords = selected.piece.get_moves(grid)
                    to_remove = []
                    for move in current_possible_move_coords:
                        if not does_not_endanger_king(this_square.piece, grid, move):
                            to_remove.append(move)
                    for item in to_remove:
                        current_possible_move_coords.remove(item)
                            
                    
                    for square_coords in current_possible_move_coords:
                        square = grid.coords(square_coords)
                        square.is_possible_move()
                        current_possible_moves.append(square)
                        
                elif this_square in current_possible_moves: #MOVING
                    selected.piece.move(grid, coords)
                    back_to_default(selected, current_possible_moves)
                    selected = None
                    current_spossible_moves = set()
                    match grid.current_turn:
                        case "w":
                            pygame.display.set_caption("Easy Chess: White Turn")
                        case "b":
                            pygame.display.set_caption("Easy Chess: Black Turn")


                    
                    
                    current_possible_moves = []
                    current_possible_move_coords = []

                    if grid.white_checked or grid.black_checked:
                        pygame.mixer.Sound.play(CHECK_SOUND)
                    else:
                        pygame.mixer.Sound.play(MOVE_SOUND)

                    
                    

                elif selected != None: #CLICKED AWAY FROM PIECE

                    back_to_default(selected, current_possible_moves)
                    selected = None
                    current_possible_moves = set()
                    current_possible_move_coords = []
 
    screen.fill(WHITE)
    pygame_chess_grid.render_grid(screen, grid.current_turn)
    render_taken_piece_log(grid.taken_white_pieces)

    if grid.white_checked or grid.black_checked:
        display_check(screen)






 
 
    pygame.display.flip()
     
    clock.tick(FPS)
 
pygame.quit()
