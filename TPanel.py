import bpy

class ToshiPanel(bpy.types.Panel):
    bl_idname = "ToshiPanel"
    bl_label = "Toshi Panel"
    bl_category = "ToshiLevelEditor"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('choose.trb', text="Open terrain.trb file")