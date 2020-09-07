# Script to upload lighting information from a txt file
# author: Ruchi Hendre
# created: 9/6/2020

import maya.cmds as cmds
import pymel.core as pm
import ast
import json

name = 'WindowID'
title = 'Light Information Upload'


def createPanel():
    cmds.window(name, title='Change Ambient Lighting', width=500)
    cmds.columnLayout(adjustableColumn=True)

    cmds.button(label='Red', command=lambda x: uploadLightInfo_fromTxtFile(0))
    cmds.button(label='Green', command=lambda x: uploadLightInfo_fromTxtFile(1))
    cmds.button(label='Blue', command=lambda x: uploadLightInfo_fromTxtFile(2))

    cmds.showWindow(name)
    cmds.window(name, edit=True, width=400, height=100)


def uploadLightInfo_fromTxtFile(i, *args):
    # multiple json entries

    with open('lights_setup.txt', 'r') as file:
        data = file.read()
        new_data = data.replace('}{', '},{')
        json_data = json.loads('['+new_data+']')

    lights = cmds.ls(type="light")

    cmds.setAttr('%s.intensity' % lights[0], json_data[i]['Intensity'])
    cmds.setAttr('%s.color' % lights[0], json_data[i]['Color'][0][0], json_data[i]['Color'][0][1],
                 json_data[i]['Color'][0][2])

    file.close()


createPanel()
