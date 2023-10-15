#import cv2
import os
from PIL import Image, ImageOps

"""
RotateImage: Supporting Script
functions for rotating and flipping output plane.

rotate: rotate counterclockwise by 90 degrees.
specific_rotate: rotate counterclockwise by a specific number of degrees.
flip: flip the image horizontally.
v_flip: flip the image vertically.

Input:
savePath: directory of file
save_filename: file name of file
angle(for specific_rotate only): rotating degree

Output: None
"""

def rotate(im, angle):
    # im: Image object
    # rotate the image by `angle`` degree counterclockwise
    return im.rotate(angle, expand=False)

def h_flip(im):
    # im: Image object
    # flip the image horizontally
    return ImageOps.mirror(im)

def v_flip(im):
    # im: Image object
    # flip the image vertically
    return ImageOps.flip(im)
