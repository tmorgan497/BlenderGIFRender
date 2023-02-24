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

import bpy

bl_info = {
    'name': 'BlenderGIFRender',
    'author': 'Tanner Morgan',
    'description': 'An addon to help you render animations to GIF',
    'blender': (3, 0, 0),
    'version': (0, 0, 1),
    'location': 'View3D',
    'wiki_url': 'https://github.com/tmorgan497/BlenderGIFRender/wiki',
    'category': '3D View',
}


class BlenderGIFRender(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_blendergifrender"
    bl_label = "BlenderGIFRender"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GIF"

    def draw(self, context):
        scene = bpy.context.scene
        rd = scene.render
        self.layout.label(text=f"Render File Format: {str(rd.image_settings.file_format)}")
        self.layout.label(text=f"Render File Path: {str(rd.filepath)}")


class BlenderGIFRenderPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    check_update: bpy.props.BoolProperty(
        name="Check for Update",
        description="If enabled, addon will check for updates",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="BlenderGIFRender Preferences")
        layout.prop(self, "check_update")
        # layout.operator("wm.url_open", text="BlenderGIFRender on Github").url = "https://github.com/tmorgan497/BlenderGIFRender"


def register():
    bpy.utils.register_class(BlenderGIFRender)
    bpy.utils.register_class(BlenderGIFRenderPreferences)


def unregister():
    bpy.utils.unregister_class(BlenderGIFRender)
    bpy.utils.unregister_class(BlenderGIFRenderPreferences)


if __name__ == "__main__":
    bpy.utils.register_class(BlenderGIFRender)
    print('hi')
