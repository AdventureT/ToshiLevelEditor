import bpy
import os
from . readTrb import read

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty

class ChooseTrb(Operator, ImportHelper):
    bl_idname = "test.open_filebrowser"
    bl_label = "Open"
    bl_description = "Test"

    filter_glob = StringProperty( default='*.trb', options={'HIDDEN'} )

    def execute(self, context):
        print(self.filepath)
        read(self.filepath, 1)
        return {'FINISHED'}