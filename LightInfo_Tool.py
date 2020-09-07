# Script to load lighting information in a txt file
# author: Ruchi Hendre
# created: 9/6/2020

import maya.cmds as cmds
import pymel.core as pm
import json
import ast
import sys

name = 'WindowID'
title = 'Light Information Download'
def createPanel():
    cmds.window(name, title=title, width=500)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout(w=500, h=100, nc=2, cs=[(1, 30), (2, 100), (3, 30)], rs=(1, 5))
    pm.text(label='Save the light info in a text file ')
    cmds.button(label='Save to text file', command=saveLightInfo_toTxtFile)
    cmds.showWindow(name)
    cmds.window(name, edit=True, width=400, height=200)


def saveLightInfo_toTxtFile(*arg):
    lights = cmds.ls(type="light")
    if len(lights) != 0:
        lightInfo = {
            "Name": cmds.file(q=True, sn=True, shn=True),
            "Intensity": cmds.getAttr('%s.intensity' % lights[0]),
            "Color": cmds.getAttr('%s.color' % lights[0])
        }

        with open('lights_setup.txt', 'a') as file:
            json.dump(lightInfo, file, sort_keys=True, indent=4)

        cmds.text("Saved successfully!")


createPanel()
