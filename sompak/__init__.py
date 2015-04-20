


class SOM:
    """
    A Self-Organnising Map aka Kohonen map.
    This class is a wrapper around SOM_PAK.
    """
    def __init__(self, data, shape=(12,8), topology='rect', neighbourhood='gaussian'):
        """
        Initialises a SOM using the input data set (a list of lists,
        or a Numpy array).
        shape is a tuple with the size of the map in x and y
        topology can be 'rect' or 'hexa'
        neighbourhood can be 'bubble' or 'gaussian'
        """
        import time
        t0 = time.time()
        print "   initialising SOM..."
        self.data = data
        nvars = len(data[0])
        self.shape = shape
        self.topol = topology
        self.neigh = neighbourhood
        from tempfile import mkdtemp
        import os
        self.bindir = os.path.dirname(os.path.abspath(__file__))+os.sep+'bin'+os.sep
        self.tmpdir = mkdtemp() + os.sep
        # create data file
        f = open(self.tmpdir + 'som.dat', 'w')
        f.write('%i\n' % nvars)
        for d in data:
            f.write(' '.join(map(str, d)) + '\n')
        f.close()
        # initialise code vector file
        from subprocess import call
        call([
            self.bindir + 'randinit', 
            '-din','%ssom.dat' % self.tmpdir,
            '-cout','%ssom.cod' % self.tmpdir,
            '-xdim','%i' % self.shape[0],
            '-ydim','%i' % self.shape[1],
            '-topol','%s' % self.topol,
            '-neigh','%s' % self.neigh
        ])
        print "   SOM initialisation done in %i seconds" % (int(time.time() - t0),)
    
    def __del__(self):
        from subprocess import call
        call(['rm', '-R', self.tmpdir])
    
    def train(self, rlen=1000, alpha=0.05, radius=10):
        """
        Trains the SOM using 'rlen' iterations.
        alpha is the learning rate that is linearly decreasing to 0
        radius is the update radius that is linearly decreasing to 0
        """
        import time
        t0 = time.time()
        print "   SOM training starting..."
        from subprocess import call
        call([
            self.bindir + 'vsom', 
            '-din','%ssom.dat' % self.tmpdir,
            '-cin','%ssom.cod' % self.tmpdir,
            '-cout','%ssom.cod' % self.tmpdir,
            '-rlen','%i' % rlen,
            '-alpha','%f' % alpha,
            '-radius','%i' % radius,
        ])
        print "   SOM training done in %i seconds" % int(time.time() - t0)
    
    def code_vectors(self):
        import numpy as np
        f = open(self.tmpdir + 'som.cod')
        h = f.readline()
        cod = np.array([map(float, l.strip().split()) for l in f])
        f.close()
        nvars = len(cod[0])
        c = np.zeros([self.shape[0], self.shape[1], nvars])
        cnt = 0
        for j in range(self.shape[1]):
            for i in range(self.shape[0]):
                c[i,j,:] = cod[cnt,:]
                cnt += 1
        return c
    
    def qerror(self):
        """
        Return the quantization error.
        """
        from subprocess import call
        f = open(self.tmpdir + 'stdout.tmp', 'w')
        call([
            self.bindir + 'qerror',
            '-din', '%ssom.dat' % self.tmpdir,
            '-cin',  '%ssom.cod' % self.tmpdir
        ], stdout=f)
        f.close()
        f = open(self.tmpdir + 'stdout.tmp')
        q = f.readline().strip()
        f.close()
        return float(q.split()[-5])
            
    def mappings(self, data=None):
        """
        Returns the mappings of the provided data. If data is None, the
        mappings of the training data will be used instead.
        The mappings are a list of coordinates of the BMU (best matching
        unit) and can be used to access the unit vector using the result
        from code_vectors.
        """
        if data is None: data = self.data
        nvars = len(data[0])
        # create data file
        f = open(self.tmpdir + 'mappings.dat', 'w')
        f.write('%i\n' % nvars)
        for d in data:
            f.write(' '.join(map(str, d)) + '\n')
        f.close()
        from subprocess import call
        call([
            self.bindir + 'visual',
            '-din', self.tmpdir + 'mappings.dat',
            '-cin', self.tmpdir + 'som.cod',
            '-dout', self.tmpdir + 'mappings.vis'
        ])
        f = open(self.tmpdir + 'mappings.vis')
        h = f.readline()
        m = []
        for l in f:
            v = l.strip().split()
            m.append([int(v[0]), int(v[1])])
        f.close()
        return m
    
    def plane(self, plane, outfile):
        """
        Creates an EPS file for the provided plane number.
        """
        if plane < 1:
            raise Exception("Error. plane must be at least 1.")
        if outfile[-4:] != '.eps': outfile += '.eps'
        import os
        if os.path.exists(outfile):
            raise Exception("Error. File '%s' already exists." % outfile)
        from subprocess import call
        call([
            self.bindir + 'planes',
            '-cin', self.tmpdir + 'som.cod',
            '-din', self.tmpdir + 'som.dat',
            '-plane', '%i' % plane
        ])
        call(['mv', self.tmpdir + 'som_p%i.eps' % plane, outfile])
    
    def umat(self, outfile):
        if outfile[-4:] != '.eps': outfile += '.eps'
        import os
        if os.path.exists(outfile):
            raise Exception("Error. File '%s' already exists." % outfile)
        f = open(outfile, 'w')
        from subprocess import call
        call([
            self.bindir + 'umat',
            '-cin', self.tmpdir + 'som.cod'
        ], stdout=f)
        f.close()



def testSom():
    colors = [
        [0., 0., 0.], [0., 0., 1.], [0., 0., 0.5], [0.125, 0.529, 1.0],
        [0.33, 0.4, 0.67], [0.6, 0.5, 1.0], [0., 1., 0.], [1., 0., 0.],
        [0., 1., 1.], [1., 0., 1.], [1., 1., 0.], [1., 1., 1.],
        [.33, .33, .33], [.5, .5, .5], [.66, .66, .66]
    ]
    som = sompak.SOM(data=colors, shape=(20,30), topology='rect', neighbourhood='gaussian')





