import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class standardization():
    def __init__(self,image_data, typei):
        self.image_data = image_data
        self.typei=typei

    def rescaling(image_data, typei):

        min_value = image_data.min()
        max_value = image_data.max()
        image_data_rescaled = (image_data - min_value) / (max_value - min_value)
        return image_data_rescaled
    
    def z_score (image_data, typei):

        mean_value = image_data[image_data > 10].mean()
        standard_deviation_value =image_data[image_data > 10].std()
        image_data_rescaled = (image_data - mean_value) / (standard_deviation_value)
        return image_data_rescaled 
    
    def white_stripe(image_data, typei):
        
        # Calcular el histograma
        hist, bin_edges = np.histogram(image_data.flatten(), bins=100)

        # Encontrar los picos del histograma
        picos, _ = find_peaks(hist, height=100)
        val_picos=bin_edges[picos]
        print(val_picos[1])

        # Imagen reecalada
        image_data_rescaled=image_data/val_picos[1]
        return image_data_rescaled
    
    def histogram_matching(transform_data,k,typei):
        #histogram
        
        print (typei)
        if typei =="IR" or typei =="IR.nii" :
            reference_data = nib.load('MRI/sample/IR.nii.gz').get_fdata()
            print ("este 1")
        elif typei =="T1" or typei =="T1.nii":
            reference_data = nib.load('MRI/sample/T1.nii.gz').get_fdata()
            print ("este 2")
        elif typei =="FLAIR" or typei =="FLAIR.nii":
            reference_data = nib.load('MRI/sample/FLAIR.nii.gz').get_fdata()
            print ("este 3")

        # Reshape the data arrays to 1D arrays

        reference_flat = reference_data.flatten()
        transform_flat = transform_data.flatten()


        reference_landmarks = np.percentile(reference_flat, np.linspace(0, 100, k))
        transform_landmarks = np.percentile(transform_flat, np.linspace(0, 100, k))

        piecewise_func = np.interp(transform_flat, transform_landmarks, reference_landmarks)


        transformed_data = piecewise_func.reshape(transform_data.shape)

        return transformed_data