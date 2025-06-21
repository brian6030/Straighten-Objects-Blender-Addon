bl_info = {
    "name": "Straighten Objects",
    "category": "Mesh",
    "blender": (2, 80, 0),
    "version": (1, 0),
    "description": "Align object to custom transform orientation based on selection.",
}

import bpy
import bmesh
from bpy.props import BoolProperty


class CustomTransformOperator(bpy.types.Operator):
    bl_idname = "transform.custom_orientation"
    bl_label = "Straighten Object"
    bl_options = {'REGISTER', 'UNDO'}

    reset_rotation: BoolProperty(
        name="Reset Rotation",
        description="Reset object rotation to (0, 0, 0)",
        default=False
    )

    def execute(self, context):
        obj = context.active_object

        # Error handling
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object is not a mesh.")
            return {'CANCELLED'}

        if context.mode != 'EDIT_MESH':
            self.report({'ERROR'}, "Must be in Edit Mode.")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        selected = {
            "verts": any(v.select for v in bm.verts),
            "edges": any(e.select for e in bm.edges),
            "faces": any(f.select for f in bm.faces),
        }

        # Error handling
        if not any(selected.values()):
            self.report({'WARNING'}, "Nothing selected in Edit Mode.")
            return {'CANCELLED'}
        if selected["verts"] and not selected["edges"] and not selected["faces"]:
            self.report({'WARNING'}, "Only vertices selected. Select edges or faces.")
            return {'CANCELLED'}

        # Create orientation from selection
        bpy.ops.transform.create_orientation(name="Custom", use=False, overwrite=True)
        context.scene.transform_orientation_slots.active.type = 'Custom'

        # Straighten object
        bpy.ops.object.mode_set(mode='OBJECT')
        context.tool_settings.use_transform_data_origin = True
        bpy.ops.transform.transform(mode='ALIGN', orient_type='Custom')
        context.tool_settings.use_transform_data_origin = False
        bpy.ops.object.mode_set(mode='EDIT')

        # Optionally reset rotation
        if self.reset_rotation:
            obj.rotation_euler = (0, 0, 0)

        return {'FINISHED'}


class CustomTransformPanel(bpy.types.Panel):
    bl_label = "Straighten Object"
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
