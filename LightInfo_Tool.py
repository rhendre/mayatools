# Script to load lighting information in a txt file

import maya.cmds as cmds
import pymel.core as pm
import json
import ast
import sys

name = 'WindowID12'
title = 'Light Information Download'

def createPanel():
    cmds.window(name, title=title, width=500)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout(w=500, h=100, nc=2, cs=[(1, 30), (2, 100), (3, 30)], rs=(1, 5))
    pm.text(label='Save the light info in a text file ')
    cmds.button(label='Save to text file', command= saveLightInfo_toTxtFile)
    cmds.showWindow(name)
    cmds.window(name, edit=True, width=400, height=200)


def saveLightInfo_toTxtFile(*arg):
    lights = cmds.ls(type="light")
    lightInfo = [{
                 
                "Name": cmds.file(q=True, sn=True, shn=True),
                "Intensity": cmds.getAttr('%s.intensity'% lights[0]),
                "Color": cmds.getAttr('%s.color'% lights[0])
                 
                }]
   
    with open('C:\\Users\\rhendre\\Downloads\\tech_artist_test\\test_02\\lightSetup.txt', 'a') as file:
     file.write(json.dumps(lightInfo))
     


createPanel()

