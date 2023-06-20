#############################################################################################
# Please, before program execution the file iss_tle.txt mut be updated with today ISS TLE.  #
# Source: Today ISS TLE https://live.ariss.org/tle/                                         #
#    example(just 2 lines without any header. No spaces at line begining) :                 #
#         1 25544U 98067A   23053.36606105  .00016605  00000-0  30653-3 0  9998             #
#         2 25544  51.6385 177.2603 0005320  15.9334  97.9818 15.49214405383989             #
#                                                                                           #
#############################################################################################		  

Program description:

  - Loop during 3 hours.
  - Take a new picture, when next picture overlap 20% from last one.

  Input file:

    Name : iss_tle.txt
       iss_tle.txt (Must be updated before execution!) 

  Output files:

    Name : idaeoh11_pic_XXX.jpg
       Pictures files.

    Name : logfile.txt
       Application log file.