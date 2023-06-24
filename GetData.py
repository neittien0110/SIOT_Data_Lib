"""_summary_
    Obtain, analysis, plot data from SIOT Center
    PREREQUISITE
        implement dependency libs
        $ pip install -r requirements
"""
import mysql.connector as myconn            # lib to connect mysql database
import matplotlib.pyplot as plt             # lib to render graphs
import numpy as np                          # lib to work with arrays
import datetime

# set environment to connect to the SIOT Center
mydb = myconn.connect(
    host="sinno.soict.ai",
    user="siot_getdata",
    password="5eb6d52843c5f3822d6fbb292fafe6ed",
    database="siot"
)

# connect db
obj = mydb.cursor()

# execute the procedure DeviceDataBySlug with the device slug of your device
obj.callproc("DeviceDataBySlug", ['siot-demo'])

# retrieve history data into an array
for result in obj.stored_results():
    devicedata = result.fetchall()

# close the connection to db
obj.close()
mydb.close()

# print to console
print("-----Raw data---------------------------")
# data struct from database
COL_ATTRIBUTENAME = 0
COL_ATTRIBUTEVALUE = 1
COL_DATETIME = 2
for det in devicedata:
    print(str(det[COL_DATETIME]) + " sensor " + det[COL_ATTRIBUTENAME] + " = " + det[COL_ATTRIBUTEVALUE])
    # print(det[COL_DATETIME].strftime('%Y-%m-%d') + " " + det[COL_ATTRIBUTENAME] + " = " + det[COL_ATTRIBUTEVALUE])

# convert raw data to numpy array to have extra features and more tools
np_devicedata =  np.array(devicedata)


print("------Just a sensor---------------------")
# extract data of a kind of sensor
AttributeName = "mysensor"
# filter by Attribute Name, and just get 2 last columns include of values and createdate 1:3
MySensors = np_devicedata[(np_devicedata == AttributeName).any(axis=1),1:3]
print(MySensors)

# extract data of a kind of sensor
AttributeName = "TurnOn"
# filter by Attribute Name, and just get 2 last columns include of values and createdate 1:3
TurnOns = np_devicedata[(np_devicedata == AttributeName).any(axis=1),1:3]
print(TurnOns)

print("------Data mining---------------------")
pre_time = 0
count_in_day = 0
MyData=[[0,datetime.datetime(2023,6,1)]];
for event in TurnOns:
    if event[1].date() == pre_time: 
        count_in_day = count_in_day + 1;
    else:
        if count_in_day != 0:
            MyData=MyData + [[count_in_day, pre_time]];
        pre_time = event[1].date()
        count_in_day  = 0;
if count_in_day != 0:
    MyData=MyData + [[count_in_day, pre_time]];

MyData = np.array(MyData)
print(MyData)  

# draw a graph
print("------plot---------------------")
# data to be plotted
#y = MySensors[:,0].astype(float)
#x = MySensors[:,1]
y = MyData[:,0].astype(int)
x = MyData[:,1]


# plotting
plt.title("Line graph")
plt.xlabel("X axis")
plt.xticks(rotation=45, ha='right')

plt.ylabel("Y axis")
plt.plot(x, y, color ="red")
plt.show()