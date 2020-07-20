import pymel.core as pm
import maya.cmds as cmds

def ToggleRenderLayer(*arg):
    renderLayerName = pm.textScrollList('renderLayers', query = True, selectItem = True)
    print renderLayerName[0]
    val = cmds.getAttr('%s.renderable'% renderLayerName[0])
    print val
    
    if val:
        cmds.setAttr('%s.renderable'% renderLayerName[0], 0)
    else:
        cmds.setAttr('%s.renderable'% renderLayerName[0], 1)

pm.window(title = 'Selecting Rendering Tool', width = 200)
pm.columnLayout(adjustableColumn = True)

renderLayerlst = cmds.ls(type = 'renderLayer')
pm.textScrollList('renderLayers', append= renderLayerlst)

pm.button(label = 'On / Off Render Layer', command = ToggleRenderLayer )
pm.showWindow()