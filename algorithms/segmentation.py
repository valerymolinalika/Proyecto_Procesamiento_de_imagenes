import nibabel as nib
import numpy as np


class segmentation():
    def __init__(self,image_data,tau):

        self.image_data = image_data
        self.tau = tau
    
    def tresholding(image_data,tau,tol):

        print ("se pudo")
        #plt.imshow(self.image_data[:, :, 100])

        while True:
            #print(tau)

            segmentationr = image_data >= tau
            mBG = image_data[np.multiply(image_data > 10, segmentationr == 0)].mean()
            mFG = image_data[np.multiply(image_data > 10, segmentationr == 1)].mean()

            tau_post = 0.5 * (mBG + mFG)

            if np.abs(tau - tau_post) < tol:
                break
            else:
             tau = tau_post
        print(tau)
        print(segmentationr.shape)
        return segmentationr

    def growing(image, tol=50,x=100, y=100, z=20):
        # Region Growing
        segmentation = np.zeros_like(image)
        if segmentation[x,y,z] == 1:
            return
        valor_medio_cluster = image[x,y,z]
        segmentation[x,y,z] = 1
        vecinos = [(x, y, z)]
        while vecinos:
            x, y, z = vecinos.pop()
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    for dz in [-1,0,1]:
                        #vecino
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if nx >= 0 and nx < image.shape[0] and \
                            ny >= 0 and ny < image.shape[1] and \
                            nz >= 0 and nz < image.shape[2]:
                            if np.abs(valor_medio_cluster - image[nx,ny,nz]) < tol and \
                                segmentation[nx,ny,nz] == 0:
                                segmentation[nx,ny,nz] = 1
                                vecinos.append((nx, ny, nz))
        return segmentation

    def k_means(image, ks,iteracion):
        
        # Inicialización de valores k
        k_values = np.linspace(np.amin(image), np.amax(image), ks)
        for i in range(iteracion):
            d_values = [np.abs(k - image) for k in k_values]
            segmentationr = np.argmin(d_values, axis=0)

            for k_idx in range(ks):
                k_values[k_idx] = np.mean(image[segmentationr == k_idx])

        return segmentationr

    def gaussian(x, mu, sigma):
        """
        Calcula la función de densidad de probabilidad de una distribución gaussiana.
        Parametros 
            x: datos de entrada 
            mu: Media de la distribución Gaussiana.
            sigma: Desviación estándar de la distribución Gaussiana.
        """
        return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

    def gmm(image_data, k, num_iterations=100, threshold=0.01):
        """
        Segmenta una imagen en múltiples clases utilizando un Modelo de Mezcla Gaussiana.

        param image_data: Datos de la imagen de entrada.
        param k: Número de clases en las que se desea segmentar la imagen.
        param num_iterations: Número máximo de iteraciones para ejecutar el algoritmo (por defecto: 100).
        param threshold: Umbral de convergencia para el algoritmo (por defecto: 0.01).
        return: Datos de la imagen segmentada.
        """
        # Se inicializan los parametros 
        num_voxels = np.prod(image_data.shape)
        mu = np.linspace(image_data.min(), image_data.max(), k)
        sigma = np.ones(k) * (image_data.max() - image_data.min()) / (2 * k)
        p = np.ones(k) / k
        q = np.zeros((num_voxels, k))

        for i in range(num_iterations):
            # calcula las responsabilidades de cada clase
            for k in range(k):
                q[:, k] = p[k] * gaussian(image_data.flatten(), mu[k], sigma[k])
            q = q / np.sum(q, axis=1)[:, np.newaxis]

            # Actualiza los parametros
            n = np.sum(q, axis=0)
            p = n / num_voxels
            mu = np.sum(q * image_data.flatten()[:, np.newaxis], axis=0) / n
            sigma = np.sqrt(np.sum(q * (image_data.flatten()[:, np.newaxis] - mu) ** 2, axis=0) / n)

            # verifica convergencia
            if np.max(np.abs(p - q.sum(axis=0) / num_voxels)) < threshold:
                break

        # Segmentacion
        segmentation = np.argmax(q, axis=1)
        segmentation = segmentation.reshape(image_data.shape)

        return segmentation       



