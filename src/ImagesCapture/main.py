"""  

Group: IPAEOH11

Program description:

  - Loop during 3 hours.
  - Take a new picture when next picture overlap 20% from last one.

  Input file:
  
    Name : iss_tle.txt
       iss_tle.txt must be updated before execution! Please see https://live.ariss.org/tle/") 
                   example:
                      1 25544U 98067A   23053.36606105  .00016605  00000-0  30653-3 0  9998") 
                      2 25544  51.6385 177.2603 0005320  15.9334  97.9818 15.49214405383989")

  Output Files:

    Name : idaeoh11_pic_XXX.jpg
       Pictures files.

    Name : logfile.txt
       Application log file.       

"""
from datetime import datetime, timedelta
import time
from time import sleep
from math import sin, cos, sqrt, atan2, radians
import logzero
from logzero import logger
import os
from skyfield.api import load, wgs84, EarthSatellite
import math
from picamera import PiCamera

EARTHRADIUS = 6371

def calculateDistanceFromLastPicture(latLastPic, lonLastPic, latIssActual, lonIssActual):
  """ Calculate distance between 2 points.
      latLastPic/lonLastPic if we want (param)overlapPercentange overlap, between 2 pics, with an 
  (param)altitudeRef altitude and with a lens angle of (param)angle. 
  return: Distance in Km
  """
  # distance between latitudes
  # and longitudes
  dLat = (latIssActual - latLastPic) * math.pi / 180.0
  dLon = (lonIssActual - lonLastPic) * math.pi / 180.0

  # convert to radians
  latLastPic = (latLastPic) * math.pi / 180.0
  latIssActual = (latIssActual) * math.pi / 180.0

  # apply formula
  a = (pow(math.sin(dLat / 2), 2) +
        pow(math.sin(dLon / 2), 2) *
            math.cos(latLastPic) * math.cos(latIssActual));
  rad = EARTHRADIUS
  c = 2 * math.asin(math.sqrt(a))
  return rad * c

def takePicture(cam, num, degLat, degLon):
  """ Take 'num' picture and add GPS metadata (degLat, degLon)
    Picture file name idaeoh11_pic_XXX.jpg
  """

  #cam.start_preview()
  # Set ISO to the desired value
  cam.iso = 100
  # Wait for the automatic gain control to settle
  sleep(2)
  # Now fix the values
  cam.shutter_speed  = cam.exposure_speed
  cam.exposure_mode = 'off'
  g = cam.awb_gains
  cam.awb_mode = 'off'
  cam.awb_gains = g
  sleep(2)
  # lat log EXIF to SET
  lat = f'{degLat[0]:.0f}/1,{degLat[1]:.0f}/1,{degLat[2]*1000:.0f}/1000'
  lon = f'{degLon[0]:.0f}/1,{degLon[1]:.0f}/1,{degLon[2]*1000:.0f}/1000' 
  cam.exif_tags['GPS.GPSLatitude'] = lat
  cam.exif_tags['GPS.GPSLatitudeRef'] = degLat[3]
  cam.exif_tags['GPS.GPSLongitude'] = lon
  cam.exif_tags['GPS.GPSLongitudeRef'] = degLon[3]      
  # Finally, take several photos with the fixed settings
  photoFileName = './idaeoh11_pic_' + str(num) + '.jpg'
  cam.capture(photoFileName,bayer=False)
  logger.info("Take one photo : " + photoFileName)

def to_deg(value, loc):
    """convert decimal coordinates into degrees, munutes and seconds tuple
    Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
    return: tuple like (25, 13, 48.343 ,'N')
    """
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg =  int(abs_value)
    t1 = (abs_value-deg)*60
    min = int(t1)
    sec = round((t1 - min)* 60, 5)
    return (deg, min, sec, loc_value)

def calculateDistanceBetween2Pictures(altitudeRef, altitudeActual, angle, overlapPercentange):
  """ Calculate distance between 2 pictures, if we want (param)overlapPercentange overlap, between 2 pics, with an 
  (param)altitudeRef altitude and with a lens angle of (param)angle. 
  return: Distance in Km
  """
  tanAngulo = math.tan(math.radians(angle)) 
  resposta = ( tanAngulo * altitudeRef) + (1-overlapPercentange/100) * altitudeActual * tanAngulo
  
  return resposta

