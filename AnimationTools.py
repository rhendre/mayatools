import pymel.core as pm
import maya.cmds as cmds

#RUCHI_HENDRE
#Tools to make animating easy for novice animators, this tool has the basic functions like set keyframe, plablast, copy, paste keys.


def SetKeyframeFromUI(*args):
    pm.setKeyframe(i = True)
    
def copyKeyframe(*args):
    cmds.copyKey()
    
def pasteKeyframe(*args):
    cmds.pasteKey()
       
def PlayblastVideo(*args):
    pm.playblast()
    
def animationEditor(*args):  
    mel.eval('tearOffPanel "Graph Editor" graphEditor true')
         
            
def addPosetoPoseEditor(*args):
    pm.pose(ap = True)

def applyPose(*args):
    pm.pose(apply= True)
    
def setPlayblackSpeed(*args):
    pm.setplaybackSpeed()
       
   
def rotationInterpolationFunction(*args):
    pm.rotationInterpolation( '%s.selected', convert='quaternionSlerp' )
    
def displayCurrentTime(*args):
    return pm.currentTime( query=True )
    
def getStartTime(*args):
      pm.setAttr('startTime.text', 120)
		

def ToggleNurbsCurves(*args):
    myPanel = cmds.getPanel(withFocus = True)

  
    if(cmds.modelEditor(myPanel, query = True, nurbsCurves = True)):
        cmds.modelEditor(myPanel, edit = True,nurbsCurves = False)
        print "nurbsCurves hidden"
    else:
        cmds.modelEditor(myPanel, edit = True, nurbsCurves=True)
        print "nurbsCurves visible"

        
def setPlaybackoptions(startFrame, endFrame):
    #get animation start time 
    pm.playbackOptions(ast = startFrame, aet = endFrame)
              
    
def createPanel():
    pm.window(windowID, title = 'Animation Tools', width = 500)
    form = pm.formLayout(numberOfDivisions=50)
    pm.columnLayout(adjustableColumn = True, columnAttach=('both', 5), rowSpacing=10, columnWidth=250 )
    pm.autoKeyframe( state=True )
   
    
    pm.text(label= 'Channel Box')
    pm.channelBox('myChannelBox')
    
    #this section shows the current frame, start frame and the end frame.
    
    cmds.rowColumnLayout( w=500, h=100, nc=2, cs=[(1, 30), (2, 100), (3, 30)],rs=(1,5))
    pm.text(label='Current Frame')
    pm.textField( text = pm.currentTime(query =True))
    pm.text(label = 'Start Frame')
    startTime =  pm.textField(text = cmds.playbackOptions( q=True,min=True ))
    pm.textField(startTime, changeCommand = getStartTime)
    pm.text(label = 'End Frame') 
    pm.textField( text = cmds.playbackOptions( q=True,max=True ))
    
    cmds.setParent('..')
    seprator1 = cmds.separator(w=400, h=10)
      
    
    cmds.rowColumnLayout( w=500, h=100, nc=2, cs=[(1, 30), (2, 100), (3, 30), (4, 30), (5, 100), (6, 30)],rs=(1,5))
    pm.button(label = 'Set Keyframe', command = SetKeyframeFromUI)
    pm.button(label = 'Copy Keyframe', command = copyKeyframe)
    pm.button(label = 'Paste Keyframe', command = pasteKeyframe)
    pm.button(label = 'Playblast', command = PlayblastVideo)
    pm.button(label = 'Open Graph Editor', command = animationEditor)
    pm.button(label = 'Show/Hide Nurbs Curves', command = ToggleNurbsCurves)
    
    
    cmds.setParent('..')
    seprator1 = cmds.separator(w=400, h=10)
    
    
    
    pm.formLayout( form, edit=True)
    allowedAreas=['right','left']
    cmds.dockControl('Animation Tools',a='right',con=windowID,aa=allowedAreas)

def AnimationToolGui():
    if (cmds.window(windowID, ex=True)):
        cmds.deleteUI(windowID, wnd=True)
    if (cmds.dockControl('Animation Tools',ex=True)):
        cmds.deleteUI('AnimationTools')
    createPanel()
    
AnimationToolGui()
