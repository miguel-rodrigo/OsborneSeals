import cv2
import os
import numpy as np
from FuncionSellosCompleta import detectar_sello
from Database import Database

path = 'C:/Users/usuario/Desktop/document'
walk = os.walk(path)
db = Database('docs_osborne', 'testuser', 'test123', 'results3')

seal_string = ['Corona Horizontal', 'Escudo 4 regiones', 'Jorge Muller', 'Leon Unicornio Postal',
               'OC Corona Diagonal', 'Oxforshire Infantry', 'sello1', 'sello12',
               'sello14', 'sello17', 'sello18', 'sello19', 'sello32', 'sello33',
               'sello34', 'Viceconsulado Imp de Rusia']

file = np.load('car_sellos.npz')
num_elements = len(file['arr_1'])
file.close()

for root, dirs, files in walk:
    max_ratio = 0
    curr_name = ''
    max_coords = (0, 0)
    there_is_any_image = False
    for curr_file in files:
        if curr_file.endswith('.png'):
            there_is_any_image = True
            img = cv2.imread(root + '/' + curr_file, 0)
            img2, coords, seal_number, ratio = detectar_sello(img, num_elements)
            # TODO: Take keypts import out of that function in order to perform that step only once
            if ratio > max_ratio:
                max_ratio = ratio
                curr_name = seal_string[seal_number]
                max_coords = coords

    if there_is_any_image:
        path_to_save = root.replace("\\", "/")
        db.insert_results(path_to_save, max_coords, curr_name, max_ratio)
