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

    def growing(image,tol):
        origin_x = 100
        origin_y = 100
        x = 1
        y = 1
        valor_medio_cluster = image[origin_x, origin_y, 20]
        #tol = 50
        segmentation = np.zeros_like(image)
        point = [origin_x,origin_y]

        tail = [point]
        evaluated = image == True

        while True:
            punto = tail.pop(0)
            
            for dx in [-x, 0, x] :
                for dy in [-y, 0, y] :
                    nuevoPunto = [punto[0]+dx, punto[1]+dy]
                    if((nuevoPunto[0] < 230) and ((nuevoPunto[0]) > 0) and (nuevoPunto[1] < 230) and ((nuevoPunto[1]) > 0) ):
                        if (not evaluated[nuevoPunto[0], nuevoPunto[1],20]):
                            if np.abs(valor_medio_cluster - image[nuevoPunto[0], nuevoPunto[1], 20]) < tol :
                                segmentation[nuevoPunto[0], nuevoPunto[1], 20] = 1
                                tail.append([nuevoPunto[0], nuevoPunto[1]])
                                evaluated[nuevoPunto[0], nuevoPunto[1], 20] = True
                                evaluated[punto[0], punto[1], 20] = True
                            else :
                                segmentation[nuevoPunto[0], nuevoPunto[1], 20] = 0
                                tail.append([nuevoPunto[0], nuevoPunto[1]])
                                evaluated[nuevoPunto[0], nuevoPunto[1], 20] = True
                                evaluated[punto[0], punto[1], 20] = True
            valor_medio_cluster = image[segmentation == 1].mean()

            if len(tail) == 0:
                break
        return segmentation

    def k_means(image, ks):
        
        iteracion=10

        # Inicialización de valores k
        k_values = np.linspace(np.amin(image), np.amax(image), ks)
        iteracion=10
        for i in range(iteracion):
            d_values = [np.abs(k - image) for k in k_values]
            segmentationr = np.argmin(d_values, axis=0)

            for k_idx in range(ks):
                k_values[k_idx] = np.mean(image[segmentationr == k_idx])

        return segmentationr

            



