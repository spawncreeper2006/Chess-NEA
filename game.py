import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


import pygame
from chess_engine_2 import *
import random

import tkinter as tk
from typing import Callable
from move_sources import Move_Source
from threading import Thread
from user_interface.pygame_user_interface import Button
from constants import *


def promote_pawn_UI() -> Piece:
    pieces = [Queen, Rook, Bishop, Knight]
    root = tk.Tk()
    WIDTH = 200
    HEIGHT = 200
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')



    lbl = tk.Label(root, text = 'What do you want to promote to?')
    lbl.place(x=0, y=0)


    var = tk.IntVar()
    r1 = tk.Radiobutton(root, text="Queen", variable=var, value=0)
    r1.place(x=0, y=50)

    r2 = tk.Radiobutton(root, text="Rook", variable=var, value=1)
    r2.place(x=0, y=80)

    r3 = tk.Radiobutton(root, text="Bishop", variable=var, value=2)
    r3.place(x=0, y=110)

    r4 = tk.Radiobutton(root, text="Knight", variable=var, value=3)
    r4.place(x=0, y=140)

    btn = tk.Button(root, text = '  OK  ', command = root.destroy)
    btn.place(x=145, y=160)
    root.mainloop()

    return pieces[var.get()]

#board.ask_for_promotion = promote_pawn_UI



pygame.init()


try:
    pygame.mixer.init()
except pygame.error:
    has_audio = False
else:
    has_audio = True


MAIN_PIECE_IMAGE_DICT = {}
FONT = pygame.font.SysFont(None, 24)
BIG_FONT = pygame.font.SysFont(None, 35)


current_possible_moves = []






def screen_to_chess_coords(coords: tuple) -> tuple:
    coords = coords[0] // SQUARE_SIDE, coords[1] // SQUARE_SIDE
    coords = coords[0] + 1, 7 - coords[1] + 1
    coords = int(coords[0]), int(coords[1])
    return coords

def back_to_default(selected_sqaure: Square, possible_moves:tuple):
    global selected
    selected.back_to_default_color()
    [i.back_to_default_color() for i in possible_moves]



