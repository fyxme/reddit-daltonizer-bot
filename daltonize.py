#!/usr/bin/env python

"""
   Written by Hexagonist. Copyright 2017
   Based on original code by Joerg Dietrich. Copyright 2015

   This code is licensed under the MIT license, see LICENSE for details.
"""

from collections import OrderedDict
from pkg_resources import parse_version
import urllib2
import collections

from PIL import Image
import numpy as np
assert parse_version(np.__version__) >= parse_version('1.9.0'), \
    "numpy >= 1.9.0 is required for daltonize"

class DaltonizableImage(object):
    def __init__(self,img):
        """
            Arguments:
                [string] img      - PIL Image you want to daltonize
        """
        self.img = img

    def simulate(self,color_deficit="d"):
        """ 
            Simulate daltonism 
            Arguments:
                [string] color_deficit  - color deficit(s) to simulate 
                    Allows single or multiple deficits
        """
        if not self.img:
            raise ValueError("No image specified")
        return [simulate_from_image(self.img, c) for c in color_deficit]

    def daltonize(self, color_deficit="d"):
        """ 
            Daltonize image
            Arguments:
                [string] color_deficit  - color deficit(s) to daltonize 
                    Allows single or multiple deficits
        """
        if not self.img:
            raise ValueError("No image specified")
        return [daltonize_from_image(self.img, c) for c in color_deficit]

class DaltonizableImageFromURL(DaltonizableImage):
    def __init__(self, url):
        super(DaltonizableImageFromURL, self).__init__(Image.open(urllib2.urlopen(url)))
        
class DaltonizableImageFromPath(DaltonizableImage):
    def __init__(self, path):
        super(DaltonizableImageFromPath, self).__init__(Image.open(path))



def transform_colorspace(img, mat):
    """Transform image to a different color space.

    Arguments:
    ----------
    img : array of shape (M, N, 3)
    mat : array of shape (3, 3)
        conversion matrix to different color space

    Returns:
    --------
    out : array of shape (M, N, 3)
    """
    # Fast element (=pixel) wise matrix multiplication
    return np.einsum("ij, ...j", mat, img)

def simulate_from_image(img, color_deficit="d", return_PIL_Image=True):
    """Simulate the effect of color blindness on an image.

    Arguments:
    ----------
    img : PIL.PngImagePlugin.PngImageFile, input image
    color_deficit : {"d", "p", "t"}, optional
        type of colorblindness, d for deuteronopia (default),
        p for protonapia,
        t for tritanopia

    Returns:
    --------
    sim_rgb : array of shape (M, N, 3)
        simulated image in RGB format
    """
    # Colorspace transformation matrices
    
    img = img.copy()
    # Simulate monochromacy
    if color_deficit == "m":
        if not return_PIL_Image:
            raise ValueError("Invalid return mode")
        img = img.convert("L")
        setattr(img, 'color_deficit', color_deficit)
        return img

    # Colorspace transformation matrices
    cb_matrices = {
        "d": np.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]]),
        "p": np.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]]),
        "t": np.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]]),
    }
    rgb2lms = np.array([[17.8824, 43.5161, 4.11935],
                        [3.45565, 27.1554, 3.86714],
                        [0.0299566, 0.184309, 1.46709]])
    # Precomputed inverse
    lms2rgb = np.array([[8.09444479e-02, -1.30504409e-01, 1.16721066e-01],
                        [-1.02485335e-02, 5.40193266e-02, -1.13614708e-01],
                        [-3.65296938e-04, -4.12161469e-03, 6.93511405e-01]])

    img = img.convert('RGB')

    rgb = np.asarray(img, dtype=float)
    # first go from RBG to LMS space
    lms = transform_colorspace(rgb, rgb2lms)
    # Calculate image as seen by the color blind
    sim_lms = transform_colorspace(lms, cb_matrices[color_deficit])
    # Transform back to RBG
    sim_rgb = transform_colorspace(sim_lms, lms2rgb)

    if return_PIL_Image:
        sim_rgb = array_to_img(sim_rgb)
        setattr(sim_rgb, 'color_deficit', color_deficit)

    return sim_rgb


def daltonize_from_image(rgb, color_deficit='d', return_PIL_Image=True):
    """
    Adjust color palette of an image to compensate color blindness.

    Arguments:
    ----------
    rgb : array of shape (M, N, 3)
        original image in RGB format
    color_deficit : {"d", "p", "t"}, optional
        type of colorblindness, d for deuteronopia (default),
        p for protonapia,
        t for tritanopia

    Returns:
    --------
    dtpn : array of shape (M, N, 3)
        image in RGB format with colors adjusted
    """
    sim_rgb = simulate_from_image(rgb, color_deficit, False)
    err2mod = np.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])
    # rgb - sim_rgb contains the color information that dichromats
    # cannot see. err2mod rotates this to a part of the spectrum that
    # they can see.
    rgb = rgb.convert('RGB')
    err = transform_colorspace(rgb - sim_rgb, err2mod)
    dtpn = err + rgb

    if return_PIL_Image:
        dtpn = array_to_img(dtpn)
        setattr(dtpn, 'color_deficit', color_deficit)

    return dtpn


def array_to_img(arr):
    """Convert a numpy array to a PIL image.

    Arguments:
    ----------
    arr : array of shape (M, N, 3)

    Returns:
    --------
    img : PIL.Image.Image
        RGB image created from array
    """
    # clip values to lie in the range [0, 255]
    arr = clip_array(arr)
    arr = arr.astype('uint8')
    img = Image.fromarray(arr, mode='RGB')
    return img


def clip_array(arr, min_value=0, max_value=255):
    """Ensure that all values in an array are between min and max values.

    Arguments:
    ----------
    arr : array_like
    min_value : float, optional
        default 0
    max_value : float, optional
        default 255

    Returns:
    --------
    arr : array_like
        clipped such that all values are min_value <= arr <= max_value
    """
    comp_arr = np.ones_like(arr)
    arr = np.maximum(comp_arr * min_value, arr)
    arr = np.minimum(comp_arr * max_value, arr)
    return arr
