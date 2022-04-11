from tkinter import *
import math as m
#import rhinoscriptsytnax as rs
import random as r

win = Tk()
win.resizable(width=False, height=False)
win.geometry("1600x800")
win.title("ray tracing !")
canvas = Canvas(win, width=1600, height=800, background="black")
canvas.place(x=0, y=0)


#myColor = rs.CreateColor(128, 128, 128)

class ViewPoint:
   def __init__(self, x, y):
      self.x = x
      self.y = y
      self.look_angle = 0
      self.ray_number = 120
      self.field_of_view = 60
      self.updateRays()
      
   def moveforxy(self, x, y):
      self.x = x
      self.y = y
      self.updateRays()
         
   def setAngle(self, xmouse, ymouse):
      self.distance = dist(self.x, self.y, xmouse, ymouse)
      self.look_angle = m.acos((xmouse-self.x)/self.distance)
      if self.y > ymouse:
         self.look_angle = -self.look_angle
      self.updateRays()
   
   def addangle(self, value):
      self.look_angle += value
      self.updateRays()
   
   def updateRays(self):
      canvas.delete("temp")
      self.rays = []
      for i in range(self.ray_number):
         self.rays.append(Ray(self.x, self.y, self.look_angle - (self.field_of_view * m.pi / 360) + (i *(self.field_of_view / self.ray_number))* m.pi / 180 ))
         self.rays[i].collide()
      self.draw_view()
   
   def draw_view(self):
      self.w = 800/len(self.rays)
      for i in range(len(self.rays)):
         self.h = 2000 / m.sqrt(self.rays[i].distance_point)
         canvas.create_rectangle(800+self.w*i, 400+self.h, 800+self.w*(i+1), 400-self.h, fill=self.rays[i].color_viewed, outline=self.rays[i].color_viewed, tag="temp")
         
   def moveindirection(self, direction):
      if direction == "forward":
         self.y += -5
      if direction == "backward":
         self.y += 5
      if direction == "left":
         self.x += 5
      if direction == "right":
         self.x += -5
      self.updateRays()


class Ray:
   def __init__(self, x, y, angle):
      self.x = x
      self.y = y
      self.angle = angle
      self.xbis = self.x + 10000 * m.cos(self.angle)
      self.ybis = self.y + 10000 * m.sin(self.angle)
      self.distance_point = 1
   
   def collide(self):
      self.farest_point = m.inf
      for i in range(len(allWalls)):
         self.tnum = ((allWalls[i].x1 - self.x)*(self.y - self.ybis) - (allWalls[i].y1 - self.y)*(self.x - self.xbis))
         self.tden = ((allWalls[i].x1 - allWalls[i].x2)*(self.y - self.ybis) - (allWalls[i].y1 - allWalls[i].y2)*(self.x - self.xbis))
         self.unum = ((allWalls[i].x1 - allWalls[i].x2)*(allWalls[i].y1 - self.y) - (allWalls[i].y1 - allWalls[i].y2)*(allWalls[i].x1 - self.x))
         self.uden = ((allWalls[i].x1 - allWalls[i].x2)*(self.y - self.ybis) - (allWalls[i].y1 - allWalls[i].y2)*(self.x - self.xbis))
         try:
            self.t = self.tnum/self.tden
         except:
            self.t = -1
         try:
            self.u = self.unum/self.uden
         except:
            self.u = -1
         if 0 <= self.t and self.t <= 1 and 0 <= self.u and self.u <= 1:
            self.px = allWalls[i].x1 + self.t * (allWalls[i].x2 - allWalls[i].x1)
            self.py = allWalls[i].y1 + self.t * (allWalls[i].y2 - allWalls[i].y1)
            if dist(self.x, self.y, self.px, self.py) < self.farest_point:
               self.farest_point = dist(self.x, self.y, self.px, self.py)
               self.finalpx = self.px
               self.finalpy = self.py
               self.distance_point = dist(self.x, self.y, self.px, self.py)
               self.darkness_degree = 1 - (self.distance_point/1000)
               if self.darkness_degree <= 0:
                  self.darkness_degree = 0.01
               self.color_viewed = dark_color(allWalls[i].color, self.darkness_degree)
      canvas.create_line(self.x, self.y, self.finalpx, self.finalpy, fill="#ffffff", width=2, tag="temp")

         

class Wall:
   def __init__(self, x1, y1, x2, y2, color):
      self.x1 = x1
      self.y1 = y1
      self.x2 = x2
      self.y2 = y2
      self.color = color
   
   def draw(self):
      canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=4, fill=self.color)


def dark_color(color, rate):
   red = hex(m.floor(int(color[1]+color[2], 16)*rate))[2:].replace("-", "")
   green = hex(m.floor(int(color[3]+color[4], 16)*rate))[2:].replace("-", "")
   blue = hex(m.floor(int(color[5]+color[6], 16)*rate))[2:].replace("-", "")
   if len(red) == 1:
      red = "0" + str(red)
   if len(green) == 1:
      green = "0" + str(green)
   if len(blue) == 1:
      blue = "0" + str(blue)
   new_color = "#" + str(red) + str(green) + str(blue)
   return new_color
   

def dist(x1, y1, x2, y2):
   dist = m.sqrt( (y2-y1)*(y2-y1) + (x2-x1)*(x2-x1) )
   return dist

def mouseMove(event):
   if event.x < 800:
      me.moveforxy(event.x, event.y)
      
def keyPressed(event):
   try:
      me.addangle(directions[event.keycode])
   except:
      print(event.keycode)

def left_click_pressed(event):
   global newx1, newy1
   if event.x < 800:
      newx1 = event.x
      newy1 = event.y
   
def left_click_released(event):
   global allWalls
   if event.x < 800:
      #allWalls.append(Wall(newx1, newy1, event.x, event.y, ["#ff0000", "#00ff00", "#0000ff", "#00ffff"][r.randint(0, 3)]))
      allWalls.append(Wall(newx1, newy1, event.x, event.y, "#ffffff"))
      allWalls[len(allWalls)-1].draw()



allWalls = []
allWalls.append(Wall(0, 0, 0, 800, "#888888"))
allWalls.append(Wall(0, 0, 800, 0, "#888888"))
allWalls.append(Wall(800, 800, 0, 800, "#888888"))
allWalls.append(Wall(800, 0, 800, 800, "#888888"))
newx1, newy1 = 0, 0

directions = {90:"forward", 83:"backward", 81:"left", 68:"right", 39:0.05, 37:-0.05}

me = ViewPoint(400, 400)




win.bind('<Button-3>', left_click_pressed)
win.bind('<ButtonRelease-3>', left_click_released)
win.bind('<B1-Motion>', mouseMove)
win.bind('<Key>', keyPressed)
win.mainloop()