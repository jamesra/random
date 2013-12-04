'''
Created on Dec 4, 2013

@author: u0490822
'''

import numpy as np
import scipy.misc as misc
from PIL import Image

def LargeImageSave():
    '''Allocate an image with dimensions larger than 2^31'''

    # for i in range(14, 17):
        # dim = 1 << i
        # dim -= 8

    xdim = 48000
    ydim = 32769
    dtypestr = "uint8"
    dtype = np.uint8

    print "Saving this big png works for me"
    outputname = '%dx%d_%s_test.png' % (xdim, ydim, dtypestr)

    a = np.zeros((xdim, ydim), dtype=dtype)

    # Ideally Scipy would work but it throws a different exception
    # misc.imsave(outputname, a)

    img = Image.fromarray(a, 'L')
    img.save(outputname)

    del a
    del img

    print "All done!"


    print "Saving a slightly larger png does not work for me"
    ydim = xdim
    a = np.zeros((xdim, ydim), dtype=dtype)
    # misc.imsave(outputname, a)

    outputname = '%dx%d_%s_test.png' % (xdim, ydim, dtypestr)

    img = Image.fromarray(a, 'L')
    img.save(outputname)

    print "All done!"


if __name__ == '__main__':
    LargeImageSave()
    pass