import pygame
import entities.entity_util as eu
import entities.entity_constants as ec
from random import random


# =========================== BASE ENTITY ===========================
# parent class for every entity
class Entity:

    # actions that Entity takes every turn
    # base class has none to take
    def take_action(self):
        pass

    # scales image to current entity size
    # draws image on game screen
    def draw(self, screen):
        pass

    # called in pygame main loop every game frame
    def update(self, screen):
        self.take_action()
        self.draw(screen)

    # constructor
    def __init__(self, x=0, y=0):

        # current location
        self.x = x
        self.y = y


# ============================ CREATURE ENTITY ===========================
# representation of a living organism
class CreatureEntity(Entity):

    # checks creature's traits
    # pays energy upkeep for those traits
    def pay_upkeep(self):
        self.energy -= eu.get_upkeep_cost(self.size, self.speed)

    # checks creature's energy.
    # if its energy reaches 0 it expires and returns True
    def expire(self):
        if self.energy < ec.res_min:
            self.creatures.remove(self)
            return True
        else:
            return False

    # checks nearby entities
    # consumes first available (if any)
    # and returns True if successful
    def consume(self):
        # check foods
        for food in self.foods:
            distance = pow(pow(abs(food.x - self.x), 2) + pow(abs(food.y - self.y), 2), 0.5)
            if distance < eu.get_creature_radius(self.size):
                self.foods.remove(food)
                self.energy += food.value
                return True

        for crt in self.creatures:
            distance = pow(pow(abs(crt.x - self.x), 2) + pow(abs(crt.y - self.y), 2), 0.5)
            if distance < eu.get_creature_radius(self.size):
                if crt.size < self.size*ec.carnivore_size_ratio:
                    self.creatures.remove(crt)
                    self.energy += crt.energy
                    return True

        return False

    # checks for creature's replication chance,
    # if successful, returns True
    def replicate(self):
        if random() < eu.get_replication_chance(self.energy):
            self.energy -= ec.replication_cost
            new_size = self.size + eu.get_spawn_mutation_offset()
            new_speed = self.speed + eu.get_spawn_mutation_offset()
            offspring = CreatureEntity(self.creatures, self.foods, size=new_size, speed=new_speed, energy=ec.replication_cost)
            offspring.x = self.x + eu.get_spawn_position_offset()
            offspring.y = self.y + eu.get_spawn_position_offset()
            self.creatures.append(offspring)
            return True
        else:
            return False

    # checks for closest food source
    # if successful, move in it's direction and return True
    def chase_food(self):
        current = (-1000, -1000)
        for food in self.foods:
            x_dir = food.x - self.x
            y_dir = food.y - self.y
            if abs(x_dir) + abs(y_dir) < abs(current[0]) + abs(current[1]):
                current = x_dir, y_dir
        for crt in self.creatures:
            x_dir = crt.x - self.x
            y_dir = crt.y - self.y
            if abs(x_dir) + abs(y_dir) < abs(current[0]) + abs(current[1]) \
                    and crt.size < self.size*ec.carnivore_size_ratio:
                current = x_dir, y_dir

        if abs(current[0]) + abs(current[1]) > 1000:
            return False

        if current[0] > 0:
            self.x += eu.get_distance_travelled(self.speed)
        elif current[0] < 0:
            self.x -= eu.get_distance_travelled(self.speed)

        if current[1] > 0:
            self.y += eu.get_distance_travelled(self.speed)
        elif current[1] < 0:
            self.y -= eu.get_distance_travelled(self.speed)

        return True

    def take_action(self):

        # limit energy
        if self.energy > ec.res_max:
            self.energy = ec.res_max

        # pay upkeep
        self.pay_upkeep()

        # break if creature expires
        if self.expire():
            return
        # break if creature consumes food
        if self.consume():
            return
        # break if creature replicates
        if self.replicate():
            return

        # move after the closes food source
        self.chase_food()

    # draws creature shape according to it's traits
    # self.size - dictates the size of the body
    # self.speed - dictates color
    # self.sense - dictates the size of the eye
    def draw(self, screen):
        color = eu.get_creature_color(self.speed)
        location = (round(self.x), round(self.y))
        radius = eu.get_creature_radius(self.size)
        pygame.draw.circle(screen, color, location, radius)
        eye_color = ec.creature_eye_color
        eye_radius = eu.get_creature_eye_radius(self.energy, radius)
        pygame.draw.circle(screen, eye_color, location, eye_radius)

    # constructor
    def __init__(self, creatures, foods, size=ec.tr_base, speed=ec.tr_base, energy=ec.res_base):
        Entity.__init__(self)

        # References to other entities
        self.creatures = creatures
        self.foods = foods

        # Energy - used for movement and reproduction.
        # At 0 energy the creature dies.
        self.energy = energy

        # Size -  bigger creature can consume smaller creatures.
        # Movement costs are greater for bigger creatures.
        self.size = size
        if self.size > ec.tr_max:
            self.size = ec.tr_max
        elif self.size < ec.tr_min:
            self.size = ec.tr_min

        # Speed - creature's rate of movement. Faster creatures
        # use more energy per distance travelled but may get to food before other creatures
        self.speed = speed
        if self.speed > ec.tr_max:
            self.speed = ec.tr_max
        elif self.speed < ec.tr_min:
            self.speed = ec.tr_min


# ============================ FOOD ENTITY ===========================
# representation of food for creature entities
class FoodEntity(Entity):

    # draws food shape according to it's value
    # self.value - dictates radius
    def draw(self, screen):
        color = ec.food_color
        location = (self.x, self.y)
        radius = eu.get_food_radius(self.value)
        pygame.draw.circle(screen, color, location, radius)

    # constructor
    def __init__(self):
        Entity.__init__(self)

        # Value - amount of energy that consuming the food
        # gives to a creature.
        self.value = eu.get_food_value()






