from FeaturesIO import FeaturesIO as FtIO
import cv2.xfeatures2d as xf
import cv2

path_sellos = 'base_sellos'

surf = xf.SURF_create()
# orb = cv2.ORB_create()
FtIO.process_and_save(path_sellos, "car_sellos", surf)
