#!/usr/bin/env python3


####################################################################################
#                                                                                  #
#  single-core implementation of the Mandelbrot set                                 #
#                                                                                  #
####################################################################################


# import required libraries
import time, os
import argparse, configparser
import numpy as np
from PIL import Image
from numba import jit, prange


# mandelbrot_colors computes pixel colors in the image
#   real_min, real_max, imag_min, imag_max: bounds of the complex plane
#   iters_max: the maximum number of iterations
#   image: a reference to a memory location of the image
@jit(nopython = True, parallel = False, cache = True)
def mandelbrot_colors(real_min, real_max, imag_min, imag_max, iters_max, image):

    # image size in pixels
    width = image.shape[1]
    height = image.shape[0]

    # pixel size in complex plane
    real_step = (real_max - real_min) / width
    imag_step = (imag_max - imag_min) / height

    # check convergence of each pixel in the image
    for y in prange(0, height):
        for x in prange(0, width):   	        
            
            # a point in a complex plane corrsponding to the pixel (x, y)
            c_real = real_min + real_step * x
            c_imag = imag_min + imag_step * y

            # check for convergence
            z_real = 0
            z_imag = 0
            iters = 0
            while z_real * z_real + z_imag * z_imag <= 4 and iters < iters_max:
                # z = z * z + c
                t_real = z_real * z_real - z_imag * z_imag + c_real
                z_imag = 2.0 * z_real * z_imag + c_imag
                z_real = t_real
                iters += 1

            # color pixel in HSV scheme
            image[y, x] = (iters % 256, 255, 255 * (iters < iters_max))

# end mandelbrot_colors


# mandelbrot creates an image array of the Mandelbrot set
#   real_min, real_max, imag_min, imag_max: bounds of the complex plane
#   iters_max: the maximum number of iterations
#   width, height: size of the final image
def mandelbrot(real_min, real_max, imag_min, imag_max, iters_max, width, height):

    # allocate image array
    image = np.zeros((height, width, 3), dtype = np.uint8)

    # process image
    mandelbrot_colors(real_min, real_max, imag_min, imag_max, iters_max, image)

    # return image array
    return image

# end mandelbrot


# main routine
def main():

    # parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', type = str, default = '', help = 'config file')
    args = vars(ap.parse_args())
    config_file = args['config']

    # parse config file
    config = configparser.ConfigParser()
    if os.path.isfile(config_file):
        config.read(config_file)
    real_min = config.getfloat('AREA', 'real_min', fallback = -2.5)
    real_max = config.getfloat('AREA', 'real_max', fallback = +1.5)
    imag_min = config.getfloat('AREA', 'imag_min', fallback = -1.125)
    imag_max = config.getfloat('AREA', 'imag_max', fallback = +1.125)
    iters_max = config.getint('ITERATIONS', 'max', fallback = 256)
    width = config.getint('IMAGE', 'width', fallback = 3840)
    height = config.getint('IMAGE', 'height', fallback = 2160)
    name = config.get('IMAGE', 'name', fallback = 'mandelbrot.jpg')

    # main processing
    t = time.time()
    image = mandelbrot(real_min, real_max, imag_min, imag_max, iters_max, width, height)
    t = time.time() - t

    # save image
    Image.fromarray(image, mode='HSV').convert('RGB').save(name)    
    
    # printout
    print('SEQ: size:', (width, height), 'iterations:', iters_max, 'time:', round(t, 3), "s")    

# end main


# invoke the main routine, when this is the main script
if __name__ == "__main__":
   main()
