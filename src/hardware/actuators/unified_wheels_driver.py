from wheels_driver import left_wheel, right_wheel, MotorController
import numpy as np

'''
Controller di entrambe le ruote.
Le velocita' ammissimibili vanno da -10 a 10. I valori negativi fanno muovere le ruote in senso opposto.
Le direzioni ammissibili vannoda da -3 a 3. I valori -3 e 3 fanno ruotare il robot su se stesso, rispettivamente in 
senso antiorario ed orario. I restanti valori fanno andare il robot piu o meno a sinistra, al centro o piu o meno a
destra. 
'''


def gen_dir_speed_matrix(direction_levels):
    matrix = np.empty((MotorController.SPEED_LEVELS + 1, direction_levels, 2), dtype=np.int0)
    for sp in range(0, MotorController.SPEED_LEVELS + 1):
        for direction in range(0, direction_levels):
            sp1 = sp2 = 0
            if sp != 0:
                sp1 = max(1, min(MotorController.SPEED_LEVELS, int(round(sp - direction))))
                sp2 = max(1, min(MotorController.SPEED_LEVELS, int(round(sp + direction))))
            matrix[sp][direction][0] = sp1
            matrix[sp][direction][1] = sp2
    return matrix


class __UnifiedWheelsDriver(object):
    DIRECTION_LEVELS = 5
    left_wheel = left_wheel
    right_wheel = right_wheel
    __dir_speed_matrix = gen_dir_speed_matrix(DIRECTION_LEVELS)

    def __init__(self):
        self.__speed = 0
        self.__direction = 0
        self.__rotation = 0
        self.__update_wheels_speed()

    def __update_wheels_speed(self):
        if self.__direction == 0:
            self.left_wheel.speed = self.right_wheel.speed = self.__speed
        else:
            sp_mod = abs(self.__speed)
            sp_sign = 1 if self.__speed >= 0 else -1
            dir_mod = abs(self.__direction)
            if dir_mod == self.DIRECTION_LEVELS:
                dir_sign = 1 if self.__direction > 0 else -1
                self.left_wheel.speed = self.__speed * dir_sign
                self.right_wheel.speed = - self.__speed * dir_sign
            else:
                speed_tuple = self.__dir_speed_matrix[sp_mod][dir_mod]
                index1 = 1 if self.__direction > 0 else 0
                self.left_wheel.speed = speed_tuple[index1] * sp_sign
                self.right_wheel.speed = speed_tuple[1 - index1] * sp_sign

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        if direction in range(-self.DIRECTION_LEVELS, self.DIRECTION_LEVELS + 1):
            self.__direction = direction
            self.__update_wheels_speed()
        else:
            raise ValueError("Specificare una direzione nell'intervallo [-%d,%d]"%(self.DIRECTION_LEVELS,
                                                                                   self.DIRECTION_LEVELS))

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed
        self.__update_wheels_speed()

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation):
        if rotation in range(-1, 2):
            self.__rotation = rotation
            self.__update_wheels_speed()
        else:
            raise ValueError("Specificare un valore di rotazione tra -1 (senso antiorario), 0 (nessuna rotazione) e "
                             "1 (senso orario")

    def stop(self):
        self.speed = 0


driver = __UnifiedWheelsDriver()
