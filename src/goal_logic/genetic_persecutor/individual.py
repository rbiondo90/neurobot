import numpy as np
import time

class Individual:
    TO_IDX_STATE = {"lwheel_speed": 0, "rwheel_speed": 1, "lwheel_dir": 2, "rwheel_dir": 3,
                    "lwheel_speed_prev": 4, "rwheel_speed_prev": 5, "lwheel_dir_prev": 6,
                    "rwheel_dir_prev": 7, "object_detected": 8, "object_h_position": 9, "object_distance": 10,
                    "object_detected_prev": 11, "object_h_position_prev": 12, "object_distance_prev": 13}
    TO_IDX_OUT = {"lwheel_speed": 0, "rwheel_speed": 1, "lwheel_dir": 2, "rwheel_dir": 3}

    def __init__(self, number, left_wheel, right_wheel, watcher, max_actions, minimum_action_pause, chromosomes=None):
        self.number = number
        self.fitness = 0.
        self.actions_taken = 0
        self.max_actions = max_actions
        self.minimum_action_pause = minimum_action_pause
        self.watcher = watcher
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.min_distance_reached = 1
        self.never_found = True
        if chromosomes is None:
            chromosomes = np.random.uniform(-5., 5.,(4, 14))
        self.chromosomes = chromosomes
        self.state = None

    def update_state(self):
        state = np.empty((14,))
        prev_state = self.state if self.actions_taken > 0 else state
        state[self.TO_IDX_STATE["lwheel_speed"]] = float(self.left_wheel.get_speed()) / 10
        state[self.TO_IDX_STATE["rwheel_speed"]] = float(self.right_wheel.get_speed()) / 10
        state[self.TO_IDX_STATE["lwheel_dir"]] = float(self.left_wheel.get_direction())
        state[self.TO_IDX_STATE["rwheel_dir"]] = float(self.right_wheel.get_direction())
        state[self.TO_IDX_STATE["lwheel_speed_prev"]] = prev_state[self.TO_IDX_STATE["lwheel_speed"]]
        state[self.TO_IDX_STATE["rwheel_speed_prev"]] = prev_state[self.TO_IDX_STATE["rwheel_speed"]]
        state[self.TO_IDX_STATE["lwheel_dir_prev"]] = prev_state[self.TO_IDX_STATE["lwheel_dir"]]
        state[self.TO_IDX_STATE["rwheel_dir_prev"]] = prev_state[self.TO_IDX_STATE["rwheel_dir"]]

        detected, distance, hpos = self.watcher.watch()
        state[self.TO_IDX_STATE["object_detected"]] = 1. if detected else 0.
        state[self.TO_IDX_STATE["object_h_position"]] = hpos if hpos is not None else 0.
        state[self.TO_IDX_STATE["object_distance"]] = distance if distance is not None else 1.
        state[self.TO_IDX_STATE["object_detected_prev"]] = prev_state[self.TO_IDX_STATE["object_detected"]]
        state[self.TO_IDX_STATE["object_h_position_prev"]] = prev_state[self.TO_IDX_STATE["object_h_position"]]
        state[self.TO_IDX_STATE["object_distance_prev"]] = prev_state[self.TO_IDX_STATE["object_distance"]]

        self.state = state

    def update_fitness(self):
        distance = self.state[self.TO_IDX_STATE["object_distance"]]
        distance_bonus = 0
        # if self.never_found and self.state[self.TO_IDX_STATE["object_detected"]]:
        #     self.fitness += 5
        #     self.never_found = False
        if self.min_distance_reached - distance > 0.1:
            distance_bonus = 10 * (self.min_distance_reached - distance)
            self.min_distance_reached = distance
        elif distance - self.min_distance_reached > 0.2:
            distance_bonus = 0.5 * (self.min_distance_reached - distance)
        self.fitness += distance_bonus
        if self.fitness < 0 or self.actions_taken == self.max_actions:
            self.actions_taken = self.max_actions
            self.fitness += min(5., 1./max(0.1,self.min_distance_reached))

    def initialize_state(self):
        self.update_state()
        min_dist = self.watcher.watch()[1]
        self.min_distance_reached = min_dist if min_dist is not None else 1

    def advance(self):
        if self.state is None:
            self.initialize_state()
        if not self.goal_reached():
            outputs = np.matmul(self.chromosomes, self.state)
            self.left_wheel.set_speed(int(np.clip(outputs[self.TO_IDX_OUT["lwheel_speed"]], 1, 3)))
            self.right_wheel.set_speed(int(np.clip(outputs[self.TO_IDX_OUT["rwheel_speed"]], 1, 3)))
            lwheel_dir = np.rint(np.clip(outputs[self.TO_IDX_OUT["lwheel_dir"]], -1, 1))
            rwheel_dir = np.rint(np.clip(outputs[self.TO_IDX_OUT["rwheel_dir"]], -1, 1))

            def decide_wheel_dir(wheel, numeric_dir):
                function = wheel.backwards if numeric_dir == -1 else wheel.stop if numeric_dir == 0 else wheel.forward
                function()

            decide_wheel_dir(self.left_wheel, lwheel_dir)
            decide_wheel_dir(self.right_wheel, rwheel_dir)

            self.actions_taken += 1
            self.update_state()
            if self.state[self.TO_IDX_STATE["object_distance"]] < 0.1:
                self.left_wheel.stop()
                self.right_wheel.stop()
            self.update_fitness()

    def live(self):
        self.left_wheel.set_speed(2)
        self.right_wheel.set_speed(2)
        self.left_wheel.forward()
        self.right_wheel.backwards()
        while not self.watcher.watch()[0]:
            pass
        if self.state is None:
            self.initialize_state()
        while self.actions_taken < self.max_actions and not self.goal_reached():
            time_before_action = time.time()
            self.advance()
            time_passed = time.time() - time_before_action
            if time_passed < self.minimum_action_pause:
                time.sleep(self.minimum_action_pause - time_passed)
        print("Individuo %d fitness finale %d" % (self.number, self.fitness))
        if self.state[self.TO_IDX_STATE["object_distance"]] < 0.2:
            self.right_wheel.set_speed(3)
            self.left_wheel.set_speed(3)
            self.right_wheel.backwards()
            self.left_wheel.backwards()
            time.sleep(1)
        self.left_wheel.stop()
        self.right_wheel.stop()

    def goal_reached(self):
        #return self.state[self.TO_IDX_STATE["object_distance"]] <= 0.05
        return False

    def reset(self):
        self.fitness = 0.
        self.actions_taken = 0
        self.state = None
        self.min_distance_reached = 1.