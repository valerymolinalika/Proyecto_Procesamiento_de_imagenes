import nibabel as nib
import numpy as np


class segmentation():
    def __init__(self,image_data,method,tau):

        self.image_data = image_data
        self.method = method
        self.tau = tau

        if method=="Thresholding":
            self.tresholding()
        elif method=="Region growing":
            self.growing()
    
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

    def growing(image,axis,valor,tol):
        print("aun no esta")
        # origin_x = 100
        # origin_y = 100
        # origin_z = 1
        # x = 1
        # y = 1
        # z = 1
        # valor_medio_cluster = image[origin_x, origin_y, 20]
        # tol = 3
        # segmentation = np.zeros_like(image)
        # itera = 1
        # point = [origin_x,origin_y]
        # tail = [point]
        # evaluated=[]
        # while True:
        #     punto = tail.pop(0)
        #     #print(len(tail))
        #     for dx in [-x, 0, x] :
        #         for dy in [-y, 0, y] :
        #             if((punto[0]+dx < 230) and ((punto[0]+dx) > 0) and (punto[1]+dy < 230) and ((punto[1]+dy) > 0) ):
        #                 if ([punto[0]+dx, punto[1]+dy] not in(evaluated)):
        #                     if np.abs(valor_medio_cluster - image[punto[0]+dx, punto[1]+dy, 20]) < tol :
        #                         segmentation[punto[0]+dx, punto[1]+dy, 20] = 1
        #                         tail.append([punto[0]+dx, punto[1]+dy])
        #                         evaluated.append([punto[0]+dx, punto[1]+dy])
        #                 else :
        #                     segmentation[punto[0]+dx, punto[1]+dy, 20] = 0
        #                     tail.append([punto[0]+dx, punto[1]+dy])
        #                     evaluated.append([punto[0]+dx, punto[1]+dy])

        #     valor_medio_cluster = image[segmentation == 1].mean()

        #     if len(tail) == 0:
        #       break


    def k_means(image, ks):
        
        iteracion=8

        # Inicialización de valores k
        k_values = np.linspace(np.amin(image), np.amax(image), ks)
        iteracion=10
        for i in range(iteracion):
            d_values = [np.abs(k - image) for k in k_values]
            segmentationr = np.argmin(d_values, axis=0)

            for k_idx in range(ks):
                k_values[k_idx] = np.mean(image[segmentationr == k_idx])

        return segmentationr

            



