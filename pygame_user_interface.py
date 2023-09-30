import pygame

class Button:
    def __init__(self, screen: pygame.surface.Surface,
                 pos: tuple[int, int], 
                 size: tuple[int, int], 
                 background_color=(255, 255, 255), 
                 text='',
                 text_color=(0, 0, 0),
                 font=pygame.font.SysFont(None, 24)):
        
        self.screen = screen
        self.pos = pos
        self.size = size
        self.background_color = background_color
        self.text = text
        self.text_color = text_color
        self.font = font

    def render(self):

        pygame.draw.rect(self.screen, self.background_color, pygame.rect(*self.pos, *self.size))        

    
if __name__ == '__main__':
    RED = (255, 0, 0)
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    bing_bong = Button(screen, (50, 50), (50, 50), RED, 'bing_bong')