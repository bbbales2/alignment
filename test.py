#%%

import numpy
import skimage.io
import os

os.chdir('/home/bbales2/alignment')

ims = []
for f in sorted(os.listdir('images')):
    im = skimage.io.imread('images/{0}'.format(f), as_grey = True)[:80, :80].astype('float')
    
    im -= im.flatten().min()
    im /= im.flatten().max()

    matte = numpy.zeros((128, 128))
    
    matte[24:-24, 24:-24] = im
    
    ims.append(matte)
#%%

results = {}
toplot = numpy.zeros((9, 9))
shifts = []
for i in range(len(ims) - 1):
    xsum = 0.0
    ysum = 0.0
    
    total_mass = 0.0
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            im2 = ims[i + 1].copy()
            
            im2 = numpy.roll(im2, dx, axis = 1)
            im2 = numpy.roll(im2, dy, axis = 0)
            mass = (numpy.abs(ims[i] - im2)).sum()
            results[(dy, dx)] = mass
            
            xsum += mass * dx
            ysum += mass * dy
            
            total_mass += mass
            toplot[dy + 4, dx + 4] = (ims[i] * im2).sum()
            
    xsum /= total_mass
    ysum /= total_mass
    
    print xsum, ysum
    
    shifts.append(sorted(results.items(), key = lambda x : x[1], reverse = False)[0][0])
    #plt.imshow(toplot, interpolation = 'NONE')
    #plt.show()
    print i