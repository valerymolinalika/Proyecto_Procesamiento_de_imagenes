import numpy as np


class borders():

    def __init__(self,image_data):
         self.image_data = image_data

    def border_magnitude(image_data):
        dfdx = np.zeros_like(image_data)
        dfdy = np.zeros_like(image_data)
        dfdz = np.zeros_like(image_data)
        for x in range(1, image_data.shape[0]-2) :
            for y in range(1, image_data.shape[1]-2) :
                for z in range(1, image_data.shape[2]-2) :
                    dfdx[x, y, z] = image_data[x+1, y, z]-image_data[x-1, y, z]
                    dfdy[x, y, z] = image_data[x, y+1, z]-image_data[x, y-1, z]
                    dfdz[x, y, z] = image_data[x, y, z+1]-image_data[x, y, z-1]
        magnitude = np.sqrt(np.power(dfdx, 2) + np.power(dfdy, 2) + np.power(dfdz, 2))
        return magnitude