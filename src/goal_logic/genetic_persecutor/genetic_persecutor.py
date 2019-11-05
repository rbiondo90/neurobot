from utils.generic import defaults
import os
import numpy as np
from configparser import ConfigParser
import random
from hardware.actuators.wheels_driver import left_wheel, right_wheel
from hardware.sensors.pi_camera import PiCameraWrapper
from recognizers.distance_interpolator import DistanceInterpolator
from watcher.watcher import Watcher
from generation import Generation
from individual import Individual

__TRAINING_DATA_PATH = os.path.join(defaults.AI_MODELS_DIRECTORY, os.path.basename(__file__).split(".")[0])


class GeneticPersecutor:
    __TRAINING_DATA_PATH = os.path.join(defaults.AI_MODELS_DIRECTORY, os.path.basename(__file__).split(".")[0])

    def __init__(self, name, individuals_per_generation=20, mating_pool_size=0.4, mutation_rate=0.2,
                 max_actions_per_individual=20, min_time_between_actions=0.05, left_wheel=left_wheel,
                 right_wheel=right_wheel, watcher=None):
        global __TRAINING_DATA_PATH
        if watcher is None:
            watcher = Watcher()
        self.training_data_path = os.path.join(self.__TRAINING_DATA_PATH, name)
        self.network_settings_file = os.path.join(self.training_data_path, "config.ini")
        self.watcher = watcher
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.max_actions_per_individual = max_actions_per_individual
        self.min_time_between_actions = min_time_between_actions
        if not os.path.isdir(self.training_data_path):
            os.mkdir(self.training_data_path)
        if os.path.isfile(self.network_settings_file):
            config = ConfigParser()
            config.read(self.network_settings_file)
            self.individuals_per_generation = config.getint("main", "ipg")
            self.mating_pool_size = config.getint("main", "mps")
            self.mutation_rate = config.getfloat("main", "mr")
            self.current_generation_number = config.getint("main", "cr")
        else:
            self.individuals_per_generation = individuals_per_generation
            self.mating_pool_size = int(np.floor(mating_pool_size * individuals_per_generation))
            self.mutation_rate = mutation_rate
            self.current_generation_number = 0
            self.current_generation = None
        self.current_generation_path = self.__prepare_generations_directory()
        self.advance_generation()

    def __store_config(self):
        config = ConfigParser()
        config.add_section("main")
        config.set("main", "ipg", str(self.individuals_per_generation))
        config.set("main", "mps", str(self.mating_pool_size))
        config.set("main", "mr", str(self.mutation_rate))
        config.set("main", "cr", str(self.current_generation_number))
        with open(self.network_settings_file) as f:
            config.write(f)

    def __prepare_generations_directory(self):
        dir_path = self.gen_dir_from_number()
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        return dir_path

    def generate_individuals(self):
        if self.current_generation_number == 1:
            individuals = [Individual(i + 1, self.left_wheel, self.right_wheel, self.watcher,
                                      self.max_actions_per_individual, self.min_time_between_actions)
                           for i in range(self.individuals_per_generation)]
        else:
            individuals = self.current_generation.get_best_n_individuals(self.mating_pool_size)
            for individual in individuals:
                individual.reset()
            individuals += self.mate(individuals)
            random.shuffle(individuals)
            for i in range(len(individuals)):
                individuals[i].number = i + 1
        return individuals

    def mate(self, mating_pool):
        mating_pool_len = len(mating_pool)
        mating_number = self.individuals_per_generation - mating_pool_len
        new_individuals = []
        for i in range(mating_number):
            son_chromosomes = np.empty((4, 14))
            parents_chromosomes = [parent.chromosomes for parent in random.sample(mating_pool, 2)]
            for row in range(len(parents_chromosomes)):
                son_chromosome = random.choice(parents_chromosomes)[row]
                if random.random() >= 1 - self.mutation_rate:
                    son_chromosome += np.random.uniform(-0.3, 0.3,(14,))
                son_chromosomes[row] = son_chromosome
            new_individuals.append(Individual(i + mating_pool_len, self.left_wheel, self.right_wheel,
                                              self.watcher, self.max_actions_per_individual,
                                              self.min_time_between_actions, son_chromosomes))
        return new_individuals

    def advance_generation(self):
        # load from file if exists
        self.current_generation_number += 1
        individuals = self.generate_individuals()
        self.current_generation = Generation(self.current_generation_number, individuals)

    def execute_next_individual(self):
        self.current_generation.advance()

    def execute_current_generation(self):
        self.current_generation.execute()

    def gen_dir_from_number(self):
        range_start = (self.current_generation_number // 100) * 100 + 1
        range_end = range_start + 100
        return os.path.join(self.__TRAINING_DATA_PATH, "%d_%d" % (range_start, range_end))

    def execute_generations(self, n):
        for _ in range(n):
            self.execute_current_generation()
            print([individual.fitness for individual in gp.current_generation.get_best_n_individuals(4)])
            self.advance_generation()


if __name__ == "__main__":
    camera = PiCameraWrapper()
    watcher = Watcher(camera=camera, distance_calculator=DistanceInterpolator("brandina.json"))
    gp = GeneticPersecutor("first_try", watcher=watcher)