########################################################################################################################
# Tentacle Rigger
# Author: Ruchi Hendre
# Created on 9/6/2020
# Tentacle rig using follicles with twist, retract extend and sine functionality
########################################################################################################################
import maya.cmds as cmds

windowName = 'WindowID'
# UI for the tentacle autorigger
def Tentacle_GUI():
    cmds.window(windowName, title='Tentacle AutoRigger', width=500)
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Auto Rig the Tentacle', command=createTentacleRig)
    cmds.showWindow(windowName)
    cmds.window(windowName, edit=True, width=200, height=200)


########################################################################################################################
def addConstraints(ctrl,  jntArray, joints, perc, ):
    # parent constraint controls to joints

    # cmds.parent(ctrl_grp, follicle_grp)
    cmds.pointConstraint(joints, ctrl)
    cmds.orientConstraint(joints, ctrl)
    # cmds.parentConstraint(joints, follicleTransform, mo=True)
    # weight mapping between the main controls
    cmds.pointConstraint('tentacle_main_ctrl1', joints, weight=1 - perc, mo=False)
    cmds.scaleConstraint('tentacle_main_ctrl2', joints, weight= 1, mo=False)
    cmds.pointConstraint('tentacle_main_ctrl3', joints, weight=perc, mo=False)
    cmds.orientConstraint('tentacle_main_ctrl1', joints, weight =  1- perc, mo=False)
    cmds.orientConstraint('tentacle_main_ctrl2', joints, weight=0.5, mo=False)
    cmds.orientConstraint('tentacle_main_ctrl3', joints, weight=perc, mo=False)
    cmds.pointConstraint('tentacle_main_ctrl1', 'tentacle_main_ctrl3', 'tentacle_main_ctrl2')


def createJointOnCurve(curveLocator, divFactor, index, jntArray, temp, ctrlArray):
    # loop to create a joint on the curve
    for temp in range(0, 1050, int(temp + divFactor)):
        index += 1
        cmds.currentTime(temp, e=True)

        locPos = cmds.xform(curveLocator, q=True, ws=True, t=True)
        joints = cmds.joint(n='tentacle_jnt' + str(index), a=True, p=(locPos[0], locPos[1], locPos[2]))

        #create controls
        # create controls corresponding to the joints and follicles
        # create the controls
        #ctrl = cmds.circle(c=(locPos[0], locPos[1], locPos[2]), nr=(1, 0, 0), r=5.0, ch=0, name=('tentacle_ctrl' + str(index)) )[0]
        #ctrlArray.append(ctrl)

        # create control group
        # ctrl_grp = cmds.group(name=('ctrl_group' + str(index)), em=1)
        # cmds.parent(ctrl, ctrl_grp)

        # add color to the controls
        #cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideEnabled'), 1)
        #cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideColor'), 16)
        cmds.setAttr('tentacle_jnt' + str(index) + ".displayLocalAxis", True)
        jntArray.append(joints)


