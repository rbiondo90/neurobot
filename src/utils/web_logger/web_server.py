from flask import Flask, Response
from utils.generic.daemon import Daemon
from hardware.sensors.pi_camera import PiCameraWrapper
import cv2
from subprocess import call
import time

class WebLogger:


    def __init__(self, watcher, wheels_driver, camera):
        self.watcher = watcher
        self.wheels_driver = wheels_driver
        self.camera = camera
        self.app = self.__generate_app()
        self.web_sever_thread = Daemon(target=lambda: self.app.run(host='0.0.0.0'))

    def __generate_app(self):
        app = Flask("NeuroBot Web Logger")

        @app.route("/")
        def root():
            return str(self.wheels_driver.speed)

        @app.route("/video")
        def video():
            return Response(gen(self.camera),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        @app.route("/s")
        def s():
            call("sudo shutdown now", shell=True)
            return str("Shutting down NeuroBot...")

        def gen(camera):
            while True:
                frame = camera.get_jpg_frame()
                time.sleep(0.1)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + 'b\r\n')
        return app


    def run(self):
        self.web_sever_thread.start()
