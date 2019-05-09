from random import random
from entities.entity import CreatureEntity
from entities.entity import FoodEntity
from entities.entity_util import get_random_trait_level as rtl


class Spawner:

    def spawn_creature(self, spawn_chance=1, default_traits=True):

        # skip this call if spawn chance "roll" fails
        # (by default it never fails)
        if random() > spawn_chance:
            return

        x = random()*(self.width-40)+20
        x = round(x)
        y = random()*(self.height-40)+20
        y = round(y)

        if default_traits:
            creature = CreatureEntity(self.creatures, self.foods)
        else:
            creature = CreatureEntity(self.creatures, self.foods, size=rtl(), speed=rtl())
        creature.x = x
        creature.y = y
        self.creatures.append(creature)
        
    def spawn_food(self, spawn_chance=1):

        # skip this call if spawn chance "roll" fails
        # (by default it never fails)
        if random() > spawn_chance:
            return

        x = random()*(self.width-40)+20
        x = round(x)
        y = random()*(self.height-40)+20
        y = round(y)
        food = FoodEntity()
        food.x = x
        food.y = y
        self.foods.append(food)

    def __init__(self, creatures, foods, width=1250, height=700):

        # appendable list of entities
        self.creatures = creatures
        self.foods = foods

        # used for determining Entity spawn range
        self.width = width
        self.height = height

