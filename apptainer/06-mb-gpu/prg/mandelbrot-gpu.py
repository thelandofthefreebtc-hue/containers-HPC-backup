#!/usr/bin/env python3


####################################################################################
#                                                                                  #
#  GPU implementation of the Mandelbrot set                                        #
#                                                                                  #
####################################################################################


# import required libraries
import time, os
import argparse, configparser
import numpy as np
from PIL import Image
from numba import cuda


# mandelbrot_color_kernel computes pixel colors in the image in GPU
# the describes the work which is performed by each GPU thread
#   real_min, real_max, imag_min, imag_max: bounds of the complex plane
#   iters_max: the maximum number of iterations
#   image_device: a reference to a memory location of the image in GPU
@cuda.jit
def mandelbrot_color_kernel(real_min, real_max, imag_min, imag_max, iters_max, image_device):

    # image size in pixels
    width = image_device.shape[1]
    height = image_device.shape[0]

    # pixel size in complex plane
    real_step = (real_max - real_min) / width
    imag_step = (imag_max - imag_min) / height

    # work alloted to a thread
    (x_start, y_start) = cuda.grid(2)
    x_grid = cuda.gridDim.x * cuda.blockDim.x
    y_grid = cuda.gridDim.y * cuda.blockDim.y

    # check convergence of each pixel in the image
    for y in range(x_start, height, x_grid):
        for x in range(y_start, width, y_grid):
            
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
            image_device[y, x] = (iters % 256, 255, 255 * (iters < iters_max))

# end mandelbrot_color_kernel


# mandelbrot_gpu creates an image of the Mandelbrot set
#   real_min, real_max, imag_min, imag_max: bounds of the complex plane
#   iters_max: the maximum number of iterations
#   width, height: size of the final image
def mandelbrot_gpu(real_min, real_max, imag_min, imag_max, iters_max, width, height):

    # allocate image array
    image = np.zeros((height, width, 3), dtype = np.uint8)

    # copy image array to a GPU
    image_device = cuda.to_device(image)

    # invoke the computation on a GPU
    block_size = (16, 16)
    grid_size = ((width - 1) // block_size[0] + 1, (height - 1) // block_size[1] + 1)
    mandelbrot_color_kernel[grid_size, block_size](real_min, real_max, imag_min, imag_max, iters_max, image_device)

    # copy imag array from GPU
    image = image_device.copy_to_host()

    # return image¸array
    return image

# end mandelbrot_gpu


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
    image = mandelbrot_gpu(real_min, real_max, imag_min, imag_max, iters_max, width, height)
    t = time.time() - t

    # save image
    Image.fromarray(image, mode='HSV').convert('RGB').save(name)    
    
    # printout
    print('GPU: size:', (width, height), 'iterations:', iters_max, 'time:', round(t, 3), "s")

#end main


# invoke the main routine, when this is the main script
if __name__ == "__main__":
   main()
