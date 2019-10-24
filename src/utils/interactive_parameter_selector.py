from __future__ import print_function
import cv2 as cv
from hardware.camera import Camera
from recognizers.classic_d_bbr import ClassicObjectBBDetector

detector = ClassicObjectBBDetector()

max_value = 255
max_value_H = 360 // 2
max_gaussian_filter_size = 55
max_iterations = 20
window_capture_name = 'Video Capture'
window_settings_name = 'Object Detection'
gaussian_sigma_name = 'Gaussian filter sigma'
gaussian_filter_size_name = 'Gaussian filter mask size'
erode_iterations_name = 'Erode iterations'
dilate_iterations_name = 'Dilate iterations'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'


def on_low_H_thresh_trackbar(val):
    global detector
    detector.lower_bound[0] = min(detector.upper_bound[0] - 1, val)
    cv.setTrackbarPos(low_H_name, window_settings_name, detector.lower_bound[0])


def on_high_H_thresh_trackbar(val):
    global detector
    detector.upper_bound[0] = max(detector.lower_bound[0] + 1, val)
    cv.setTrackbarPos(high_H_name, window_settings_name, detector.upper_bound[0])


def on_low_S_thresh_trackbar(val):
    global detector
    detector.lower_bound[1] = min(detector.upper_bound[1] -1 , val)
    cv.setTrackbarPos(low_S_name, window_settings_name, detector.lower_bound[1])


def on_high_S_thresh_trackbar(val):
    global detector
    detector.upper_bound[1] = max(detector.lower_bound[1] + 1, val)
    cv.setTrackbarPos(high_S_name, window_settings_name, detector.upper_bound[1])


def on_low_V_thresh_trackbar(val):
    global detector
    detector.lower_bound[2] = min(detector.upper_bound[2] - 1, val)
    cv.setTrackbarPos(low_V_name, window_settings_name, detector.lower_bound[2])


def on_high_V_thresh_trackbar(val):
    global detector
    detector.upper_bound[2] = max(detector.lower_bound[2] + 1, val)
    cv.setTrackbarPos(high_V_name, window_settings_name, detector.upper_bound[2])

def on_gaussian_size_trackbar(val):
    global detector
    detector.mask_size = (val * 2) + 1
    cv.setTrackbarPos(gaussian_filter_size_name, window_settings_name, val)

def on_erode_iterations_trackbar(val):
    global detector
    detector.erode_iterations = val
    cv.setTrackbarPos(erode_iterations_name, window_settings_name, detector.erode_iterations)

def on_dilate_iterations_trackbar(val):
    global detector
    detector.dilate_iterations = val
    cv.setTrackbarPos(dilate_iterations_name, window_settings_name, detector.dilate_iterations)

camera = Camera()
cv.namedWindow(window_capture_name)
cv.namedWindow(window_settings_name)
cv.namedWindow("Mask")
cv.createTrackbar(low_H_name, window_settings_name, detector.lower_bound[0], max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_settings_name, detector.upper_bound[0], max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_settings_name, detector.lower_bound[1], max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_settings_name, detector.upper_bound[1], max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_settings_name, detector.lower_bound[2], max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_settings_name, detector.upper_bound[2], max_value, on_high_V_thresh_trackbar)
cv.createTrackbar(gaussian_filter_size_name, window_settings_name, (detector.mask_size - 1) //2, max_gaussian_filter_size, on_gaussian_size_trackbar)
cv.createTrackbar(erode_iterations_name, window_settings_name, detector.erode_iterations, max_iterations, on_erode_iterations_trackbar)
cv.createTrackbar(dilate_iterations_name, window_settings_name, detector.dilate_iterations, max_iterations, on_dilate_iterations_trackbar)

try:
    while True:
        frame = camera.get_image()
        if frame is None:
            break
        elaborated_frame = detector.get_image_mask(frame)
        boundary_box = detector.get_object_boundary_box(elaborated_frame)
        if boundary_box is not None:
            norm_area = detector.get_normalized_area(frame.shape[0], boundary_box)
            horizontal_position = detector.get_horizontal_position(frame.shape[1], boundary_box)
            if horizontal_position < 0.33:
                horizontal_position = "left"
            elif horizontal_position < 0.66:
                horizontal_position = "center"
            else:
                horizontal_position = "right"
            cv.rectangle(frame,(boundary_box[0],boundary_box[1]),(boundary_box[0]+boundary_box[2],
                                                                        boundary_box[1]+boundary_box[3]),(0,255,0),2)
            cv.putText(frame, "Normalized area (proximity): %d" % norm_area, (5, 100),
                        cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
            cv.putText(frame, "Object on the %s" % horizontal_position, (5, 150),
                        cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
        cv.imshow(window_capture_name, frame)
        cv.imshow("Mask", elaborated_frame)

        key = cv.waitKey(30)
        if key == ord('q') or key == 27:
            break
finally:
    cv.destroyAllWindows()
    camera.release()