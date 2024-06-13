bl_info = {
    "name": "Straighten Objects",
    "blender": (2, 80, 0),
    "category": "3D View",
    "version": (1, 0, 0),
    "author": "Your Name",
    "description": "Create a custom transform orientation and align objects to it, with an option to reset rotation.",
}

import bpy
from bpy.props import BoolProperty

class CustomTransformOperator(bpy.types.Operator):
    bl_idname = "transform.custom_orientation"
    bl_label = "Straighten Object"
    bl_options = {'REGISTER', 'UNDO'}  # Enable the Operator Redo panel
    
    reset_rotation: BoolProperty(
        name="Reset Rotation",
        description="Reset rotation back to (0, 0, 0)",
        default=False
    )
    
    def execute(self, context):
        obj = bpy.context.active_object
        
        # Ensure we're in Edit Mode
        if bpy.context.mode != 'EDIT_MESH':
            self.report({'WARNING'}, "Must be in Edit Mode")
            return {'CANCELLED'}
        
        # Create a new transform orientation
        bpy.ops.transform.create_orientation(name="Custom", use=False, overwrite=True)
        
        # Set the new orientation as active
        context.scene.transform_orientation_slots[0].type = 'Custom'
        
        # Switch to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Enable Affect Only > Origins
        bpy.context.tool_settings.use_transform_data_origin = True
        
        # Align the selected objects to the new custom transform orientation
        bpy.ops.transform.transform(mode='ALIGN', orient_type='Custom')
        
        # Disable Affect Only > Origins
        bpy.context.tool_settings.use_transform_data_origin = False
        
        # Optionally reset rotation
        if self.reset_rotation:
            obj.rotation_euler = (0, 0, 0)
        
        # Update the scene
        bpy.context.view_layer.update()
        return {'FINISHED'}

class CustomTransformPanel(bpy.types.Panel):
    bl_label = "Custom Transform Orientation"
    bl_idname = "VIEW3D_PT_custom_transform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("transform.custom_orientation")

def register():
    bpy.utils.register_class(CustomTransformOperator)
    bpy.utils.register_class(CustomTransformPanel)

def unregister():
    bpy.utils.unregister_class(CustomTransformOperator)
    bpy.utils.unregister_class(CustomTransformPanel)

if __name__ == "__main__":
    register()
