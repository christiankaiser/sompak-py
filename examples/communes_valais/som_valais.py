#!/usr/bin/env python

import sompak
import numpy as np
import codecs


# Dimensions of the SOM
somshape = (30,20)

# Read the data into a Numpy array for use in the SOM
fin = codecs.open('valais-socio-econo-2000.tsv', 'r', 'utf-8')
h = fin.readline().strip().split('\t')
d = []
for l in fin:
    v = l.strip().split('\t')
    d.append(map(float, v[2:]))
fin.close()
d = np.array(d)

# Create and train the SOM
som = sompak.SOM(data=d, shape=somshape, topology='rect', neighbourhood='gaussian')
som.train(rlen=10000, alpha=0.05, radius=20)
som.train(rlen=50000, alpha=0.02, radius=3)

# Quantization error:
qerr = som.qerror()

# Extract the code vectors
cvec = som.code_vectors()

# The SOM mappings; the mappings associate each input data element (municipality in our case)
# to one of the SOM neurons
ms = som.mappings()

# Produce the SOM planes for each variable
for i in range(1,5):
    som.plane(i, 'som-plane-%i.eps' % i)

# and the U-matrix:
som.umat('som-umatrix.eps')
