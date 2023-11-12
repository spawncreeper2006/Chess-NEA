from constants import *
from performance_monitor import log_performance
from game import Against_Move_Source, Same_PC_Multiplayer, main_game
from chess_engine import board, init_board
from chess_client import Connection, establish_quickplay_connection, establish_tournament_connection
from move_sources import Minimax
from user_interface.menu import menu, Choice, Quickplay
from threading import Thread
from typing import Callable
import user_interface.menu as menu


def quickplay_conn(kill: Callable) -> tuple[Connection, str]:
    conn, team = establish_quickplay_connection()
    kill()
    return conn, team



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
                        thread = Thread(target=quickplay_conn, args=(choice.root.destroy, ))
                        thread.start()
                        Quickplay(choice.root).run()
                        thread.join()
 
                    case 'tournament':
                        print ('tournament')

                    case _:
                        break
            
            init_board(board)


if __name__ == '__main__':

    main()



