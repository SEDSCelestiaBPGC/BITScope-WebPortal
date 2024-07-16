import requests
import re

base_url = 'http://localhost:8090/api/objects/'

categories = ["NebulaMgr","NebulaMgr:5","StarMgr","SolarSystem"]

# Returns type,rise and set time and magnitude of obj given
def getObjDetails(objName):
    details = requests.get(f"{base_url}info?name={objName}&format=json").json()
    return {"type":details["type"],"rise":details["rise"],"set":details["set"],"mag":details["vmag"]}

#contains keys as objname and values as its details dictionary
objects_dict = {}

# Returns the time in hours rounded to two decimal places
def format_time(time_str):
    match = re.match(r'(\d+)h(\d+)m', time_str)
    if match:
        hours, minutes = map(int, match.groups())
        time = round(hours + minutes / 60, 2)
        return time + 24 if time < 12 else time # Normalize the time
    else:
        return None

# Returns the magnitude limit for the object
def mag_limit(type):
    type = type.lower()
    if 'cluster' in type:
        return 7
    elif ('nebula' in type) or ('cloud' in type) or ('remnant' in type):
        return 7
    elif 'galaxy' in type:
        return 7
    elif 'star' in type:
        return 6
    elif 'planet' in type:
        return 6
    else:
        return 7



# Telescope operation times:
start_time = 20.0
end_time = 6.0 + 24 # next day
filtered_objects_dict = {}

for type in categories:
    objects =eval( requests.get(f"{base_url}listobjectsbytype?type={type}").text)#get list of objects of "type"
    for obj in objects:
        try:
            obj_data = getObjDetails(obj)
            rise_time = format_time(obj_data['rise'])
            set_time = format_time(obj_data['set'])
            if rise_time < end_time and set_time > start_time:
                if obj_data['mag'] <= mag_limit(obj_data['type']):
                    objects_dict[obj] = obj_data

        except :# when obj not found
            pass


# for obj in objects_dict:
#     data = objects_dict[obj]
#     rise_time = format_time(data['rise'])
#     set_time = format_time(data['set'])
#     try:
#         if rise_time < end_time and set_time > start_time:
#             if data['mag'] <= mag_limit(data['type']):
#                 filtered_objects_dict[obj] = data
#     except:
#         continue

print(len(objects_dict.keys()))
