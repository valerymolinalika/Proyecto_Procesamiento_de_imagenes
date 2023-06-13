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

    def filter_with_borders(image):
        threshold = 100

        filtered_image = np.zeros_like(image)

        for x in range(1, image.shape[0] - 2):
            for y in range(1, image.shape[1] - 2):
                for z in range(1, image.shape[2] - 2):
                    # Compute the derivatives in x, y, and z directions
                    dx = image[x + 1, y, z] - image[x - 1, y, z]
                    dy = image[x, y + 1, z] - image[x, y - 1, z]
                    dz = image[x, y, z + 1] - image[x, y, z - 1]

                    # Compute the magnitude of the gradient
                    magnitude = np.sqrt(dx * dx + dy * dy + dz * dz)

                    # Separate pixels based on the current threshold
                    below_threshold = magnitude[magnitude < threshold]
                    above_threshold = magnitude[magnitude >= threshold]

                    # # Calculate the new threshold as the average of below_threshold and above_threshold
                    threshold = (np.mean(below_threshold) + np.mean(above_threshold)) / 2   

                    # If the magnitude is below the threshold, apply median filter
                    if magnitude < threshold:
                        neighbours = []
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                for dz in range(-1, 2):
                                    neighbours.append(image[x + dx, y + dy, z + dz])
                        median = np.median(neighbours)
                        filtered_image[x, y, z] = median
                    else:
                        filtered_image[x, y, z] = image[x, y, z]
        return filtered_image