def check_disk_space():
    disk_space = os.statvfs("/")
    total_space = disk_space.f_frsize * disk_space.f_blocks
    available_space = disk_space.f_frsize * disk_space.f_bfree
    used_space = total_space - available_space
    logger.info("")
    logger.info("Total space:" + str(total_space) + " bytes")
    logger.info("Used space:" + str(used_space) + " bytes")
    logger.info("Available space:" + str(available_space) + " bytes")

def readTleFile():
  # Read ISS TLE information
  
  try:
    with open('./iss_tle.txt') as f:
      lines = f.readlines()
      return lines[0], lines[1]

  except FileNotFoundError:
    logger.error("Error: The file ./iss_tle.txt must exist and must be filled with ISS TLE information. Please see https://live.ariss.org/tle/") 
    logger.error("iss_tle.txt example: ")
    logger.error("1 25544U 98067A   23053.36606105  .00016605  00000-0  30653-3 0  9998") 
    logger.error("2 25544  51.6385 177.2603 0005320  15.9334  97.9818 15.49214405383989")
    quit()

def main():
  
  # Set Log file
  logzero.logfile("./logfile.txt")
  
  logger.info("######################################")
  logger.info("# Program start " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  #")
  logger.info("######################################")
  logger.info("")
  logger.warning("Warning : Remember that file iss_tle.txt must be updated before execution! Please see https://live.ariss.org/tle/") 
  logger.warning("iss_tle.txt example: ")
  logger.warning("1 25544U 98067A   23053.36606105  .00016605  00000-0  30653-3 0  9998") 
  logger.warning("2 25544  51.6385 177.2603 0005320  15.9334  97.9818 15.49214405383989")
  logger.info("")
  
  try:
    # Read iss_tle.txt file with ISS tle info
    line1, line2 = readTleFile()

    check_disk_space()  

    # File counter
    fileNum = 1
    # Initialize camera
    camera = PiCamera(resolution=(4056,3040), framerate=30)
        
    # Create a `datetime` variable to store the start time
    start_time = datetime.now()
    now_time = datetime.now()
    ts = load.timescale()
    
    satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)
    logger.info("")
    logger.info("Que satelite: ")
    logger.info(str(satellite))
    logger.info("Satelite informação: ")
    logger.info(str(satellite.epoch.utc_jpl()))
    logger.info("")

    # Obtain the start time `t`
    t = load.timescale().now()
    # Compute where the ISS is at time `t`
    position = satellite.at(t)

    issLat, issLon = wgs84.latlon_of(position)
    issAltitude = position.distance().km - EARTHRADIUS

    latitudeRef = issLat.degrees
    longitudeRef = issLon.degrees
    altitudeRef = issAltitude

    # Loop 3 hours
    while (now_time < start_time + timedelta(seconds=3*60*60)):

       # Obtain the current time `t`
      t = load.timescale().now()
      # Obtain where is ISS
      locAtual = satellite.at(t)
      latIssActual, lonIssActual = wgs84.latlon_of(locAtual)

      # Set new Altitude for calculation
      issAltitudeAtual = locAtual.distance().km - EARTHRADIUS

      # Calculate absolute distance that we must make next picture
      distanciaEntreFotografias = calculateDistanceBetween2Pictures(issAltitudeAtual,issAltitudeAtual, 29.72, 20)

      # Calulate distance since last picture
      distanciaDaUltima = calculateDistanceFromLastPicture(latitudeRef, longitudeRef, latIssActual.degrees, lonIssActual.degrees)
      logger.info("Distance between photos:" + str("{:.2f}".format(distanciaEntreFotografias)) + " --> Distance from last: " + str("{:.2f}".format(distanciaDaUltima)))

      # If distance from last picture is > than the calculated distance between 2 pictures, is time to take another picture
      if distanciaDaUltima > distanciaEntreFotografias:

        degLat = to_deg(latitudeRef, ['S', 'N'])
        degLon = to_deg(longitudeRef, ['W', 'E'])
        # take a new picture
        takePicture(camera, fileNum, degLat, degLon)
        latitudeRef = latIssActual.degrees
        longitudeRef = lonIssActual.degrees
        fileNum += 1

      time.sleep(1)

      #  Update the current time
      now_time = datetime.now()

  except Exception as e:
      logger.exception(e)

if __name__=="__main__":
  main()