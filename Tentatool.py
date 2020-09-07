import math

import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

windowName = 'WindowID'


def Tentacle_GUI():
    cmds.window(windowName, title='Tentacle AutoRigger', width=500)
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Auto Rig the Tentacle', command=createTentacleRig)
    cmds.showWindow(windowName)
    cmds.window(windowName, edit=True, width=200, height=200)


def distance_between_two_points(p1, p2):
    return math.sqrt(
        ((p2[0] - p1[0]) * (p2[0] - p1[0])) + ((p2[1] - p1[1]) * (p2[1] - p1[1])) + ((p2[2] - p1[2]) * (p2[2] - p1[2])))


def createTentacleRig(*args):
    count = 10
    ctrlArray = []
    jntArray = []
    grpArray = []
    # create two locators at the start and end of the tentacle
    start = cmds.spaceLocator(p=(cmds.getAttr('tentacool.translateX'), cmds.getAttr('tentacool.translateY'), 0))
    end = cmds.spaceLocator(p=(-cmds.getAttr('tentacool.translateX'), cmds.getAttr('tentacool.translateY'), 0))

    # calculate the distance between start and end.
    pos1 = cmds.xform(start, query=True, worldSpace=True, translation=True)
    pos2 = cmds.xform(end, query=True, worldSpace=True, translation=True)

    source = OpenMaya.MPoint(pos1[0], pos1[1], pos1[2])
    target = OpenMaya.MPoint(pos2[0], pos2[1], pos2[2])

    # tentacle width
    width = source - target
    steps = 1.0 / (count - 1)
    perc = 0

    # create nurbs plane
    nurbsPlane = cmds.nurbsPlane(axis=(0, 1, 0), width=10, lengthRatio=(1.0 / 10), u=count, v=1, degree=3, ch=0)[0]

    for x in range(count):
        # create hair follicles for the tentacle for better twisting motion
        follicle = cmds.createNode('follicle')
        follicleTransform = cmds.listRelatives(follicle, type='transform', p=True)
        cmds.connectAttr(follicle + '.outRotate', follicleTransform[0] + '.rotate')
        cmds.connectAttr(follicle + '.outTranslate', follicleTransform[0] + '.translate')

        cmds.connectAttr('tentacool.worldMatrix', follicle + '.inputWorldMatrix')
        cmds.connectAttr('tentacool.outMesh', follicle + '.inputMesh')

        cmds.setAttr(follicle + '.parameterU', 10 * x)
        cmds.setAttr(follicle + '.parameterV', cmds.getAttr('tentacool.translateY'))

        cmds.parentConstraint(start, end, follicleTransform, mo=True)

        # create follicle group
        follicle_grp = cmds.group(name=('follicle' + 'group' + str(x + 1)), em=1)
        cmds.parent(follicle, follicle_grp)

        # create the controls
        ctrl = cmds.circle(c=(0, 0, 0), nr=(1, 0, 0), r=5.0, ch=0, name=('tentacle_ctrl' + str(x + 1)))[0]
        ctrlArray.append(ctrl)

        #create control group
        ctrl_grp = cmds.group(name = ('ctrl_group'+ str(x+1)), em = 1)
        cmds.parent(ctrl, ctrl_grp)

        # create joints
        joints = cmds.joint(name=('tentacle' + str(x + 1) + '_jnt'), radius=0.3)  # Create a new joint.
        jntArray.append(joints)

        # parent joints to create a chain
        # if x != 0:
        # cmds.delete(cmds.parentConstraint('tentacle' + str(x + 1) + '_jnt', 'tentacle' + str(x) + '_jnt', mo = True))

        # display local axis for the joints
        cmds.setAttr('tentacle' + str(x + 1) + '_jnt' + ".displayLocalAxis", True)

        # add color to the controls
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideEnabled'), 1)
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideColor'), 14)

        # equidistantly place the joints in the tentacle
        cmds.setAttr((ctrl + '.translate'), 20 * x, cmds.getAttr('tentacool.translateY'), 0)
        cmds.setAttr((joints + '.translate'), 20 * x, cmds.getAttr('tentacool.translateY'), 0)

        # parent constraint controls to joints
        cmds.parent(ctrl_grp, follicle_grp)
        cmds.parent(joints, ctrl_grp)

        cmds.parentConstraint(start, follicle_grp, weight = 1- perc)
        cmds.parentConstraint(end, follicle_grp, weight = perc)

        perc += steps

    # create controllers at the start end and mid points
    top_Point = \
        cmds.circle(c=(cmds.getAttr('tentacool.translateX'), cmds.getAttr('tentacool.translateY'), 0), nr=(1, 0, 0),
                    r=10.0,
                    ch=0, name=('top_ctrl'))[0]
    middle_Point = cmds.circle(c=(0, 0, 0), nr=(1, 0, 0), r=10.0, ch=0, name=('mid_ctrl'))[0]
    end_Point = \
        cmds.circle(c=(-cmds.getAttr('tentacool.translateX'), cmds.getAttr('tentacool.translateY'), 0), nr=(1, 0, 0),
                    r=10.0,
                    ch=0, name=('end_ctrl'))[0]

    addColor(end_Point, middle_Point, top_Point)

    midConst = cmds.pointConstraint(top_Point, end_Point, middle_Point)

    cmds.delete(cmds.parentConstraint(start, jntArray, weight=1.0 - perc, mo=False))
    cmds.delete(cmds.parentConstraint(end, jntArray, weight=perc, mo=False))

    # creating non linear deformers

    twist = cmds.nonlinearDeformer(type='bend', curvature=0.5)


def addColor(end_Point, middle_Point, top_Point):
    cmds.setAttr((cmds.listRelatives(top_Point, type='shape')[0] + '.overrideEnabled'), 1)
    cmds.setAttr((cmds.listRelatives(top_Point, type='shape')[0] + '.overrideColor'), 14)
    cmds.setAttr((cmds.listRelatives(middle_Point, type='shape')[0] + '.overrideEnabled'), 1)
    cmds.setAttr((cmds.listRelatives(middle_Point, type='shape')[0] + '.overrideColor'), 14)
    cmds.setAttr((cmds.listRelatives(end_Point, type='shape')[0] + '.overrideEnabled'), 1)
    cmds.setAttr((cmds.listRelatives(end_Point, type='shape')[0] + '.overrideColor'), 14)


def addAttributes():
    cmds.addAttr('top_ctrl', longName='Twist', niceName='twist', at="float", k=True)
    cmds.setAttr(('top_ctrl' + '.' + 'Twist'), lock=1)
    cmds.addAttr('top_ctrl', longName='Roll', niceName='roll', at="float", k=True)
    cmds.setAttr(('top_ctrl' + '.' + 'Roll'), lock=1)
    cmds.addAttr('top_ctrl', longName='Stretch', niceName='stretch', at="float", k=True)
    cmds.setAttr(('top_ctrl' + '.' + 'Stretch'), lock=1)


Tentacle_GUI()
