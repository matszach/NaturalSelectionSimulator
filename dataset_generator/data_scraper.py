import numpy as np
import pandas as pd
import game_constants as gc
import entities.entity_constants as ec


# reads data from entity lists
# exports it to .csv file
class DataScraper:

    # reads one sample
    def get_sample(self):

        num_cr = len(self.creatures)
        num_fd = len(self.foods)

        sample = [num_cr, num_fd]
        self.population_data.append(sample)
        
        creature_sample = []
        for creature in self.creatures:
            c = [creature.size, creature.speed, creature.energy]
            creature_sample.append(c)

        self.creature_data.append(creature_sample)

    # saves dataset to .csv
    def save(self):
        
        df = pd.DataFrame(self.population_data, columns=self.population_columns)
        df.to_csv('data/session_data.csv')
        
        for i, sd in enumerate(self.creature_data):
            sdf = pd.DataFrame(sd, columns=self.creature_columns)
            sdf.to_csv(f'data/creature_data/creature_data_{i}.csv')

    # save settings
    def save_settings(self):

        settings_saved = []
        settings_saved.append('================================================')
        settings_saved.append(f'Total frames: {gc.frames_per_session}')
        settings_saved.append(f'Frames per sample: {gc.frames_per_sample}')
        settings_saved.append('================================================')
        settings_saved.append(f'Food spawn chance: {gc.food_spawn_chance*100}%')
        settings_saved.append(f'Starting creatures: {gc.starting_creatures}')
        settings_saved.append('================================================')
        settings_saved.append(f'Energy range: {ec.res_min} - {ec.res_max}, starting value: {ec.res_base}')
        settings_saved.append(f'Trait level range: {ec.tr_min} - {ec.tr_max}')
        settings_saved.append(f'Replication cost: {ec.replication_cost}')
        settings_saved.append(f'Predation against creatures up to {ec.carnivore_size_ratio*100}% of predator\'s size')
        settings_saved.append('================================================')
        settings_saved.append(f'Speed {ec.min_dist}px/f ({ec.min_speed_upkeep}en/f) - {ec.max_dist}px/f ({ec.max_speed_upkeep}en/f)')
        settings_saved.append(f'Size {ec.min_dist}px/f ({ec.min_size_upkeep}en/f) - {ec.max_dist}px/f ({ec.max_size_upkeep}en/f)')

        

        settings_file = open('data/settings.txt', 'w+')
        for line in settings_saved:
            settings_file.write(line+'\n')

    # constructor
    def __init__(self, creatures, foods):

        # references to game's entity lists
        self.creatures = creatures
        self.foods = foods

        self.population_columns = ['num. of creatures', 'num. of foods']
        self.population_data = []
        
        self.creature_columns = ['size', 'speed', 'energy']
        self.creature_data = []

