'''
Created on Dec 4, 2013

@author: u0490822
'''

import numpy as np
import scipy.misc as misc
from PIL import Image, TiffTags



def LargeImageSave():
    '''Allocate an image with dimensions larger than 2^31'''

    # for i in range(14, 17):
        # dim = 1 << i
        # dim -= 8

    print(Image.PILLOW_VERSION)

    # xdim = 48000
    # ydim = 32769
    xdim = 1024
    ydim = 1024
    dtypestr = "uint8"
    dtype = np.uint8

    a = np.ones((xdim, ydim), dtype=dtype)
    for iRow in range(0, ydim):
        a[iRow, :] = iRow % 256

    outputname = '%dx%d_%s_test.tif' % (xdim, ydim, dtypestr)

    img = Image.fromarray(a, 'L')
    tiff_info = CreateTiledTiffInfo()
    img.save(outputname, tiffinfo=tiff_info)

    print("All done!")

def TagNameToTagNumber():
    NameToNumber = {}
    for k, v in TiffTags.TAGS.items():
        NameToNumber[v] = k

    return NameToNumber

def CreateTiledTiffInfo(img=None):
    '''Create the tiff_info dictionary required to prompt Pillow to write a tiled tiff file'''

    Tags = TagNameToTagNumber()

    tiff_info = {}
    tiff_info[Tags["TileWidth"]] = 256
    tiff_info[Tags["TileLength"]] = 256

    return tiff_info


if __name__ == '__main__':
    LargeImageSave()
    pass