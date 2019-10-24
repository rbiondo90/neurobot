import cv2
from utils import util


class Camera:

    def __init__(self, device=0):
        self.__devid = device
        self.dev = cv2.VideoCapture(device)
        self.setup()

    def setup(self):
        if not self.dev.isOpened():
            self.dev.open(self.__devid)
            print("Device opened")

    def get_image(self, gray=False):
        ret, frame = self.dev.read()
        if ret:
            if gray:
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    def release(self):
        self.dev.release()
        print("Device released")

    def show_image(self, window_title ='', gray = False):
        self.setup()
        util.imshow(window_title, self.get_image(gray), lambda : self.release())

    def show_video(self, title = '', frame_interval = 1, frame_elaboration_function=None):
        self.setup()
        def imageUpdateFunction():
            image = self.get_image()
            if frame_elaboration_function is not None:
                image = frame_elaboration_function(image)
            return image
        util.vidshow(title, image_update_function=imageUpdateFunction, update_interval=frame_interval, callback=lambda: self.release())

    def save_image(self, path, gray = False):
        cv2.imwrite(path, self.get_image(gray))

if __name__ == '__main__':
    cam = Camera(device = 0)
    cam.show_video('test')
