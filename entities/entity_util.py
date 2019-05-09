from random import random
import entities.entity_constants as ec


# =========================== Creature Functions ===========================

def get_spawn_position_offset():
    if random() > 0.5:
        return ec.spawn_position_offset
    else:
        return -ec.spawn_position_offset


def get_spawn_mutation_offset():
    if random() > 0.5:
        return ec.spawn_mutation_offset
    else:
        return -ec.spawn_mutation_offset


def get_replication_chance(cur_energy):
    return (cur_energy - 80)/(ec.res_max - 80)


def get_distance_travelled(cr_speed):
    dist = (cr_speed - ec.tr_min)/(ec.tr_max - ec.tr_min) * (ec.max_dist-ec.min_dist) + ec.min_dist
    return dist


def get_upkeep_cost(cr_size, cr_speed):
    size_cost = (cr_size - ec.tr_min)/(ec.tr_max - ec.tr_min) * (ec.max_size_upkeep-ec.min_size_upkeep) + ec.min_size_upkeep
    speed_cost = (cr_speed - ec.tr_min)/(ec.tr_max - ec.tr_min) * (ec.max_speed_upkeep-ec.min_speed_upkeep) + ec.min_speed_upkeep
    return size_cost+speed_cost


# =========================== Creature Creation ===========================

# random trait level
def get_random_trait_level():
    return random()*(ec.tr_max-ec.tr_min) + ec.tr_min


# =========================== Creature Shape ===========================

# returns rgb tuple based on creature's speed
def get_creature_color(cr_speed):
    r = (cr_speed - ec.tr_min)/(ec.tr_max - ec.tr_min) * ec.max_rgb
    g = ec.min_rgb
    b = ec.max_rgb - r
    return r, g, b


# returns radius based on creature's size
def get_creature_radius(cr_size):
    radius = cr_size / ec.tr_max * (ec.max_cr_rad - ec.min_cr_rad) + ec.min_cr_rad
    return round(radius)


def get_creature_eye_radius(cr_energy, cr_body_radius):
    ratio = cr_energy / ec.res_max * (ec.max_eye_ratio - ec.min_eye_ratio) + ec.min_eye_ratio
    eye_radius = cr_body_radius * ratio
    return round(eye_radius)


# =========================== Food Value ===========================

# returns random food value from range
def get_food_value():
    val = random()*(ec.val_max-ec.val_min)+ec.val_min
    return val


# =========================== Food Shape ===========================

# returns radius based on food's value
def get_food_radius(food_value):
    radius = food_value / ec.val_max * (ec.max_food_rad - ec.min_food_rad) + ec.min_food_rad
    return round(radius)
