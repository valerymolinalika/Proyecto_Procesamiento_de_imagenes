import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

class standarization():
    def __init__(self,image_data, method, type):
        self.image_data = image_data
        self.method = method
        self.type=type

    def rescaling(self):
        mediana = self.image_data.mean()
        desviacion=self.image_data.std()
        image_data_rescaled =(self.image_data - mediana)/desviacion 