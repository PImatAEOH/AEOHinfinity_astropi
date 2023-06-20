"""  

Group: IPAEOH11

Program description:

  - Read and proccess each 176 received images.
  - These images must be located at ./FilesIn
  - For each received image is created one NDVI image located at ./FilesNDVI with name format : idaeoh11_pic_XXX_NDVI.jpg

  Input files:
  
    Name : ./FilesIn/idaeoh11_pic_XXX.jpg

  Output Files:

    Name : ./FilesOut/idaeoh11_pic_XXX_NDVI.jpg
       NDVI images files.      

"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from gmplot import gmplot
from decimal import Decimal

def list_filtered_directory_files(directory, extension):
    filesOut = []
    file_list = os.listdir(directory)
    
    filtered_files = [file_name for file_name in file_list if file_name.endswith(extension)]
    
    for file_name in filtered_files:
            filesOut.append(file_name)            
    return sorted(filesOut)

def calculate_ndvi(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Extract the NIR and Red channels
    nir_channel = image[:, :, 0]  # Assuming NIR is in the third channel
    red_channel = image[:, :, 2]  # Assuming Red is in the first channel
    
    # Convert the channel values to float32
    nir_channel = nir_channel.astype(np.float32)
    red_channel = red_channel.astype(np.float32)
    
    # Calculate NDVI
    ndvi = (nir_channel - red_channel) / (nir_channel + red_channel)
    
    return ndvi

def main():
    try:
        

        directoryPathInput = "./FilesIn/"
        directoryPathOutput = "./FilesNDVI/"

        listaFiles = list_filtered_directory_files(directoryPathInput, ".jpg")
        for oneFile in listaFiles:
            # Provide the path to your input image
            inputFile = oneFile
            print(inputFile)

            # Call the function to calculate the NDVI
            ndviImage = calculate_ndvi(directoryPathInput+inputFile)

            # Save the NDVI image to disk

            outputFile = inputFile[0:16] + "_NDVI" + inputFile[16:]
            plt.imsave(directoryPathOutput+outputFile, ndviImage, cmap='RdYlGn')

    except OSError as e:
        print("OSError: {0}".format(e))


if __name__=="__main__":
  main()