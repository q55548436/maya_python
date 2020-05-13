import maya.cmds as mc
import maya.mel as mel
import maya.OpenMaya as om

def firstclick(*args):
    cmds.spaceLocator(n="Z_Temp_A")
    cmds.spaceLocator(n="Z_Temp_B")
def secondclick(*args):
    """ calculator object camera distance """

    mc.select( 'Z_Temp_A', add=True )
    mc.select( 'Z_Temp_B', add=True )

    objectSelected = mc.ls(sl=1)

    P1 = mc.xform(objectSelected[0], q=1, ws=1, t=1)
    P2 = mc.xform(objectSelected[1], q=1, ws=1, t=1)
    v1, v2 = om.MVector(*P1), om.MVector(*P2)
    lengthA = om.MVector(v2-v1).length()

    P1 = mc.xform(objectSelected[0], q=1, ws=1, t=1)
    P2 = mc.xform(objectSelected[2], q=1, ws=1, t=1)
    v1, v2 = om.MVector(*P1), om.MVector(*P2)
    lengthB = om.MVector(v2-v1).length()


    """ generate custom aovs for redshift """


    def aov_generator():
        aovs = ['Depth']  # AOV's to generate

        customnames = ['Depth']

        def generate_aov(aov):
            """ generate aovs"""
            for word in aov:
                mc.rsCreateAov(type=word)

        generate_aov(aovs)

        def name_change(aovlist):
            """ give custom names to aovs in aovlist"""
            clean_names = []

            for word in aovlist:  # remove spaces between each word and
                clean = word.replace(' ', '')
                clean_names.append(clean)

            return clean_names

        def set_attributes(aovs, customnames):
            """ sets the attributes for the custom aovs"""

            for index, value in enumerate(aovs):  # CHANGE NAMES OF AOVLIST WITH CUSTOM NAMES
                mc.setAttr('rsAov_{}.name'.format(value), "{}".format(customnames[index]), type="string")
                if value == 'Depth':
                    mc.setAttr('rsAov_Depth.depthMode', 2)  # depth-mode to 'inverted'
                    mc.setAttr('rsAov_Depth.useCameraNearFar', 0)  # disable 'camera Near/Far'
                    mc.setAttr('rsAov_Depth.fileFormat', 5)
                    mc.setAttr('rsAov_Depth.tifBits', 2)
                    mc.setAttr('rsAov_Depth.minDepth', lengthA)
                    mc.setAttr('rsAov_Depth.maxDepth', lengthB)

            mel.eval("redshiftUpdateActiveAovList()")  # refresh the redshift UI
            mc.confirmDialog(title='Z', message='ZDepth are generated')

        # call function
        mel.eval("redshiftUpdateActiveAovList()")  # refresh the redshift UI
        return set_attributes(name_change(aovs), customnames)

    aov_generator()
def final(*args):
    cmds.delete( 'Z_Temp_A', 'Z_Temp_B' )
cmds.window( width=300,t="ZDepth")
cmds.columnLayout( adjustableColumn=True )
cmds.button( label='ReadMe:\n\n1.Click CreatZLocator\n\n2.MoveLocator\n\n3.SelectCamera\n\n4.Click CreatDepthAov')
cmds.button( label='CreatZLocator', command=firstclick )
cmds.button( label='CreatDepthAov', command=secondclick )
cmds.button( label='DelectLocal', command=final )
cmds.showWindow()