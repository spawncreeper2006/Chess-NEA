import pygame
from chess_engine import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
FPS = 60
WIDTH = 600
HEIGHT = 600
SQUARE_SIDE = WIDTH / 8

GRID_OUTLINE_COLOR = (66, 34, 25)
GRID_OUTLINE = 30


def screen_to_chess_coords(coords:tuple) -> tuple:
    coords = coords[0] // SQUARE_SIDE, coords[1] // SQUARE_SIDE
    coords = coords[0] + 1, 7 - coords[1] + 1
    coords = int(coords[0]), int(coords[1])
    return coords

def back_to_default(selected_sqaure:Square, possible_moves:tuple):
    selected.back_to_default_color()
    [i.back_to_default_color() for i in possible_moves]

pygame.init()
FONT = pygame.font.SysFont(None, 24)

def display_check(screen:pygame.surface.Surface, color=RED):
    screen.blit(FONT.render("Check", False, color), (WIDTH//2 - 40, 20))

def display_checkmate(screen:pygame.surface.Surface, color=RED):
    pass

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
                screen.blit(FONT.render(square.piece.piece_identifier, True, BLACK), coords)


pygame.display.set_caption("Easy Chess: White Turn")
pygame_chess_grid = Pygame_Chess_Grid((100, 100), 400)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock() 
selected = None
current_possible_moves = set()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            coords = pygame_chess_grid.handle_click(pos)
            if coords != None:

                this_square = grid.coords(coords)
                if this_square.contains_piece and this_square.piece.color == grid.current_turn:
                

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
                        
                elif this_square in current_possible_moves:
                    selected.piece.move(grid, coords)
                    back_to_default(selected, current_possible_moves)
                    selected = None
                    current_possible_moves = set()
                    match grid.current_turn:
                        case "w":
                            pygame.display.set_caption("Easy Chess: White Turn")
                        case "b":
                            pygame.display.set_caption("Easy Chess: Black Turn")
                    

                elif selected != None:

                    back_to_default(selected, current_possible_moves)
                    selected = None
                    current_possible_moves = set()
 
    screen.fill(WHITE)

    pygame_chess_grid.render_grid(screen, grid.current_turn)
    # screen.blit(FONT.render(square.piece.piece_identifier, True, BLACK), coords)

    


 
 
    pygame.display.flip()
     
    clock.tick(FPS)
 
pygame.quit()
