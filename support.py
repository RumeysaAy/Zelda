from csv import reader
from os import walk
import pygame

import pygame

def import_csv_layout(path):
    arazi_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',') # , e gore ayirir
        for satir in layout:
            arazi_map.append(list(satir))
        return arazi_map
        
def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path): # ('resimler/grass', [], ['grass_2.png', 'grass_3.png', 'grass_1.png'])
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path)
            surface_list.append(image_surf)
    return surface_list

import_folder('resimler/grass')