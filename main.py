import pygame
import sys
import game_constants as gc
from entities.spawner import Spawner
from dataset_generator.data_scraper import DataScraper
from info_display.info_display import InfoDisplay


# =========================== ENTITIES ===========================

# for each entity in those an "update" method is called on every game frame
creatures = []
foods = []
spawner = Spawner(creatures, foods, gc.window_size[0], gc.window_size[1])


# =========================== DATA ===========================
current_frame = 0
data_scraper = DataScraper(creatures, foods)

# =========================== DISPLAY ===========================
info_display = InfoDisplay(creatures, foods)

# =========================== GAME INIT ===========================

# main game screen
main_game_screen = pygame.display.set_mode(gc.window_size)

# set app name
pygame.display.set_caption('Natural Selection')

# spawn starting creatures
for i in range(gc.starting_creatures):
    spawner.spawn_creature(default_traits=False)

# =========================== MAIN GAME LOOP ===========================

# finishing of this loop closes the app
game_running = True

while game_running:

    # save data
    if current_frame % gc.frames_per_sample == 0:
        data_scraper.get_sample()

    if current_frame >= gc.frames_per_session:
        data_scraper.save()
        data_scraper.save_settings()
        sys.exit()  # TODO

    # game speed / 'frame-rate'
    pygame.time.delay(gc.game_speed)

    # list of events (keyboard / mouse presses)
    for event in pygame.event.get():

        # if QUIT (X pressed) -> close the app
        if event.type == pygame.QUIT:
            sys.exit()

    # "clears" the screen by filling it with background color
    main_game_screen.fill(gc.background_color)

    # spawns food
    spawner.spawn_food(gc.food_spawn_chance)

    # calls "update" for each entity
    for f in foods:
        f.update(main_game_screen)
    for c in creatures:
        c.update(main_game_screen)

    # display info
    info_display.draw_info(main_game_screen, current_frame)

    # increment current frame
    current_frame += 1

    # draws on display
    pygame.display.update()
