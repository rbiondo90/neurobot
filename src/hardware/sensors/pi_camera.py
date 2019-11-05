from picamera import PiCamera
from picamera.array import PiRGBArray
from utils.generic.daemon import Daemon
import cv2
import time

class PiCameraWrapper():
    thread = None
    jpg_frame = None
    image = None
    dev = None
    last_access = 0
    resolution = (256, 256)
    iso = 800
    rotation = 180
    framerate = 30

    @classmethod
    def initalize(cls):
        if PiCameraWrapper.thread is None:
            # Avvia il thread di generazione dei frame
            PiCameraWrapper.thread = Daemon(target=cls._daemon_function)
            PiCameraWrapper.thread.start()

            # Attendi fino a quando il primo frame non e' disponibile
            while cls.jpg_frame is None:
                time.sleep(0)

    # def get_image(self, gray=False):
    #     if self.dev is None:
    #         self.setup()
    #     raw_capture = PiRGBArray(self.dev)
    #     self.dev.capture(raw_capture, format="bgr", use_video_port=True)
    #     frame = raw_capture.array
    #     if gray:
    #         cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     return frame

    @classmethod
    def get_jpg_frame(cls):
        PiCameraWrapper.last_access = time.time()
        cls.initalize()
        return cls.jpg_frame

    @classmethod
    def get_image(cls):
        PiCameraWrapper.last_access = time.time()
        cls.initalize()
        return cls.image

    @classmethod
    def _daemon_function(cls):
        with PiCamera(resolution=cls.resolution, framerate=cls.framerate) as camera:
            cls.dev = camera
            camera.rotation = cls.rotation
            stream = PiRGBArray(camera, cls.resolution)
            for frame in camera.capture_continuous(stream, format='bgr', use_video_port=True):
                cls.image = frame.array
                stream.truncate(0)
                cls.jpg_frame = cv2.imencode('.jpg',cls.image,[int(cv2.IMWRITE_JPEG_QUALITY),25])[1].tostring()
                # se non ci sono state richieste da parte di alcun client negli ultimi 10 secondi ferma il thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
