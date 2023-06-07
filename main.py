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

pygame.init()





FONT = pygame.font.SysFont(None, 24)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Easy Chess")

running = True


clock = pygame.time.Clock()
 

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
             pos = pygame.mouse.get_pos()
             coords = screen_to_chess_coords(pos)


             grid.coords(coords).clicked()

 
    screen.fill(WHITE_WOOD)

    for n in range(64):
        y = (8 - n // 8) - 1
        x = n % 8

        coords = x*SQUARE_SIDE, y*SQUARE_SIDE
        chess_coords = screen_to_chess_coords(coords)
        
        #color = WHITE_WOOD if (x + y) % 2 == 0 else BLACK_WOOD
        square = grid.coords(chess_coords)
        

        pygame.draw.rect(screen, square.color, [coords[0], coords[1], SQUARE_SIDE, SQUARE_SIDE],0)
        


        if square.contains_piece:
            #print (coords, x, y, square)
            

            screen.blit(FONT.render(square.piece.piece_identifier, True, BLACK), coords)




    # pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    # pygame.draw.ellipse(screen, BLACK, [20,20,250,100], 2)
 
 
    pygame.display.flip()
     
    clock.tick(FPS)
 
pygame.quit()
