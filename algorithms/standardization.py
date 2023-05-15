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
    
    def histogram_matching(path_imagen,image_data, typei):
        #histogram
        image = nib.load(path_imagen)
        print (path_imagen)
        print (typei)
        if typei =="IR" or typei =="IR.nii" :
            data_target = nib.load('MRI/sample/IR.nii.gz').get_fdata()
            print ("este 1")
        elif typei =="T1" or typei =="T1.nii":
            data_target = nib.load('MRI/sample/T1.nii.gz').get_fdata()
            print ("este 2")
        elif typei =="FLAIR" or typei =="FLAIR":
            data_target = nib.load('MRI/sample/FLAIR.nii.gz').get_fdata()
            print ("este 3")

        data_orig = image_data
        
        # Redimensionar los datos en un solo arreglo 1D
        flat_orig = data_orig.flatten()
        flat_target = data_target.flatten()

        # Calcular los histogramas acumulativos
        hist_orig, bins = np.histogram(flat_orig, bins=256, range=(0, 255), density=True)
        hist_orig_cumulative = hist_orig.cumsum()
        hist_target, _ = np.histogram(flat_target, bins=256, range=(0, 255), density=True)
        hist_target_cumulative = hist_target.cumsum()

        # Mapear los valores de la imagen de origen a los valores de la imagen objetivo
        lut = np.interp(hist_orig_cumulative, hist_target_cumulative, bins[:-1])

        # Aplicar el mapeo a los datos de la imagen de origen
        data_matched = np.interp(data_orig, bins[:-1], lut)

        # Crear una nueva imagen con los datos estandarizados
        image_matched = nib.Nifti1Image(data_matched, image.affine, image.header)
        
        return data_matched