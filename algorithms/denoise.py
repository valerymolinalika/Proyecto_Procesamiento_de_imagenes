import nibabel as nib
import numpy as np


class denoise():
    def __init__(self,image_data):
         self.image_data = image_data
    
    def mean_filter(image_data):
        # Mean Filter
        filtered_image_data = np.zeros_like(image_data)
        for x in range(1, image_data.shape[0]-2) :
            for y in range(1, image_data.shape[1]-2) :
                for z in range(1, image_data.shape[2]-2) :
                    avg = 0
                    for dx in range(-1, 1) :
                        for dy in range(-1, 1) :
                            for dz in range(-1, 1) :
                                avg = avg + image_data[x+dx, y+dy, z+dz]

                    filtered_image_data[x+1, y+1, z+1] = avg / 27
        return filtered_image_data

    def median_filter(image_data):
        filtered_image_data = np.zeros_like(image_data)
        for x in range(1, image_data.shape[0]-2) :
            for y in range(1, image_data.shape[1]-2) :
                for z in range(1, image_data.shape[2]-2) :
                    neightbours = []
                    for dx in range(-1, 1) :
                        for dy in range(-1, 1) :
                            for dz in range(-1, 1) :
                                neightbours.append(image_data[x+dx, y+dy, z+dz])

                    median = np.median(neightbours)
                    filtered_image_data[x+1, y+1, z+1] = median
        return filtered_image_data

    def filter_with_borders(image_data):

        filtered_image_data = np.zeros_like(image_data)

        # Estimar la desviacion estandar de la intesidad
        std = np.std(image_data)

        for x in range(1, image_data.shape[0]-2):
            for y in range(1, image_data.shape[1]-2):
                for z in range(1, image_data.shape[2]-2):
                    # deriivadas en x - y - z 
                    dx = image_data[x+1, y, z] - image_data[x-1, y, z]
                    dy = image_data[x, y+1, z] - image_data[x, y-1, z]
                    dz = image_data[x, y, z+1] - image_data[x, y, z-1]

                    # magnitud del gradiente
                    magnitude = np.sqrt(dx*dx + dy*dy + dz*dz)

                    # usando la desviacion estandar se calcula el threshold
                    threshold = 3 * std

                    # si la magnitud es menor que es threshold se aplica el filtro medio
                    if magnitude < threshold:
                        neighbours = []
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                for dz in range(-1, 2):
                                    neighbours.append(image_data[x+dx, y+dy, z+dz])
                        median = np.median(neighbours)
                        filtered_image_data[x, y, z] = median
                    else:
                        filtered_image_data[x, y, z] = image_data[x, y, z]
                        
        return filtered_image_data