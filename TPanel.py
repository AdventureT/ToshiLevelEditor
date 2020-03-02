import bpy

class ToshiPanel(bpy.types.Panel):
    bl_idname = "ToshiPanel"
    bl_label = "Simple Panel"
    bl_category = "Test Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('test.open_filebrowser', text="Open Trb File")