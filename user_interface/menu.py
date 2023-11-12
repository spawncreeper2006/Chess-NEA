from tkinter import *
from PIL import ImageTk
from .loading_screen_wheel import Loading_Screen_Wheel

WIDTH = 600
HEIGHT = 600

def centre(root: Tk):
    root.update_idletasks()
    width = root.winfo_width()
    frm_width = root.winfo_rootx() - root.winfo_x()
    win_width = width + 2 * frm_width
    height = root.winfo_height()
    titlebar_height = root.winfo_rooty() - root.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = root.winfo_screenwidth() // 2 - win_width // 2
    y = root.winfo_screenheight() // 2 - win_height // 2
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.deiconify()

def create_root(title: str) -> Tk:
    root = Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.resizable(False, False)
    root.title(title)
    centre(root)
    return root

def try_destroy(root: Tk):
    try:
        root.destroy()
        
    except TclError:
        pass

class Choice:
    def __init__(self, text: str, root=None):
        self.text = text

        if root == None:
            self.type = 'simple'
        else:
            self.type = 'complex'
            self.root = root

    


class Menu:


    def __init__(self, root: Tk):
        self.root = root
        self.background = PhotoImage(file = r'assets\chess_board.png', master=self.root)
        Label(self.root, image=self.background).place(x=0,y=0)
        # Label(self.root, text=title, font='Arial 25 underline', justify='center', bg='white').place(x=WIDTH//2 - len(title) * 8,y=20)
        self.selection = None

    def run(self):
        self.root.mainloop()
        return self.selection

    def return_and_stop(self, to_return):
        def action_function():
            self.root.quit()
            self.selection = to_return
        return action_function


class Main_Menu(Menu):

    def __init__(self, root: Tk):
        super().__init__(root)
        Button(self.root, text='          Singleplayer          ', font=('Ariel', 15), justify='center', command=self.return_and_stop('singleplayer')).place(x=WIDTH//2 - 100, y=180)
        Button(self.root, text='           Multiplayer           ', font=('Ariel', 15), justify='center', command=self.return_and_stop('multiplayer')).place(x=WIDTH//2 - 100, y=280)
        Button(self.root, text='                Quit                ', font=('Ariel', 15), justify='center', command=self.return_and_stop('quit')).place(x=WIDTH//2 - 100, y=380)
        
class Singleplayer(Menu):
    def __init__(self, root: Tk):
        super().__init__(root)
        Button(self.root, text='             Minimax             ', font=('Ariel', 15), justify='center', command=self.return_and_stop('minimax')).place(x=WIDTH//2 - 100, y=180)
        Button(self.root, text='                 AI                 ', font=('Ariel', 15), justify='center', command=self.return_and_stop('ai')).place(x=WIDTH//2 - 100, y=280)
        Button(self.root, text='               Back               ', font=('Ariel', 15), justify='center', command=self.return_and_stop('back')).place(x=WIDTH//2 - 100, y=380)


class Multiplayer(Menu):
    def __init__(self, root: Tk):
        super().__init__(root)
        Button(self.root, text='             Quickplay        ', font=('Ariel', 15), justify='center', command=self.return_and_stop('quickplay')).place(x=WIDTH//2 - 100, y=180)
        Button(self.root, text='           Tournament        ', font=('Ariel', 15), justify='center', command=self.return_and_stop('tournament')).place(x=WIDTH//2 - 100, y=280)
        Button(self.root, text='             Same PC         ', font=('Ariel', 15), justify='center', command=self.return_and_stop('same pc')).place(x=WIDTH//2 - 100, y=380)
        Button(self.root, text='                Back            ', font=('Ariel', 15), justify='center', command=self.return_and_stop('back')).place(x=WIDTH//2 - 100, y=480)

class Quickplay(Menu):
    def __init__(self, root: Tk):

        super().__init__(root)
        for widget in root.winfo_children():
            widget.destroy()


        #Text(root, text='Waiting for Players').place(x=10, y=10)
        
        Label(root, text='Waiting For Players...', font=('Calibri 20')).place(x=WIDTH // 2 - 100, y=130)
        canvas = Canvas(root, width=WIDTH, height=HEIGHT // 2)
        canvas.place(x=0, y=HEIGHT // 2)
        Loading_Screen_Wheel(canvas, 30, (WIDTH//2, HEIGHT//4), 100)


'''
return vals for main_menu
minimax
ai
quickplay
tournament
same pc
quit
'''

def menu() -> Choice:

    root = create_root('main menu')

    while True:

        match Main_Menu(root).run():
            case 'singleplayer':

                x = Singleplayer(root).run()
                if x == '':
                    return Choice('')
                
                elif x != 'back':
                    
                    try_destroy(root)
                    return Choice(x)
                
            case 'multiplayer':

                x = Multiplayer(root).run()
                if x == 'back':
                    continue

                elif x == '':
                    return Choice('')
                
                else:
                    return Choice(x, root)
            
            case _:
                return Choice('quit')
            


