from constants import *
from performance_monitor import log_performance
from game import Against_Move_Source, Same_PC_Multiplayer, main_game
from chess_engine import board, init_board
from chess_client import Connection, establish_quickplay_connection, establish_tournament_connection
from move_sources import Minimax, Quickplay
from user_interface.menu import menu, Choice, Quickplay_Menu
from threading import Thread
from typing import Callable
import user_interface.menu as menu
from tkinter import Tk


def quickplay_conn(kill: Callable, start_info: dict) -> tuple[Connection, str]:
    conn, team = establish_quickplay_connection()

    kill()
    start_info['conn'] = conn
    start_info['team'] = team

# def kill_ui_from_thread_func(root: Tk) -> Callable[[], None]:
#     def func():
#         root.quit()
#         root.update()
#     return func


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
                        print ('this was selected')
                        main_game(Same_PC_Multiplayer((600, 600), undo_enabled=True))

                    case _:
                        break

                
            else:
                match choice.text:
                    case 'quickplay':
                        quickplay = Quickplay_Menu(choice.root)

                        start_info = {}
                        thread = Thread(target=quickplay_conn, args=(quickplay.kill_ui, start_info, ))
                        thread.start()
                        quickplay.run()
                        thread.join()
                        #print (start_info['conn'], start_info['team'], 'this now works')
                        main_game(Against_Move_Source((600, 600), start_info['team'], Quickplay(start_info['conn'])))
                        start_info['conn'].close()
 
                    case 'tournament':
                        print ('tournament')

                    case _:
                        break
            
            init_board(board)


if __name__ == '__main__':

    main()



