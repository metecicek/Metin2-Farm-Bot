class EdgeFilter:

    def __init__(self,
                 kernelSize=5,
                 erodeIter=1,
                 dilateIter=1,
                 canny1=100,
                 canny2=200):

        # ❗ DEFAULT VALUE FIX (None riskini kaldırır)
        self.kernelSize = kernelSize
        self.erodeIter = erodeIter
        self.dilateIter = dilateIter
        self.canny1 = canny1
        self.canny2 = canny2