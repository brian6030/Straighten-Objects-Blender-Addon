bl_info = {
    "name": "Straighten Objects",
    "category": "Mesh",
}

import bpy
from bpy.props import BoolProperty
import bmesh

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
        
        # Eror handling
        bm = bmesh.from_edit_mesh(obj.data)
        if not any(v.select for v in bm.verts) and not any(e.select for e in bm.edges) and not any(f.select for f in bm.faces):
            self.report({'WARNING'}, "Nothing selected in Edit Mode")
            return {'CANCELLED'}
        if any(v.select for v in bm.verts) and not any(e.select for e in bm.edges) and not any(f.select for f in bm.faces):
            self.report({'WARNING'}, "Only vertices selected")
            return {'CANCELLED'}

        # Straighten object
        bpy.ops.transform.create_orientation(name="Custom", use=False, overwrite=True)
        context.scene.transform_orientation_slots[0].type = 'Custom'
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.tool_settings.use_transform_data_origin = True
        bpy.ops.transform.transform(mode='ALIGN', orient_type='Custom')
        bpy.context.tool_settings.use_transform_data_origin = False
        
        # Optionally reset rotation
        if self.reset_rotation:
            obj.rotation_euler = (0, 0, 0)
        
        bpy.context.view_layer.update()
        return {'FINISHED'}

class CustomTransformPanel(bpy.types.Panel):
    bl_label = "Custom Transform Orientation"
    bl_idname = "VIEW3D_PT_custom_transform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'
    
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
