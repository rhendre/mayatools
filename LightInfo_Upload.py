# Script to load lighting information in a txt file

import maya.cmds as cmds
import pymel.core as pm
import ast
import json

name = 'WindowID30'
title = 'Light Information Upload'

def createPanel():
    cmds.window(name, title='Light Information Tool', width=500)
    cmds.columnLayout(adjustableColumn=True)

    cmds.rowColumnLayout(w=500, h=100, nc=3, cs=[(1, 30), (2, 30), (3, 30)], rs=(1, 5))
    cmds.button(label='Scene A', command= uploadLightInfo_fromTxtFile)
    cmds.button(label='Scene B', command= uploadLightInfo_fromTxtFile_SceneB)
    cmds.button(label='Scene C', command= uploadLightInfo_fromTxtFile)

    cmds.showWindow(name)
    cmds.window(name, edit=True, width=400, height=200)
    

def uploadLightInfo_fromTxtFile(*args):
    fileHandle = open('C:\\Users\\rhendre\\Downloads\\tech_artist_test\\test_02\\lightSetup.txt', 'r')
    lightInfo = json.load(fileHandle)
    print lightInfo
    
    lights = cmds.ls(type="light")
  
    cmds.setAttr('%s.intensity'% lights[0], lightInfo[0]['Intensity'])
    cmds.setAttr('%s.color'% lights[0], lightInfo[0]['Color'][0][0],lightInfo[0]['Color'][0][1], lightInfo[0]['Color'][0][2])

        
    fileHandle.close()
    return 'yes'
    
    
def uploadLightInfo_fromTxtFile_SceneB(*args):
    fileHandle = open('C:\\Users\\rhendre\\Downloads\\tech_artist_test\\test_02\\lightSetup.txt', 'r')
    lightInfo = json.load(fileHandle)
    print lightInfo
    
    lights = cmds.ls(type="light")
    cmds.setAttr('%s.intensity'% lights[0], lightInfo[1]['Intensity'])
    cmds.setAttr('%s.color'% lights[0], lightInfo[1]['Color'][0][0],lightInfo[1]['Color'][0][1], lightInfo[1]['Color'][0][2])
        
    fileHandle.close()
    return 'yes'
    


    

    
createPanel()