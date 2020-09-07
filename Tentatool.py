import math

import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

windowName = 'WindowID'


# UI for the tentacle autorigger
def Tentacle_GUI():
    cmds.window(windowName, title='Tentacle AutoRigger', width=500)
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Auto Rig the Tentacle', command=createTentacleRig)
    cmds.showWindow(windowName)
    cmds.window(windowName, edit=True, width=200, height=200)


def createTentacleRig(*args):
    count = 10
    ctrlArray = []
    jntArray = []
    follicleArray = []
    # create two locators at the start and end of the tentacle
    # start = cmds.spaceLocator(p=(cmds.getAttr('tentacool.translateX'), cmds.getAttr('tentacool.translateY'), 0))
    # end = cmds.spaceLocator(p=(-cmds.getAttr('tentacool.translateX'), cmds.getAttr('tentacool.translateY'), 0))
    # middle = cmds.spaceLocator(p=(0.0, cmds.getAttr('tentacool.translateY'), 0))

    # calculate the distance between start and end.
    # pos1 = cmds.xform(start, query=True, worldSpace=True, translation=True)
    # pos2 = cmds.xform(middle, query=True, worldSpace=True, translation=True)
    # pos3 = cmds.xform(end, query=True, worldSpace=True, translation=True)

    # startPoint = OpenMaya.MPoint(pos1[0], pos1[1], pos1[2])
    # midPoint = OpenMaya.MPoint(pos2[0], pos2[1], pos2[2])
    # endPoint = OpenMaya.MPoint(pos3[0], pos3[1], pos3[2])

    steps = 1.0 / (count - 1)
    perc = 0

    # create a curve between the locators
    curvePoints = cmds.curve(d=2, p=[(cmds.getAttr('tentacool.translateX'), cmds.getAttr('tentacool.translateY'), 0),
                                     (0, cmds.getAttr('tentacool.translateY'), 0),
                                     (-cmds.getAttr('tentacool.translateX'), cmds.getAttr('tentacool.translateY'), 0)])
    curveName = cmds.rename(curvePoints, 'Tentacle_curve')

    cmds.select(curveName + '.cv[*]')
    allPts = cmds.ls(sl=True, fl=True)

    # for each vertices create a cluster and a locator and then parent the cluster to the locator
    for cv in allPts:
        i = 0
        clusterName = cmds.cluster(cv, n='cluster' + str(i + 1))
        position = cmds.xform(cv, q=True, t=True, worldSpace=True)
        locName = cmds.spaceLocator(n='Tentacle_Locator')
        cmds.xform(r=True, t=position)
        cmds.parent(clusterName, locName)
        i = i + 1

    # create joints on the curve

    curveLocator = cmds.spaceLocator(n='Curve_Locator')
    cmds.select(curveLocator, curveName)
    pathLocator = cmds.pathAnimation(stu=1, etu=1000, f=True)

    # set a motion path
    cmds.selectKey(pathLocator + '_uValue', k=True, time=(1, 1000))

    # make motion path linear
    cmds.keyTangent(itt='Linear', ott='Linear')

    jointNumber = 10
    divFactor = 1000 / jointNumber
    index = 0
    cmds.select(cl=True)
    temp = cmds.currentTime(1, e=True)

    createJointOnCurve(curveLocator, divFactor, index, jntArray, temp)

    # create follicle, controls around the created joints
    index = 0
    for joints in jntArray:
        index += 1
        # create hair follicles and connect it to the joints
        follicle = cmds.createNode('follicle')
        follicleTransform = cmds.listRelatives(follicle, type='transform', p=True)
        cmds.connectAttr(follicle + '.outRotate', follicleTransform[0] + '.rotate')
        cmds.connectAttr(follicle + '.outTranslate', follicleTransform[0] + '.translate')

        cmds.connectAttr('tentacool.worldMatrix', follicle + '.inputWorldMatrix')
        cmds.connectAttr('tentacool.outMesh', follicle + '.inputMesh')

        cmds.setAttr(follicle + '.parameterU', cmds.getAttr('tentacle_jnt' + str(index) + '.translateX'))
        cmds.setAttr(follicle + '.parameterV', cmds.getAttr('tentacool.translateY'))

        cmds.parentConstraint(joints,  follicleTransform, mo=True)



        # create follicle group
        follicle_grp = cmds.group(name=('follicle' + 'group' + str(index)), em=1)
        cmds.parent(follicle, follicle_grp)
        follicleArray.append(follicle_grp)

        # create controls corresponding to the joints and follicles
        # create the controls
        ctrl = cmds.circle(c=(0, 0, 0), nr=(1, 0, 0), r=5.0, ch=0, name=('tentacle_ctrl' + str(index)))[0]
        ctrlArray.append(ctrl)

        # create control group
        ctrl_grp = cmds.group(name=('ctrl_group' + str(index)), em=1)
        cmds.parent(ctrl, ctrl_grp)

        # add color to the controls
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideEnabled'), 1)
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideColor'), 14)

        addConstraints(ctrl, ctrl_grp, follicle_grp, jntArray, joints, perc)

        perc += steps

        # add a non linear deformer for sine functionality


  ctrl_grp = cmds.group(name=('tentacle_rig'), em=1)
  cmds.parent(follicleArray, ctrl_grp)


def addConstraints(ctrl, ctrl_grp, follicle_grp, jntArray, joints, perc):
    # parent constraint controls to joints

    cmds.parent(ctrl_grp, follicle_grp)
    cmds.parent(joints, ctrl)
    cmds.parentConstraint(joints, ctrl, mo=False)
    cmds.parentConstraint('Tentacle_Locator', joints, weight=1 - perc, mo=False)
    cmds.parentConstraint('Tentacle_Locator1', joints, weight=0, mo=False)
    cmds.parentConstraint('Tentacle_Locator2', joints, weight=perc, mo=False)
    # cmds.delete(cmds.parentConstraint(start, jntArray, weight=1.0 - perc, mo=False))
    # cmds.delete(cmds.parentConstraint(end, jntArray, weight=perc, mo=False))


def createJointOnCurve(curveLocator, divFactor, index, jntArray, temp):
    # loop to create a joint on the curve
    for temp in range(0, 1050, int(temp + divFactor)):
        index += 1
        cmds.currentTime(temp, e=True)

        locPos = cmds.xform(curveLocator, q=True, ws=True, t=True)
        joints = cmds.joint(n='tentacle_jnt' + str(index), a=True, p=(locPos[0], locPos[1], locPos[2]))
        cmds.setAttr('tentacle_jnt' + str(index) + ".displayLocalAxis", True)
        jntArray.append(joints)


Tentacle_GUI()
