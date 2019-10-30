
class Goer:

    def __init__(self, watcher, wheels_driver):
        self.watcher = watcher
        self.driver = wheels_driver


    def go(self):
        arrived = False
        while True:
            recognized, distance, h_pos = self.watcher.watch()
            if not recognized:
                self.rotate_until_found()
            else:
                arrived = True if distance < 0.02 else False
                if not arrived:
                    self.driver.direction = int(round(h_pos * 3))
                    self.driver.speed = int(10 * distance)
                else:
                    if abs(h_pos) < 0.05:
                        self.driver.speed = 0
                        self.driver.direction = 0
                    else:
                        self.driver.direction = -3 if h_pos < 0 else 3
                        self.driver.speed = int(10 * distance ** 2)
        #self.driver.speed = 0
        #elf.driver.direction = 0


    def rotate_until_found(self):
        recognized = False
        h_pos = 1
        while not recognized and abs(h_pos) > 0.05:
            self.driver.direction = 3
            self.driver.speed = 6
            recognized, distance, h_pos = self.watcher.watch()
            if h_pos is None:
                h_pos = 1
        self.driver.direction = 0
        self.driver.speed = 0


