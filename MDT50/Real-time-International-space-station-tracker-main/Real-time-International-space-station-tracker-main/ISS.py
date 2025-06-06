import ISS_Info
import turtle
import time
import json
import urllib.request\

screen = turtle.Screen()
screen.setup(720,360)
screen.setworldcoordinates(-180,-90,180,90)
screen.bgpic("map.png")
screen.bgcolor("black")
screen.register_shape("isss.gif")
screen.title("Real time ISS tracker")

iss = turtle.Turtle()
iss.shape("isss.gif")
iss.penup()   ### Avoid a line being drawn from initilisation to first coord
iss.pen(pencolor="red", pensize=1)
style = ('Arial', 8, 'bold')

'''# Home
lat = 54.06459 
lon = -2.9062

prediction = turtle.Turtle()
prediction.penup()
prediction.color('yellow')
prediction.goto(lon,lat)
prediction.dot(5)
prediction.hideturtle()

url = 'http://api.open-notify.org/iss-now.json?lat=' +str(lat) + '&lon=' + str(lon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())

#over = result ['response'][1]['risetime']

#prediction.write(time.ctime(over), font=style)


 Houston
lat = 29.640427
lon = -95.279804

prediction.penup()
prediction.color('orange')
prediction.goto(lon,lat)
prediction.dot(5)
prediction.hideturtle()

url = 'http://api.open-notify.org/iss-now.json?lat=' +str(lat) + '&lon=' + str(lon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())

#over = result ['response'][1]['risetime']

#prediction.write(time.ctime(over), font=style)

# Monqui
lat = 45.08003
lon = -93.2967

prediction.penup()
prediction.color('pink')
prediction.goto(lon,lat)
prediction.dot(5)
prediction.hideturtle()

url = 'http://api.open-notify.org/iss-now.json?lat=' +str(lat) + '&lon=' + str(lon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())

#over = result ['response'][1]['risetime']

#prediction.write(time.ctime(over), font=style)

# Cunin
lat = 45.9144
lon = 13.2752

prediction.penup()
prediction.color('light blue')
prediction.goto(lon,lat)
prediction.dot(5)
prediction.hideturtle()

url = 'http://api.open-notify.org/iss-now.json?lat=' +str(lat) + '&lon=' + str(lon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())

#over = result ['response'][1]['risetime']

#prediction.write(time.ctime(over), font=style) '''

astronauts = turtle.Turtle()
astronauts.penup()
astronauts.color('black')
astronauts.goto(-178,86)
astronauts.hideturtle()
url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())
print("There are currently " + str(result["number"]) + " astronauts in space:")
print("")
astronauts.write("People in space: " + str(result["number"]), font=style)
astronauts.sety(astronauts.ycor() - 5)

people = result["people"]

for p in people:
    print(p["name"] + " on: " + p["craft"])
    astronauts.write(p["name"] + " on: " + p["craft"], font=style)
    astronauts.sety(astronauts.ycor() - 5)

def wipe():
    iss.clear()

screen.onkey(wipe, "space")### Allow us to clear history with spacebar 
screen.listen()            ### if screen gets too busy over time

while True:  
     
    location = ISS_Info.iss_current_loc()
    lat = location['iss_position']['latitude']
    lon = location['iss_position']['longitude']
    print("Position: \n latitude: {}, longitude: {}".format(lat,lon))
    pos = iss.pos() 
    posx = iss.xcor()
    if iss.xcor() >= (179.1):           ### Stop drawing at the right edge of  
        iss.penup()                     ### the screen to avoid a 
        iss.goto(float(lon),float(lat)) ### horizontal wrap round line
        time.sleep(5)
    else:
      iss.goto(float(lon),float(lat))
      iss.pendown()
      time.sleep(5)

 
