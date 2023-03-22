# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:34:15 2022

@author: 113423
"""

import turtle
colors=["red","purple","blue","green","orange","yellow"]
t=turtle.Pen()
turtle.bgcolor("black")
t.speed(0)
for x in range(360):
    t.pencolor(colors[x%6])
    t.width(x//100+1)
    t.forward(x)
    t.left(59)