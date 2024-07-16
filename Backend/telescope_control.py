# Required libraries
import sqlite3
import dotenv
import requests, synscan
# import database (uncomment if switch to mysql)
import os
import time
from datetime import datetime

dotenv.load_dotenv()
port = os.environ["PORT"]
connect = sqlite3.connect("database.db")

# Fetches the final coordinates of an object given the port number
def fetch_object(obj, port):

    jso = requests.get(f"http://localhost:{port}/api/objects/info?name={obj}&format=json").json()

    return {"az":jso["azimuth"],"alt":jso["altitude"]}


# Slews the telescope to the coordinates provided
def slew_telescope(coords):

    smc = synscan.motors()
    smc.set_pos(0,0)

    smc.goto(coords['az'], coords['alt'], synchronous=True)

    curr_pos= [smc.axis_get_pos(1), smc.axis_get_pos(2)]
    print(f"Current position of telescope: [Az: {curr_pos[0]}, Alt: {curr_pos[1]}]")

# Track Object 'obj' for 't' time 
def track(obj, t):

    coords = fetch_object('+'.join(obj.lower().split(' ')), port)
    print(f"[+] Tracking {obj} || Exposure {t}s ...")
    slew_telescope(coords)
    endtime = time.time() + t
    while time.time() < endtime:
        coords = fetch_object('+'.join(obj.lower().split(' ')), port)
        slew_telescope(coords)
        time.sleep(0.01)
    print("[+] Tracking done !")

# Takes Object name through CLI
def manual_control():

    obj = input("Enter Object Name : ").strip()
    track(obj, 30)

# Function to Capture image
def capture_image():
    pass

def sorter(elem):
    dte = elem[5].split("-")
    tm = elem[6].split(":")

    return datetime(dte[0],dte[1],dte[2],tm[0],tm[1],tm[2])

def sorted_data():
    data= connect.execute("SELECT * FROM DATA").fetchall()
    return sorted(data,key=sorter)

def web_control():
    data=connect.execute("SELECT * from data").fetchall()
    for req_ind in range(len(data)):
        track(data[req_ind][3],data[req_ind][2])
   

def main():

    control = input("Enter Control method - Manual(m) or Web(w) : ").strip().lower()
    if control=="m":
        manual_control()
    elif control=="w":
        web_control()
    else:
        print("Enter Valid input !")
        main()


main()