# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "ToshiLevelEditor",
    "author" : "AdventureT",
    "description" : "Imports Level Data from the Toshi Engine",
    "blender" : (2, 81, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from . TPanel import ToshiPanel
from . FileBrowseOperator import ChooseTrb

def register():
    bpy.utils.register_class(ChooseTrb)
    bpy.utils.register_class(ToshiPanel)
def unregister():
    bpy.utils.unregister_class(ChooseTrb)
    bpy.utils.unregister_class(ToshiPanel)

if __name__ == "__main__":
    register()