import pygame
import game_constants as gc


# displays
class InfoDisplay:

    def draw_info(self, screen, current_frame):
        frame_info = self.font.render(f'Frame: {current_frame}/{gc.frames_per_session}', False, gc.text_color)
        screen.blit(frame_info, (7, 7))
        cr_info = self.font.render(f'Creatures: {len(self.creatures)}', False, gc.text_color)
        screen.blit(cr_info, (7, 7+gc.font_size*1.2))
        food_info = self.font.render(f'Food: {len(self.foods)}', False, gc.text_color)
        screen.blit(food_info, (7, 7+gc.font_size*2.4))

    # constructor
    def __init__(self, creatures, foods):

        # references to entity lists
        self.creatures = creatures
        self.foods = foods

        # font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', gc.font_size)
