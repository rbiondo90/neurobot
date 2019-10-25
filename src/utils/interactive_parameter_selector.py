import cv2
from hardware.sensors.camera import Camera
from hardware.sensors.pi_camera import PiCameraWrapper
from recognizers.classic_d_bbr import ClassicObjectBBDetector
from recognizers.distance_interpolator import DistanceInterpolator
import platform
import time

class InteractiveParameterSelector:
    
    MAX_VALUE = 255
    MAX_VALUE_H = 360 // 2
    MAX_GAUSSIAN_FILTER_SIZE = 55
    MAX_ITERATIONS = 20
    WINDOW_CAPTURE_NAME = 'Video Capture'
    WINDOW_SETTINGS_NAME = 'Object Detection'
    WINDOW_MASK_NAME = 'Mask'
    GAUSSIAN_SIGMA_NAME = 'Gaussian filter sigma'
    GAUSSIAN_FILTER_SIZE_NAME = 'Gaussian filter mask size'
    ERODE_ITERATIONS_NAME = 'Erode iterations'
    DILATE_ITERATIONS_NAME = 'Dilate iterations'
    LOW_H_NAME = 'Low H'
    LOW_S_NAME = 'Low S'
    LOW_V_NAME = 'Low V'
    HIGH_H_NAME = 'High H'
    HIGH_S_NAME = 'High S'
    HIGH_V_NAME = 'High V'
    
    def __init__(self, detector_settings_file=None, distance_interpolator_settings_file=None):
        self.detector = ClassicObjectBBDetector(detector_settings_file)
        if "arm" in platform.machine():
            self.camera = PiCameraWrapper()
        else:
            self.camera = Camera()
        if distance_interpolator_settings_file is not None:
            self.distance_interpolator = DistanceInterpolator(distance_interpolator_settings_file)
        else:
            self.distance_interpolator = None

    
    def __on_low_H_thresh_trackbar(self, val):
        self.detector.lower_bound[0] = min(self.detector.upper_bound[0] - 1, val)
        cv2.setTrackbarPos(self.LOW_H_NAME, self.WINDOW_SETTINGS_NAME, self.detector.lower_bound[0])
    
    
    def __on_high_H_thresh_trackbar(self, val):
        self.detector.upper_bound[0] = max(self.detector.lower_bound[0] + 1, val)
        cv2.setTrackbarPos(self.HIGH_H_NAME, self.WINDOW_SETTINGS_NAME, self.detector.upper_bound[0])
    
    
    def __on_low_S_thresh_trackbar(self, val):
        self.detector.lower_bound[1] = min(self.detector.upper_bound[1] -1 , val)
        cv2.setTrackbarPos(self.LOW_S_NAME, self.WINDOW_SETTINGS_NAME, self.detector.lower_bound[1])
    
    
    def __on_high_S_thresh_trackbar(self, val):
        self.detector.upper_bound[1] = max(self.detector.lower_bound[1] + 1, val)
        cv2.setTrackbarPos(self.HIGH_S_NAME, self.WINDOW_SETTINGS_NAME, self.detector.upper_bound[1])
    
    
    def __on_low_V_thresh_trackbar(self, val):
        self.detector.lower_bound[2] = min(self.detector.upper_bound[2] - 1, val)
        cv2.setTrackbarPos(self.LOW_V_NAME, self.WINDOW_SETTINGS_NAME, self.detector.lower_bound[2])
    
    
    def __on_high_V_thresh_trackbar(self, val):
        self.detector.upper_bound[2] = max(self.detector.lower_bound[2] + 1, val)
        cv2.setTrackbarPos(self.HIGH_V_NAME, self.WINDOW_SETTINGS_NAME, self.detector.upper_bound[2])
    
    def __on_gaussian_size_trackbar(self, val):
        self.detector.mask_size = (val * 2) + 1
        cv2.setTrackbarPos(self.GAUSSIAN_FILTER_SIZE_NAME, self.WINDOW_SETTINGS_NAME, val)
    
    def __on_erode_iterations_trackbar(self, val):
        self.detector.erode_iterations = val
        cv2.setTrackbarPos(self.ERODE_ITERATIONS_NAME, self.WINDOW_SETTINGS_NAME, self.detector.erode_iterations)
    
    def __on_dilate_iterations_trackbar(self, val):
        self.detector.dilate_iterations = val
        cv2.setTrackbarPos(self.DILATE_ITERATIONS_NAME, self.WINDOW_SETTINGS_NAME, self.detector.dilate_iterations)

    def __initilize_windows_and_trackbars(self):
        cv2.namedWindow(self.WINDOW_CAPTURE_NAME)
        cv2.namedWindow(self.WINDOW_SETTINGS_NAME)
        cv2.namedWindow(self.WINDOW_MASK_NAME)
        cv2.createTrackbar(self.LOW_H_NAME, self.WINDOW_SETTINGS_NAME, self.detector.lower_bound[0], self.MAX_VALUE_H,
                           self.__on_low_H_thresh_trackbar)
        cv2.createTrackbar(self.HIGH_H_NAME, self.WINDOW_SETTINGS_NAME, self.detector.upper_bound[0],self. MAX_VALUE_H,
                           self.__on_high_H_thresh_trackbar)
        cv2.createTrackbar(self.LOW_S_NAME, self.WINDOW_SETTINGS_NAME, self.detector.lower_bound[1], self.MAX_VALUE,
                           self.__on_low_S_thresh_trackbar)
        cv2.createTrackbar(self.HIGH_S_NAME, self.WINDOW_SETTINGS_NAME, self.detector.upper_bound[1], self.MAX_VALUE,
                           self.__on_high_S_thresh_trackbar)
        cv2.createTrackbar(self.LOW_V_NAME, self.WINDOW_SETTINGS_NAME, self.detector.lower_bound[2], self.MAX_VALUE,
                           self.__on_low_V_thresh_trackbar)
        cv2.createTrackbar(self.HIGH_V_NAME, self.WINDOW_SETTINGS_NAME, self.detector.upper_bound[2], self.MAX_VALUE,
                           self.__on_high_V_thresh_trackbar)
        cv2.createTrackbar(self.GAUSSIAN_FILTER_SIZE_NAME, self.WINDOW_SETTINGS_NAME, (self.detector.mask_size - 1) // 2,
                           self.MAX_GAUSSIAN_FILTER_SIZE, self.__on_gaussian_size_trackbar)
        cv2.createTrackbar(self.ERODE_ITERATIONS_NAME, self.WINDOW_SETTINGS_NAME, self.detector.erode_iterations,
                           self.MAX_ITERATIONS, self.__on_erode_iterations_trackbar)
        cv2.createTrackbar(self.DILATE_ITERATIONS_NAME, self.WINDOW_SETTINGS_NAME, self.detector.dilate_iterations,
                           self.MAX_ITERATIONS, self.__on_dilate_iterations_trackbar)

    def start(self):
        self.__initilize_windows_and_trackbars()
        try:
            while True:
                start_time = time.time()
                frame = self.camera.get_image()
                if frame is None:
                    break
                elaborated_frame = self.detector.get_image_mask(frame)
                boundary_box = self.detector.get_object_boundary_box(elaborated_frame)
                if boundary_box is not None:
                    area = self.detector.get_area(boundary_box)
                    horizontal_position = self.detector.get_horizontal_position(frame.shape[1], boundary_box)
                    if horizontal_position < - 0.34:
                        horizontal_position = "left"
                    elif horizontal_position < 0.34:
                        horizontal_position = "center"
                    else:
                        horizontal_position = "right"
                    cv2.rectangle(frame, (boundary_box[0], boundary_box[1]), (boundary_box[0] + boundary_box[2],
                                                                              boundary_box[1] + boundary_box[3]), (0,255,0), 2)
                scaled_frame = cv2.resize(frame, (320, 320))
                scaled_eframe = cv2.resize(elaborated_frame, (320,320))
                if boundary_box is not None:
                    if self.distance_interpolator is not None:
                        cv2.putText(scaled_frame, "Distance: %.2f" % self.distance_interpolator.interpolate(area),
                                    (2, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, 2)

                    cv2.putText(scaled_frame, "Object area : %d" % area, (2, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, 2)
                    cv2.putText(scaled_frame, "Object on the %s" % horizontal_position, (2, 75),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, 2)
                end_time = time.time() - start_time
                cv2.putText(scaled_frame, "%d FPS" % (60. / end_time), (225, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2, 2)
                cv2.imshow(self.WINDOW_CAPTURE_NAME, scaled_frame)
                cv2.imshow("Mask", scaled_eframe)

                key = cv2.waitKey(30)
                if key == ord('q') or key == 27:
                    break
        finally:
            cv2.destroyAllWindows()
            self.camera.release()

    def store_parameters(self):
        self.detector.save_settings()