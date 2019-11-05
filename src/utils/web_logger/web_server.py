from flask import Flask
from threading import Thread

class WebLogger:


    def __init__(self, watcher, wheels_driver):
        self.watcher = watcher
        self.wheels_driver = wheels_driver
        self.app = self.__generate_app()
        self.web_sever_thread = Thread(target=lambda: self.app.run(host='0.0.0.0'))

    def __generate_app(self):
        app = Flask("NeuroBot Web Logger")

        @app.route("/")
        def root():
            return str(self.wheels_driver.speed)

        return app


    def run(self):
        self.web_sever_thread.start()