def display_check(screen: pygame.surface.Surface, color=RED):
    screen.blit(BIG_FONT.render("Check", False, color), (WIDTH//2 - 40, 0))

def display_checkmate(screen:pygame.surface.Surface, color=RED):
    screen.blit(BIG_FONT.render("Checkmate", False, color), (WIDTH//2 - 40, 0))

def display_draw(screen:pygame.surface.Surface, color=RED):
    screen.blit(BIG_FONT.render("Draw", False, color), (WIDTH//2 - 40, 0))




# current_possible_move_coords = []


class Pygame_Chess_Board:
    def __init__(self, board: Board, pos: tuple, size: float):
        self.board = board
        self.pos = pos
        self.size = size
        self.square_size = size // 8
        self.square_colors = [WHITE_WOOD if (n % 8 + n // 8) % 2 == 1 else BLACK_WOOD for n in range(64)]
        self.default_sqaure_colors = self.square_colors.copy()
        self.transform = None

    def transform_coords(self, coord: tuple[int, int]) -> int:
        coord = (coord[0] - 1, coord[1] - 1)
        _val = (coord[0] + coord[1] * 8)
        return _val

    def set_color(self, coord: tuple[int, int], color: tuple[int, int, int]):
        self.square_colors[self.transform_coords(coord)] = color
    
    def set_colors(self, coords: tuple[tuple[int, int]], color: tuple[int, int, int]):
        for coord in coords:
            self.set_color(coord, color)

    def default_color(self, coord: tuple[int, int]):
        index = self.transform_coords(coord)
        self.square_colors[index] = self.default_sqaure_colors[index]

    def default_colors(self, coords: tuple[tuple[int, int]]):
        for coord in coords:
            self.default_color(coord)

    def screen_to_chess_coords(self, coords: tuple[int, int]) -> tuple[int, int]:

        
        coords = coords[0] - self.pos[0], coords[1] - self.pos[1]
        coords = coords[0] // self.square_size + 1, coords[1] // self.square_size + 1
        return self.transform(coords)
        # return coords
    
    def handle_click(self, click_pos: tuple[int, int]):
        
        coords = self.screen_to_chess_coords(click_pos)

        if Board.contains(coords):
            return coords
        else:
            return None
        
    



        

    # def screen_to_chess_coords(self, coords: tuple) -> tuple[int, int]:

    #     coords = coords[0] - self.pos[0], coords[1] - self.pos[1]
    #     coords = coords[0] // self.square_size, coords[1] // self.square_size
    #     coords = coords[0] + 1, 7 - coords[1] + 1
    #     coords = int(coords[0]), int(coords[1])
    #     coords = self.coords_transform(coords)
    #     print (coords)
    #     return coords

    

    # def handle_click(self, click_pos: tuple):
        
    #     coords = self.screen_to_chess_coords(click_pos)

    #     if Board.contains(coords):
    #         return coords
    #     else:
    #         return None
        
    def render_board(self, screen: pygame.surface.Surface, view_direction: str, possible_moves: list[tuple]):

        #global current_possible_move_coords
        

        pygame.draw.rect(screen, BOARD_OUTLINE_COLOR, [self.pos[0] - BOARD_OUTLINE, self.pos[1] - BOARD_OUTLINE, 2 * BOARD_OUTLINE + self.size, BOARD_OUTLINE])
        pygame.draw.rect(screen, BOARD_OUTLINE_COLOR, [self.pos[0] - BOARD_OUTLINE, self.pos[1] + self.size, 2 * BOARD_OUTLINE + self.size, BOARD_OUTLINE])
        pygame.draw.rect(screen, BOARD_OUTLINE_COLOR, [self.pos[0] - BOARD_OUTLINE, self.pos[1], BOARD_OUTLINE, self.size])
        pygame.draw.rect(screen, BOARD_OUTLINE_COLOR, [self.pos[0] + self.size, self.pos[1], BOARD_OUTLINE, self.size])

        match view_direction:
            case "w":
                self.transform = lambda t: (t[0], 9 - t[1])
                # self.transform = lambda t: t
            case 'b':
                self.transform = lambda t: (9 - t[0], t[1])
            
        
        # for n in range(64):
        #     y = (n // 8)
        #     x = n % 8

        #     coords = (x, y)

        #     x, y = self.transform((x + 1, y + 1))
        #     coords = self.pos[0] + x * self.square_size, self.pos[1] + y * self.square_size

            
        #     chess_coords = coords[0] - self.pos[0], coords[1] - self.pos[1]
        #     chess_coords = chess_coords[0] // self.square_size + 1, chess_coords[1] // self.square_size + 1
        #     chess_coords = self.transform(chess_coords)
        #     # x, y = self.chess_coords_transform(chess_coords)
        #     square = self.board[self.transform((chess_coords[0], chess_coords[1]))]
        #     pygame.draw.rect(screen, self.square_colors[n], [coords[0], coords[1], self.square_size, self.square_size],0)


        #     if square.piece != None:

        #         screen.blit(MAIN_PIECE_IMAGE_DICT[square.piece.piece_identifier], coords)

        #     if chess_coords in possible_moves:
        #         pygame.draw.circle(screen, BLUE, (coords[0] + BLUE_DOT_OFFSET, coords[1] + BLUE_DOT_OFFSET), 10, 10)


        for n in range(2 ** 6):
            y, x = divmod(n, 8)
            chess_coords = self.transform((x + 1, y + 1))
            
            index = self.transform_coords(chess_coords)
            rect = [x * self.square_size + self.pos[1], y * self.square_size + self.pos[1], self.square_size, self.square_size]
            pygame.draw.rect(screen, self.square_colors[index], rect)

            square = self.board[chess_coords]

            if square.piece != None:
                screen.blit(MAIN_PIECE_IMAGE_DICT[square.piece.piece_identifier], rect)

            if chess_coords in possible_moves:
                pygame.draw.circle(screen, BLUE, (rect[0] + BLUE_DOT_OFFSET, rect[1] + BLUE_DOT_OFFSET), 10, 10)
        
        
        # x = pygame.surface.Surface((500, 500))
        # x.set_alpha(150)
        # # x.fill((255, 255, 255))
        # pygame.draw.polygon(x.convert_alpha(), (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
        # screen.blit(x, (0, 0))



selected = None


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

ICON_PIECE_IMAGE_DICT = {'BB': pygame.transform.scale(BB_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'BK': pygame.transform.scale(BK_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'BKn': pygame.transform.scale(BKN_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'BP': pygame.transform.scale(BP_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'BQ': pygame.transform.scale(BQ_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'BR': pygame.transform.scale(BR_IMAGE, ICON_IMAGE_DIMENSIONS),

                         'WB': pygame.transform.scale(WB_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'WK': pygame.transform.scale(WK_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'WKn': pygame.transform.scale(WKN_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'WP': pygame.transform.scale(WP_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'WQ': pygame.transform.scale(WQ_IMAGE, ICON_IMAGE_DIMENSIONS),
                         'WR': pygame.transform.scale(WR_IMAGE, ICON_IMAGE_DIMENSIONS)}


if has_audio:

    CHESS_SOUND_DICT = {}
    CHESS_SOUND_DICT_2 = {}



def render_taken_piece_log(screen: pygame.surface.Surface, piece_list: list, starting_coords: tuple):

    # coords = starting_coords
    # for piece in piece_list:
    #     screen.blit(ICON_PIECE_IMAGE_DICT[piece], coords)
    #     coords = add_coords(coords, (ICON_SPACING, 0))

    pass





class Window:

    def undo(self):
        if self.board.can_undo():
            self.board.undo()

        # global board

        # board.undo()
        # pieces = board.white_pieces if board.current_turn == 'w' else board.black_pieces
        # for piece in pieces:
        #     board.coords(piece.pos).back_to_default_color()
        
        # self.board.undo()

            

    def __init__(self, size: tuple[int, int], render_function: Callable[[list[pygame.event.Event]], None], undo_enabled=False):
        global CHESS_SOUND_DICT, CHESS_SOUND_DICT_2, BIG_FONT, current_possible_moves, current_possible_move_coords, stack
        
        self.possible_move_coords = set()
        
        self.board = create_board()
        self.pygame_chess_board = Pygame_Chess_Board(self.board, (100, 100), 400)




        self.widgets = []

        self.screen = pygame.display.set_mode(size)

        self.undo_enabled = undo_enabled
        if undo_enabled:
            self.widgets.append(Button(screen=self.screen, text='Undo', pos=(530, 30), click_action=self.undo, background_color=(230, 230, 230)))
            
            # stack.clear()


        self.thread = None
        self.busy = False
        self.finished_thread = False
        self.width, self.height = size
        
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_possible_moves = set()
        self.render_function = render_function
        self.render_function([])
        self.disabled = False
        self.destroyed = False

        self.selected = None
        

        # current_possible_moves = set()
        # current_possible_move_coords = set()
        pygame.font.init()

        if has_audio:
                
            pygame.mixer.init()
            
            CHESS_SOUND_DICT = {'B': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Bishop.wav')),
                                'K': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'King.wav')),
                                'Kn': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Knight.wav')),
                                'P': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Pawn.wav')),
                                'Q': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Queen.wav')),
                                'R': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Rook.wav'))}

            CHESS_SOUND_DICT_2 = {'B': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Bishop 2.wav')),
                                'K': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'King 2.wav')),
                                'Kn': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Knight 2.wav')),
                                'P': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Pawn 2.wav')),
                                'Q': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Queen 2.wav')),
                                'R': pygame.mixer.Sound(os.path.join(FOLDER_NAME, 'Rook 2.wav'))}

        BIG_FONT = pygame.font.SysFont(None, 35)


    def update(self) -> bool:
        
        events = pygame.event.get()


        if self.finished_thread:
            self.finished_thread = False
            self.busy = False
            self.render_function(events)
            return True

        if events == []:
            return True

        event_types = list(map(lambda x: x.type, events))

        if pygame.QUIT in event_types:
            self.destroyed = True
            return False
        
        elif pygame.MOUSEBUTTONDOWN in event_types:
            self.render_function(events)
            return True
        


        else: #Nothing happened
            return True
        
    def move(self, start: tuple[int, int], dest: tuple[int, int], is_computer=False):
        
        # piece.move(board, pos, is_computer=is_computer)
        # if self.undo_enabled:
        #     stack.push(deepcopy(board))
        
        #board.coords(piece.pos).piece.move(board, pos, is_simulated=False, is_computer=is_computer)
        self.board.move(np.array([start, dest]))
        self.play_sound_effect(self.board[dest].piece)

        

    def play_sound_effect(self, piece: Piece):

        
        if has_audio:

            
            pieceID = piece.piece_identifier[1:]



            if random.randint(0,1) == 1:
                pygame.mixer.Sound.play(CHESS_SOUND_DICT[pieceID])
            else:
                pygame.mixer.Sound.play(CHESS_SOUND_DICT_2[pieceID])

    def handle_click(self) -> bool:
        move_made = False
        pos = pygame.mouse.get_pos()
        coords = self.pygame_chess_board.handle_click(pos)
        if coords != None and not self.disabled:


            square = self.board[coords]
            if square.piece != None and square.piece.color == self.board.current_turn:
                if self.selected != None:
                    self.pygame_chess_board.default_color(self.selected)

                # self.pygame_chess_board.default_colors(self.current_possible_moves)
                    
                self.selected = coords
                self.possible_move_coords = square.piece.get_moves(coords, self.board)
                self.possible_move_coords = set(list(map(tuple, self.possible_move_coords)))

                self.pygame_chess_board.set_color(np.array(self.selected), SELECTED_COLOR)

                print (self.selected)

            elif coords in self.possible_move_coords:
                
                self.move(self.selected, coords)
                move_made = True
                self.pygame_chess_board.default_color(self.selected)
                self.possible_move_coords = set()

        else:
            self.pygame_chess_board.default_color(self.selected)
            self.possible_move_coords = set()


            for widget in self.widgets:
                if widget.check_click(pos):

                    
                    
                    break

        return move_made
                    

        



        # move_made = False
        # global selected, current_possible_moves, current_possible_move_coords
        # pos = pygame.mouse.get_pos()
        # coords = pygame_chess_board.handle_click(pos)
        # if coords != None and not self.disabled:

            # this_square = board.coords(coords)

            # if this_square.contains_piece and this_square.piece.color == board.current_turn: #SELECTING PIECE
            

            #     this_square.clicked()
                

                # if selected != None and selected != this_square:
                #     selected.back_to_default_color()
                #     for square in current_possible_moves:
                #         square.back_to_default_color()

                # selected = this_square
                # current_possible_moves = []
                # current_possible_move_coords = selected.piece.get_moves(board)
                # to_remove = []
                # for move in current_possible_move_coords:
                #     if not does_not_endanger_king(this_square.piece, board, move):
                #         to_remove.append(move)
                # for item in to_remove:
                #     current_possible_move_coords.remove(item)
                        
                
                # for square_coords in current_possible_move_coords:
                #     square = board.coords(square_coords)
                #     square.is_possible_move()
                #     current_possible_moves.append(square)

                
                    
            # elif this_square in current_possible_moves: #MOVING
                
            #     move_made = True
            #     piece = selected.piece
            #     #self.move(piece, coords, True)
            #     self.move(piece, coords, False)
            #     # piece.move(board, coords)
                

                
            #     back_to_default(selected, current_possible_moves)
            #     selected = None                

                
            #     current_possible_moves = []
            #     current_possible_move_coords = []



                
                
                

            # elif selected != None: #CLICKED AWAY FROM PIECE

            #     back_to_default(selected, current_possible_moves)
            #     selected = None
            #     current_possible_moves = set()
            #     current_possible_move_coords = []

        # else:


        # return move_made

    
    def render_screen(self, *, view_direction: str):


        self.screen.fill(WHITE)
        # if DEBUG_MODE:
        #     for x in range(1, 9):
        #         for y in range(1, 9):
        #             board.coords((x, y)).back_to_default_color()
                    
        #     for move in get_team_attack_moves(other_team(board.current_turn), board):
        #         board.coords(move).color = RED
        self.pygame_chess_board.render_board(self.screen, view_direction, self.possible_move_coords)
        

        # match view_direction:
        #     case 'w':
        #         render_taken_piece_log(self.screen, board.taken_white_pieces, (100, 30))
        #         render_taken_piece_log(self.screen, board.taken_black_pieces, (100, HEIGHT - 50))

        #     case 'b':
        #         render_taken_piece_log(self.screen, board.taken_black_pieces, (100, 30))
        #         render_taken_piece_log(self.screen, board.taken_white_pieces, (100, HEIGHT - 50))

        

        if self.board.win_state != '':

            match self.board.win_state:
                case 'w':
                    display_checkmate(self.screen)
                case 'b':
                    display_checkmate(self.screen)
                case 'd':
                    display_draw(self.screen)

            self.disabled = True

        elif self.board.checked['w'] or self.board.checked['b']:
            display_check(self.screen)
        
        

        match self.board.current_turn:
            case "w":
                pygame.display.set_caption("Easy Chess: White Turn")
            case "b":
                pygame.display.set_caption("Easy Chess: Black Turn")


def render_widgets(func):
    def render_widget_func(self: Window, *args, **kwargs):
        return_val = func(self, *args, **kwargs)
        
        for widget in self.widgets:
            widget.render()

        pygame.display.flip()
        return return_val
    
    return render_widget_func
    

def wait_for_move(window: Window, func, *args):

    piece, pos = func(*args)
    if not window.destroyed:

        window.move(piece, pos, is_computer=True)
        window.finished_thread = True


class Against_Move_Source(Window):
    

    @render_widgets
    def render_function(self, events: list[pygame.event.Event]):


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.busy:
                    self.handle_click()



        self.render_screen(view_direction=self.player_side)
        



        if not self.busy and self.board.current_turn != self.player_side and self.board.win_state == '':
            self.busy = True

            self.thread = Thread(target = wait_for_move, args=((self, self.move_source.get_move, self.board)))
            self.thread.start()





    def __init__(self, size: tuple[int, int], player_side: str, move_source: Move_Source, **kwargs):
        self.player_side = player_side
        self.move_source = move_source
        super().__init__(size, self.render_function, **kwargs)

class Same_PC_Multiplayer(Window):

    @render_widgets
    def render_function(self, events: list[pygame.event.Event]):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: #MOUSE CLICK ACTIONS
                self.handle_click()
    

        self.render_screen(view_direction=self.board.current_turn)

        pygame.display.flip()


    def __init__(self, size: tuple[int, int], **kwargs):
        super().__init__(size, self.render_function, **kwargs)


def main_game(window: Window):
    
    while window.update():
        window.clock.tick(FPS)
    pygame.quit()

