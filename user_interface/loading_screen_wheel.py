from tkinter import Canvas
import tkinter as tk


PI = 3.141592654


def fact(x: int) -> int:
    if x <= 1:
        return 1
    else:
        return x * fact(x - 1)

def is_even(x: int) -> bool:
    return x % 2 == 0


def sin_aprox(x: float, n: int) -> float:

    if n < 0:
        return 0
    else:

        return (1 if is_even(n) else -1) * x ** (2 * n + 1) / fact(2 * n + 1) + sin_aprox(x, n - 1)

def cos_aprox(x: float, n: int) -> float:
    if n < 0:
        return 0
    else:
        return (1 if is_even(n) else -1) * x ** (2 * n) / fact(2 * n) + cos_aprox(x, n - 1)
    

def sin(x: float, n=7) -> float:
    return sin_aprox(x % (2 * PI), n)

def cos(x: float, n=8) -> float:
    return cos_aprox(x % (2 * PI), n)

def tan(x: float) -> float:
    return sin(x) / cos(x)



def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return '#' + ''.join([hex(int(i))[2:].zfill(2) for i in rgb])


DOT_RAD = 10


class Loading_Screen_Wheel:
    def __init__(self, canvas: Canvas, radius: float, center: tuple[int, int], refresh_rate_ms: int):
        self.stage = 0

        self.canvas = canvas
        self.dots = [(radius * sin(x*PI/4) + center[0], radius * cos(x*PI/4) + center[1]) for x in range(8)]
        self.refresh_rate_ms = refresh_rate_ms
        self.canvas.after(0, self.run_loading_screen)

    def draw_loading_screen(self, stage: int):
        self.canvas.delete('all')
        brightnesses = [-255 * (x % 8) / 8 + 255 for x in range (stage, stage + 8)]

        for (x, y), brightness in zip(self.dots, brightnesses):
            self.canvas.create_oval(x - DOT_RAD / 2, y - DOT_RAD / 2, x + DOT_RAD / 2, y + DOT_RAD / 2, fill = rgb_to_hex([brightness] * 3))

    def run_loading_screen(self):
        

        self.stage += 1
        self.stage %= 8

        self.draw_loading_screen(self.stage)



        self.canvas.after(self.refresh_rate_ms, self.run_loading_screen)

        # time.sleep(self.refresh_rate_ms / 1000)



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x400')
    canvas = tk.Canvas(root, width=200, height=200, borderwidth=0, highlightthickness=0, bg="black")
    canvas.pack()

    lsw = Loading_Screen_Wheel(canvas, 30, (100, 100), 100)

    root.mainloop()
