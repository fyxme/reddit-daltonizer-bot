#!/usr/bin/env python

from itertools import izip
from PIL import Image, ImageChops
import helper
import urllib
import daltonize
import collections

IMG_EXTENSION = "jpg"
IMG_ORIGINAL = "original.jpg"

COLOR_DEFICITS = collections.OrderedDict([
    ("d", "deuteranopia"),
    ("p", "protanopia"),
    ("t", "tritanopia")])

def deficit_to_fullname(deficit):
    return COLOR_DEFICITS[deficit]

# Helper function to not be used outside of class
def _get_conv_img_name(name, color_deficit, simulated):
    if simulated:
        return "%s_%s_sim.%s" % (name, color_deficit, IMG_EXTENSION)
    return "%s_%s_dalt.%s" % (name, color_deficit, IMG_EXTENSION)

class Img(object):
    def __init__(self, name, img_url, folder_path, auto_download=True):
        self.name = name
        self.img_url = img_url
        self.folder_path = folder_path
        self.converted = dict(
            daltonized=dict(),
            simulated=dict())

        if auto_download:
            self.download()

    def get_original_img_path(self):
        return "%s/%s" % (self.folder_path, IMG_ORIGINAL)

    def download(self):
        helper.create_folder(self.folder_path)
        urllib.urlretrieve(self.img_url, self.get_original_img_path())

    def daltonize(self, simulate_daltonism=True):
        i = Image.open(self.get_original_img_path())

        for col in COLOR_DEFICITS.keys():
            dalt = daltonize.daltonize(i,col)
            self.converted["daltonized"][col] = daltonize.array_to_img(dalt)

            if simulate_daltonism:
                sim = daltonize.simulate(i,col)
                self.converted["simulated"][col] = daltonize.array_to_img(sim)
            
    def save_converted(self):
        for cdv_type in self.converted:
            for c_def in self.converted[cdv_type]:
                is_simulated = (cdv_type == "simulated") 
                img = self.converted[cdv_type][c_def]
                img.save("%s/%s" % (self.folder_path,
                                    _get_conv_img_name(self.name, 
                                                       c_def,
                                                       is_simulated)))

    def get_converted_paths(self):
        ret = dict(
            daltonized=dict(),
            simulated=dict())

        for col in COLOR_DEFICITS.keys():
            ret["simulated"][col] = _get_conv_img_name(self.name, col, True)
            ret["daltonized"][col] = _get_conv_img_name(self.name, col, False)

        return ret