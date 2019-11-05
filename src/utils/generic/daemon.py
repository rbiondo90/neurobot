from threading import Thread


class Daemon(Thread):

    def __init__(self, *args, **kwargs):
        super(Daemon, self).__init__(*args, **kwargs)
        self.daemon = True
