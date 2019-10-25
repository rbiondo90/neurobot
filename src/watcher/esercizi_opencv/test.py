#%%
import esercizi_opencv.distanza_oggetto as do
import cv2

#%%
image = cv2.imread('esercizi_opencv/quaderno.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#%%
filtered = cv2.GaussianBlur(image,(11,11),0)

lower_bound = (20, 125, 0)
upper_bound = (40, 255, 255)
mask_original = cv2.inRange(hsv, lower_bound, upper_bound)
mask_filtered = cv2.inRange(hsv, lower_bound, upper_bound)
mask = cv2.erode(mask_filtered, None, iterations=3)
mask = cv2.dilate(mask, None, iterations=3)
#%%
cv2.imshow('originale',image)
cv2.imshow('maschera filtrata', mask_filtered)
cv2.imshow('maschera + erode + dilate',mask)
masked_im = image & mask[:,:,None]
cv2.imshow('originale mascherata', masked_im)
while cv2.waitKey(1) &0xFF != ord('q'):
    pass
cv2.destroyAllWindows()

#%%
from esercizi_opencv.distanza_oggetto import DistanceComputer
distanceComputer = DistanceComputer()