########################################################################################################################
def createTentacleRig(*args):
    count = 11
    ctrlArray = []
    jntArray = []
    follicleArray = []

    steps = 1.0 / (count - 1)
    perc = 0.0

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
        locName = cmds.circle(c=(0, 0, 0), nr=(1, 0, 0), r=15.0, ch=0, name=('tentacle_main_ctrl' + str(i + 1)))[0]
        cmds.setAttr((cmds.listRelatives(locName, type='shape')[0] + '.overrideEnabled'), 1)
        cmds.setAttr((cmds.listRelatives(locName, type='shape')[0] + '.overrideColor'), 14)
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

    createJointOnCurve(curveLocator, divFactor, index, jntArray, temp, ctrlArray)

    ####################################################################################################################
    # create follicle, controls around the created joints
    index = 0
    for joints in jntArray:
        index += 1
        # create the controls
        ctrl = cmds.circle(c=(0, 0, 0), nr=(1, 0, 0), r=5.0, ch=0, name=('tentacle_ctrl' + str(index)))[0]
        ctrlArray.append(ctrl)

        # create control group
        # ctrl_grp = cmds.group(name=('ctrl_group' + str(index)), em=1)
        # cmds.parent(ctrl, ctrl_grp)

        # add color to the controls
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideEnabled'), 1)
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideColor'), 16)

        addConstraints(ctrl, jntArray, joints, perc)

        perc += steps

    ########################################################################################################################

    # add attributes to the controllers
    cmds.addAttr('tentacle_main_ctrl2', longName='Sine', niceName='--------', at="float", k=True)
    cmds.setAttr(('tentacle_main_ctrl2' + '.' + 'Sine'), lock=1)
    cmds.addAttr('tentacle_main_ctrl2', longName='amplitude', niceName='amplitude', at="float", k=True)
    cmds.addAttr('tentacle_main_ctrl2', longName='offset', niceName='offset', at="float", k=True)
    cmds.addAttr('tentacle_main_ctrl2', longName='twist', niceName='twist', at="float", k=True)
    cmds.addAttr('tentacle_main_ctrl2', longName='sineLength', niceName='sineLength', at="float", k=True)

    # sine deformer
    sineDef = cmds.nonLinear('tentacool', type='sine', lowBound=-1, highBound=1)
    sineDef[0] = cmds.rename(sineDef[0], ('nonLinear sine' + '_def'))
    sineDef[1] = cmds.rename(sineDef[1], ('nonLinear sine' + '_handle'))
    cmds.setAttr((sineDef[1] + '.rotate'), 0, 0, 90)

    cmds.setAttr((sineDef[0] + '.dropoff'), 1)
    cmds.connectAttr(('tentacle_main_ctrl2' + '.amplitude'), (sineDef[0] + '.amplitude'))
    cmds.connectAttr(('tentacle_main_ctrl2' + '.offset'), (sineDef[0] + '.offset'))
    cmds.connectAttr(('tentacle_main_ctrl2' + '.twist'), (sineDef[1] + '.rotateY'))
    cmds.connectAttr(('tentacle_main_ctrl2' + '.sineLength'), (sineDef[0] + '.wavelength'))

    # switch to dynamic (Spline IK)
    cmds.addAttr('tentacle_main_ctrl1', longName='isDynamic', niceName='isDynamic', at="bool", k=True)
    cmds.addAttr('tentacle_main_ctrl3', longName='isDynamic', niceName='isDynamic', at="bool", k=True)

    # when the isDynamic is enabled make curve dynamic
    fullTarget = ('tentacle_main_ctrl3 '+ "." + 'isDynamic')
    jobNum = cmds.scriptJob(attributeChange=[fullTarget, "makeCurveDynamic('Tentacle_curve')"])

    ctrl_grp = cmds.group(name='tentacle_rig', em=1)
    ctrl_grp = cmds.group(name='tentacle_rig', em=1)
    #cmds.parent(follicleArray, ctrl_grp)


########################################################################################################################
# bind the rig to the tentacle
def makeCurveDynamic(curveName):
    dynamicHair = cmds.createNode('hairSystem')
    nucleus = cmds.createNode('nucleus')

    cmds.connectAttr('time1.outTime', dynamicHair + '.currentTime')
    cmds.connectAttr('time1.outTime', nucleus + '.currentTime')

    cmds.connectAttr(nucleus + '.startFrame', dynamicHair + '.startFrame')
    cmds.connectAttr(nucleus + '.outputObjects[0]', dynamicHair + '.nextState')
    cmds.connectAttr(dynamicHair + '.currentState', nucleus + '.inputActive[0]')
    cmds.connectAttr(dynamicHair + '.startState', nucleus + '.inputActiveStart[0]')

    cmds.rebuildCurve('Tentacle_curve', rt=0, spans=50, ch=0, replaceOriginal=1)
    _follicle = cmds.createNode('follicle')
    _nurbsCurve = cmds.createNode('nurbsCurve')

    cmds.connectAttr(dynamicHair + '.outputHair[%s]' % (1), _follicle + '.currentPosition')
    cmds.connectAttr(_follicle + '.outHair', dynamicHair + '.inputHair[%s]' % (1))
    # connect follicle node to input curve
    cmds.connectAttr('Tentacle_curve' + '.local', _follicle + '.startPosition')
    cmds.connectAttr('Tentacle_curve' + '.worldMatrix[0]', _follicle + '.startPositionMatrix')
    # connect follicle node to output curve
    cmds.connectAttr(_follicle + '.outCurve', _nurbsCurve + '.create')

    #create IK Spline handle from the current Curve

    ikh, effector, curve = cmds.ikHandle(
        name='{0}_ikh'.format('Tentacle_curve'), solver='ikSplineSolver',
        startJoint='tentacle_jnt1', endEffector='tentacle_jnt11', parentCurve=False, autoCreateCurve = False,
        simplifyCurve=False)
    effector = cmds.rename(effector, '{0}_eff'.format('Tentacle_curve'))
    curve = cmds.rename(curve, '{0}_crv'.format('Tentacle_curve'))


    #connect output curve to joints


Tentacle_GUI()
