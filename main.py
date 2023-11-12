from constants import *
from performance_monitor import log_performance
from game import Against_Move_Source, Same_PC_Multiplayer, main_game
from chess_engine import board, init_board
from move_sources import Minimax
import user_interface.menu as menu
from user_interface.menu import menu, Choice, Quickplay




@log_performance
def main():
        while True:
            choice = menu()

            if choice.type == 'simple':
                match choice.text:
                    case 'minimax':
                        main_game(Against_Move_Source((600, 600), 'w', Minimax('b', 2)))
                    case 'ai':
                        print ('ai')
                    case 'same pc':
                        main_game(Same_PC_Multiplayer((600, 600), undo_enabled=True))

                    case _:
                        break

                
            else:
                match choice.text:
                    case 'quickplay':
                        Quickplay(choice.root).run()
                    case 'tournament':
                        print ('tournament')

                    case _:
                        break
            
            init_board(board)


if __name__ == '__main__':

    main()



