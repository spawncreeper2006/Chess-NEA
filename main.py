import pygame
from chess_engine import *


BLACK = (0, 0, 0)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
FPS = 60
WIDTH = 600
HEIGHT = 600
SQUARE_SIDE = WIDTH / 8


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

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Easy Chess White Turn")

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
            coords = screen_to_chess_coords(pos)

            this_square = grid.coords(coords)
            

            if this_square.contains_piece and this_square.piece.color == grid.current_turn:
            

                this_square.clicked()
                

                if selected != None and selected != this_square:
                    selected.back_to_default_color()
                    for square in current_possible_moves:
                        square.back_to_default_color()

                else:

                    selected = this_square
                    current_possible_moves = []
                    current_possible_move_coords = selected.piece.get_moves()
                    for square_coords in current_possible_move_coords:
                        square = grid.coords(square_coords)
                        square.is_possible_move()
                        current_possible_moves.append(square)
                        
            elif this_square in current_possible_moves:
                selected.piece.move(coords)
                back_to_default(selected, current_possible_moves)
                selected = None
                current_possible_moves = set()

            elif selected != None:

                back_to_default(selected, current_possible_moves)
                selected = None
                current_possible_moves = set()
 
    screen.fill(WHITE_WOOD)

    for n in range(64):
        y = (8 - n // 8) - 1
        x = n % 8

        coords = x*SQUARE_SIDE, y*SQUARE_SIDE
        chess_coords = screen_to_chess_coords(coords)
        

        square = grid.coords(chess_coords)
        

        pygame.draw.rect(screen, square.color, [coords[0], coords[1], SQUARE_SIDE, SQUARE_SIDE],0)
        


        if square.contains_piece:

            screen.blit(FONT.render(square.piece.piece_identifier, True, BLACK), coords)

 
 
    pygame.display.flip()
     
    clock.tick(FPS)
 
pygame.quit()
