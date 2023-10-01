import pygame
import typing


class Button:
    def __init__(self,
                 *,
                 screen: pygame.surface.Surface,
                 pos: tuple[int, int],
                 click_action: typing.Callable[[], None],
                 padding = (10, 10),
                 background_color=(255, 255, 255), 
                 text='',
                 text_color=(0, 0, 0),
                 font=None):
        
        try:
            if font == None:
                self.font = pygame.font.SysFont(None, 24)
            self.pygame_text = self.font.render(text, True, text_color)
        except:
            pygame.font.init()
            if font == None:
                self.font = pygame.font.SysFont(None, 24)
            self.pygame_text = self.font.render(text, True, text_color)


        self.screen = screen
        self.pos = pos
        self.click_action = click_action
        self.padding = padding
        self.background_color = background_color
        self.text = text
        self.text_color = text_color
        self.font = font
        

        self.text_rect = self.pygame_text.get_rect()
        self.text_rect[0] = self.pos[0]
        self.text_rect[1] = self.pos[1]

        self.padded_rect = self.text_rect[:]
        self.padded_rect[0] = self.text_rect[0] - self.padding[0]
        self.padded_rect[1] = self.text_rect[1] - self.padding[1]
        self.padded_rect[2] = self.text_rect[2] + self.padding[0] * 2
        self.padded_rect[3] = self.text_rect[3] + self.padding[1] * 2


        

    def render(self):

        pygame.draw.rect(self.screen, self.background_color, self.padded_rect)
        self.screen.blit(self.pygame_text, self.text_rect)

    def check_click(self, coords: tuple[int, int, int, int]) -> bool:
        if (coords[0] > self.padded_rect[0] and coords[1] > self.padded_rect[1]) and (coords[0] < (self.padded_rect[0] + self.padded_rect[2]) and coords[1] < (self.padded_rect[1] + self.padded_rect[3])):
            self.click_action()
            return True
        else:
            return False

# def ca():
#     print ('hello world')


    
# if __name__ == '__main__':
#     clock = pygame.time.Clock()
#     RED = (255, 0, 0)
#     screen = pygame.display.set_mode((400, 400))

#     bing_bong = Button(screen, (50, 50), ca, text='bing_bong', background_color=RED)
#     pygame.init()
#     while True:

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()

#             elif event.type == pygame.MOUSEBUTTONDOWN:
                
#                 bing_bong.check_click(pygame.mouse.get_pos())
            
#         screen.fill((255, 255, 255))
#         bing_bong.render()
        
#         clock.tick(60)
#         pygame.display.flip()