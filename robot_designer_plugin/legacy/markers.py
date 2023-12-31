# #####
#  This file is part of the RobotDesigner developed in the Neurorobotics
#  subproject of the Human Brain Project (https://www.humanbrainproject.eu).
#
#  The Human Brain Project is a European Commission funded project
#  in the frame of the Horizon2020 FET Flagship plan.
#  (http://ec.europa.eu/programmes/horizon2020/en/h2020-section/fet-flagships)
#
#  The Robot Designer has initially been forked from the RobotEditor
#  (https://gitlab.com/h2t/roboteditor) developed at the Karlsruhe Institute
#  of Technology in the High Performance Humanoid Technologies Laboratory (H2T).
# #####

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Blender-specific imports (catch exception for sphinx documentation)
import bpy
from bpy.props import *


# operator to create new marker
class RobotDesigner_createMarker(bpy.types.Operator):
    bl_idname = "robotdesigner.createmarker"
    bl_label = "Create Marker"

    markerName = StringProperty(name="Marker Name")
    radius = FloatProperty(name="Radius", default=0.0025, min=0.001)

    def execute(self, context):
        armName = context.active_object.name
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=self.radius)
        context.active_object.name = self.markerName
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        context.active_object.name = "MARKER_" + self.markerName
        context.active_object.RobotDesigner.tag = 'MARKER'

        for obj in bpy.data.objects:
            obj.select = False

        bpy.data.objects[self.markerName].select = True
        bpy.data.objects["MARKER_" + self.markerName].select = True
        context.scene.objects.active = bpy.data.objects["MARKER_" + self.markerName]
        bpy.ops.object.parent_set()

        bpy.ops.RobotDesigner.selectarmature(armatureName=armName)
        bpy.ops.RobotDesigner.selectmarker(markerName="MARKER_" + self.markerName)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


# operator to select marker
class RobotDesigner_selectMarker(bpy.types.Operator):
    bl_idname = "robotdesigner.selectmarker"
    bl_label = "Select Marker"

    markerName = StringProperty()

    def execute(self, context):
        context.scene.RobotDesigner.markerName = self.markerName
        marker = bpy.data.objects[self.markerName]
        arm = context.active_object

        for obj in bpy.data.objects:
            obj.select = False

        marker.select = True
        arm.select = True

        return {'FINISHED'}


# dynamic menu to select from markers
class RobotDesigner_markerMenu(bpy.types.Menu):
    bl_idname = "robotdesigner.markermenu"
    bl_label = "Select Marker"

    def draw(self, context):
        layout = self.layout
        markerNames = [obj.name for obj in bpy.data.objects if
                       obj.RobotDesigner.tag == 'MARKER' and context.scene.RobotDesigner.liveSearchMarkers in obj.name]

        for marker in sorted(markerNames, key=str.lower):
            if bpy.data.objects[marker].parent_bone:
                text = marker + " --> " + bpy.data.objects[marker].parent_bone
            else:
                text = marker
            layout.operator("RobotDesigner.selectmarker", text=text).markerName = marker


# operator to assign marker to bone
class RobotDesigner_assignMarker(bpy.types.Operator):
    bl_idname = "robotdesigner.assignmarker"
    bl_label = "Assign Marker to Bone"

    def execute(self, context):
        bpy.ops.object.parent_set(type='BONE')
        return {'FINISHED'}


# operator to unassign marker from bone
class RobotDesigner_unassignMarker(bpy.types.Operator):
    bl_idname = "robotdesigner.unassignmarker"
    bl_label = "Unassign marker"

    def execute(self, context):
        currentMarker = bpy.data.objects[context.scene.RobotDesigner.markerName]
        marker_global = currentMarker.matrix_world
        currentMarker.parent = None
        currentMarker.matrix_world = marker_global

        return {'FINISHED'}


# defines the UI part of the markers submenu
def draw(layout, context):
    layout.operator("robotdesigner.createmarker")
    layout.label("Select marker")
    topRow = layout.column(align=True)
    markerMenuText = ""
    if context.active_bone and not context.scene.RobotDesigner.markerName == "":
        marker = bpy.data.objects[context.scene.RobotDesigner.markerName]

        if marker.parent_bone:
            markerMenuText = context.scene.RobotDesigner.markerName + " --> " + marker.parent_bone
        else:
            markerMenuText = context.scene.RobotDesigner.markerName
    topRow.menu("robotdesigner.markermenu", text=markerMenuText)
    topRow.prop(context.scene.RobotDesigner, "liveSearchMarkers", icon='VIEWZOOM', text="")
    topRow.separator()
    topRow.operator("robotdesigner.unassignmarker")

    layout.label("Select Bone:")
    lowerRow = layout.column(align=True)
    lowerRow.menu("robotdesigner.bonemenu", text=context.active_bone.name)
    lowerRow.prop(context.scene.RobotDesigner, "liveSearchBones", icon='VIEWZOOM', text="")
    lowerRow.separator()
    lowerRow.operator("robotdesigner.assignmarker")


def register():
    bpy.utils.register_class(RobotDesigner_createMarker)
    bpy.utils.register_class(RobotDesigner_selectMarker)
    bpy.utils.register_class(RobotDesigner_markerMenu)
    bpy.utils.register_class(RobotDesigner_assignMarker)
    bpy.utils.register_class(RobotDesigner_unassignMarker)


def unregister():
    bpy.utils.unregister_class(RobotDesigner_createMarker)
    bpy.utils.unregister_class(RobotDesigner_selectMarker)
    bpy.utils.unregister_class(RobotDesigner_markerMenu)
    bpy.utils.unregister_class(RobotDesigner_assignMarker)
    bpy.utils.unregister_class(RobotDesigner_unassignMarker)
