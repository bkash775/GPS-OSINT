#!/usr/bin/env python3
import subprocess
import sys

def create_banner():
    # Description
    description = "A simple OSINT tool used for image OSINT."
    
    # Author information
    author = "Author: B1K4SH"
    usage  = f"[+]Usage: python3 gpsosint.py <image file>"
    
    # ASCII art (ImageOSINT)
    ascii_art = """
     ____  _  _ ____ ____ ____ _    ____ _  _ ____ _ ____ ____ 
     |__|  |  | |___ |__| |  | |    |___ |\ | |    | |  | |__/ 
     |  |  |__| |___ |  | |__| |___ |___ | \| |___ | |__| |  \ 
                                                            
    """

    # Combine all parts into the banner
    banner = f"{description}\n{author}\n\n\t\t{usage}\n\n\t{ascii_art}"

    return banner

def get_gps_coordinate():
    try:
        if len(sys.argv) !=2:
            sys.exit("Usage:python3 gpsosint.py [file.jpg,jpeg,png]")

        result = subprocess.check_output(['exiftool','-gpslongitude','-gpslatitude',sys.argv[1]]).decode('utf-8')
        lines = result.strip().split('\n')
        longitude=None
        latitude=None
        for line in lines:
            if 'GPS Longitude'  in line:
                longitude = line.strip().split(":")[1]
            elif 'GPS Latitude' in line:
                latitude= line.strip().split(":")[1]
    
        if longitude and latitude:
            return longitude,latitude
        else:
            sys.exit("No coordinates found,please try another image files!!")

    except subprocess.CalledProcessError:
        sys.exit(1)


def coordinate_to_decimal(longitude,latitude):
    #longitude,latitude= get_gps_coordinate()
    longitude = longitude.split()
    latitude = latitude.split()
    degree=[]
    minute = []
    second = []
    direction = []
    degree_long = int(longitude[0])
    minute_long = int(longitude[2].replace("'",""))
    second_long = float(longitude[3].replace('"',""))
    direction_long = longitude[-1]
    decimal_degrees_long = degree_long + (minute_long/60) + (second_long/3600)
    if direction_long in ['S','W']:
        decimal_degrees_long = -decimal_degrees_long

    degree_lati = int(latitude[0])
    minute_lati = int(latitude[2].replace("'",""))
    second_lati = float(latitude[3].replace('"',""))
    direction_lati = latitude[-1]
    decimal_degrees_lati = degree_lati + (minute_lati/60) + (second_lati/3600)
    if direction_lati in ['S','W']:
        decimal_degrees_lati = -decimal_degrees_lati
    return decimal_degrees_lati ,decimal_degrees_long
    


if __name__ == "__main__":
    print(create_banner())
    #parse_coordinates()
    long,lati=get_gps_coordinate()
    latitude_value,longitude_value = coordinate_to_decimal(long,lati)
    print(f"GEO LOCATION: {latitude_value:.6f} , {longitude_value:.6f}")


