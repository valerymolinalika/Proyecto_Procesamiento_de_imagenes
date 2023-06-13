import os
import SimpleITK as sitk
from tkinter import filedialog
from tkinter import ttk,messagebox

class register():
    def rigid_register(fixed_path, moving_path, name, moving_seg_path):
        
        file_name = os.path.basename(moving_path)
        name, ext = os.path.splitext(file_name) 
    
        # Load fixed and moving images
        fixed_image = sitk.ReadImage(fixed_path)
        moving_image = sitk.ReadImage(moving_path)
        moving_seg_image=sitk.ReadImage(moving_seg_path)

        # Convert image types
        fixed_image = sitk.Cast(fixed_image, sitk.sitkFloat32)
        moving_image = sitk.Cast(moving_image, sitk.sitkFloat32)
        moving_seg_image= sitk.Cast(moving_seg_image, sitk.sitkFloat32)
        # Define the registration components
        registration_method = sitk.ImageRegistrationMethod()

        # Similarity metric - Mutual Information
        registration_method.SetMetricAsMattesMutualInformation()

        # Interpolator
        registration_method.SetInterpolator(sitk.sitkNearestNeighbor)

        # Optimizer - Gradient Descent
        registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                        estimateLearningRate=registration_method.EachIteration)

        # Initial transform - Identity
        initial_transform = sitk.Transform()
        registration_method.SetInitialTransform(initial_transform)

        # Setup for the registration process
        registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
        registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
        registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

        # Perform registration
        final_transform = registration_method.Execute(fixed_image, moving_seg_image)

        # Resample the moving image to match the fixed image dimensions and orientation
        reference_image = fixed_image
        interpolator = sitk.sitkNearestNeighbor
        default_pixel_value = 0.0
        resampled_image = sitk.Resample( moving_image,reference_image, final_transform,
                                        interpolator, default_pixel_value)

        # Convert the resampled image to Numpy array
        resampled_array = sitk.GetArrayFromImage(resampled_image)

        # Save the resampled image as NIfTI
        sitk.WriteImage(resampled_image, "MRI/patient/registered_"+name+".gz") 



