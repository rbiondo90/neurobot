import cv2
import threading


def imshow(window_title, image, callback=None):
    #def thread_function():
    if image.shape[0] > 900:
        image = cv2.resize(image, (640,640))
    cv2.imshow(window_title, image)
    wait_for_window_closed(window_title)
    if callback is not None:
        callback()

    #thread = threading.Thread(target=thread_function)
    #thread.start()


def vidshow(title, image_update_function, update_interval, callback=None):
    #def threadFunction():
    while True:
        frame = image_update_function()
        cv2.imshow(title, frame)
        if (cv2.waitKey(update_interval) & 0xFF == ord('q')) or (cv2.getWindowProperty(title, 0) < 0):
            cv2.destroyWindow(title)
            break
    if callback is not None:
        callback()

    #thread = threading.Thread(target=threadFunction)
    #thread.start()


def wait_for_window_closed(window_title, time_interval=1):
    while (cv2.waitKey(time_interval) & 0xFF != ord('q')) and (cv2.getWindowProperty(window_title, 0) >= 0):
        pass
    cv2.destroyWindow(window_title)
