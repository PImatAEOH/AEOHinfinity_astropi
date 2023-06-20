"""  

Group: IPAEOH11

Program description:

  - Read and proccess each 176 received images.
  - These images must be located at ./FilesIn
  - Is created an HTML file named map.html with a map with a pin for each inage. Pin label contain filename + GPS info.

  Input files:
  
    Name : ./FilesIn/idaeoh11_pic_XXX.jpg

  Output Files:

    Name : ./map.html
       World map with pins where each image was taken.      

"""
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from gmplot import gmplot
from decimal import Decimal

def get_gps_coordinates(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    
    if exif_data is None:
        print("No EXIF data found.")
        return None
    
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        if tag_name == 'GPSInfo':
            #a = value.keys()
            #for key in value.keys():
            #    sub_tag_name = GPSTAGS.get(key, key)
            #    print(str(sub_tag_name) + ": " + str(value[key]))

            print(image_path + " " + str(int(value[2][0])) + "°" + str(int(value[2][1])) + "'" + str(value[2][2]) + '"' + value[1] + " " + str(int(value[4][0])) + "°" + str(int(value[4][1])) + "'" + str(value[4][2]) + '"' + value[3])
            return int(value[2][0]), int(value[2][1]), value[2][2], value[1], int(value[4][0]), int(value[4][1]), value[4][2], value[3],  image_path


def list_filtered_directory_files(directory, extension):
    filesOut = []
    file_list = os.listdir(directory)
    
    filtered_files = [file_name for file_name in file_list if file_name.endswith(extension)]
    
    for file_name in filtered_files:
        file_nameOld = file_name
        if os.path.isfile(os.path.join(directory, file_name)):
            if(len(file_name) == 19):
                file_name = file_name[0:13] + "0" + file_name[13:]
            if(len(file_name) == 18):
                file_name = file_name[0:13] + "00" + file_name[13:]
            os.rename(directory+file_nameOld, directory+file_name)
            filesOut.append(file_name)            
    return sorted(filesOut)

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    if direction.upper() in ['S', 'W']:
        decimal *= -1
    return decimal

def main():
    try:
        
        # Create an instance of the Google Maps plot
        gmap = gmplot.GoogleMapPlotter(37.7749, -122.4194, 1)  # Pass the center latitude, longitude, and zoom level


        directoryPathInput = "./FilesIn/"

        listaFiles = list_filtered_directory_files(directoryPathInput, ".jpg")
        for oneFile in listaFiles:
            oneRet = get_gps_coordinates(directoryPathInput+oneFile)
            print(oneRet)

            lat = dms_to_decimal(oneRet[0], oneRet[1], oneRet[2], oneRet[3])
            log = dms_to_decimal(oneRet[4], oneRet[5], oneRet[6],oneRet[7])

            pin_latitude = [lat]
            pin_longitude = [log]


            gmap.scatter(pin_latitude , pin_longitude, '#FF0000', size=40, marker=True, title= oneRet[8] + " " + str(lat) + str(log))  # Add the pins to the map

        # Draw the map to an HTML file
        gmap.draw('./map.html')

    except OSError as e:
        print("OSError: {0}".format(e))


if __name__=="__main__":
  main()




