# -*- coding: utf-8 -*-
"""
Created on Mon May 29 03:54:30 2017

Motion Capture Addon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

@author: alex
"""

bl_info = {
    "name": "AOMotionCapture", 
    "author": "Alex Barry",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "description": "Blender Add on to assist in the use of using BVH data",
    "category": "Object",
}

import bpy

class CopyBoneRotations(bpy.types.Operator):
    bl_idname = "object.copy_bone_roll"
    bl_label = "Copy Bone Roll"
    bl_options = {'REGISTER', 'UNDO'}
    source = bpy.props.StringProperty(name="SourceObject", default="SourceObject")
    destination = bpy.props.StringProperty(name="DestinationObject", default="DestinationObject")

    # Called when operator is run
    def execute(self, context):

        # Get the logger
        print("Copying Bone Rotation from %s to %s" % (self.source, self.destination))
        
        # Setup
        rolls = {}
        # Deselect everything
        for ob in bpy.context.selected_objects:
            ob.select = False

        # Get the source and target armatures
        src = bpy.context.scene.objects[self.source]
        trg = bpy.context.scene.objects[self.destination]

        # Select the source and target armatures
        src.select = True
        trg.select = True

        print("Pulling Bone Roll from Source")

        # Pull the Roll values from the source armature        
        bpy.context.scene.objects.active = src
        bpy.ops.object.mode_set(mode='EDIT')
        for eb in src.data.edit_bones:
            rolls[eb.name] = eb.roll
            bpy.ops.object.mode_set(mode='POSE')

        print("Writing Bone Roll to Target")

        # Place the Roll values in the target armature
        bpy.context.scene.objects.active = trg
        bpy.ops.object.mode_set(mode='EDIT')
        for eb in trg.data.edit_bones:
            oldRoll = eb.roll
            eb.roll = rolls[eb.name]
            print(eb.name, oldRoll, eb.roll)
        
        #Let's blender know the operator is finished
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
def copy_bone_rot_menu_func(self, context):
    self.layout.operator(CopyBoneRotations.bl_idname) 
        
def register():
    bpy.utils.register_class(CopyBoneRotations)
    bpy.types.VIEW3D_MT_object.append(copy_bone_rot_menu_func)
    
def unregister():
    bpy.types.VIEW3D_MT_object.remove(copy_bone_rot_menu_func)
    bpy.utils.unregister_class(CopyBoneRotations)
    
if __name__ == "__main__":
    register()