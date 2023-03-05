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
import sys
import glob
from pathlib import Path
from PIL import Image
from dataclasses import dataclass


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


@dataclass
class AddonSettings:
    GITHUB_URL = "https://github.com/tmorgan497/BlenderGIFRender"


class BlenderGIFRender(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_blendergifrender"
    bl_label = "BlenderGIFRender"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GIF"

    def render_file_format(self, context):
        scene = context.scene
        rd = scene.render
        return rd.image_settings.file_format

    bpy.types.Scene.render_file_format = render_file_format

    bpy.types.Scene.my_bool = bpy.props.BoolProperty(
        name="a bool",
        description="A bool property",
        default=True,
    )
    bpy.types.Scene.my_enum = bpy.props.EnumProperty(
        name="an enum",
        description="An enum property",
        items=[
            ("OPT_A", "First Option", "Description one"),
            ("OPT_B", "Second Option", "Description two"),
            ("OPT_C", "Third Option", "Description three"),
        ],
        default="OPT_A",
    )

    def draw(self, context):
        scene = context.scene
        rd = scene.render
        self.layout.label(text=f"Render File Format: {str(rd.image_settings.file_format)}")
        # self.layout.label(text=f"Render File Path: {str(rd.filepath)}")  # , icon='ERROR')
        self.layout.prop(scene, "render_file_format", text="text")
        # row = self.layout.row()
        # row.prop(scene, "my_enum", text="text", expand=True)
        # row.prop(scene, "my_bool", text="text", expand=True)
        self.layout.operator("wm.gif_render", text="Render", icon='RENDER_ANIMATION')


class GIFRenderOperator(bpy.types.Operator):
    bl_idname = "wm.gif_render"
    bl_label = "Render to GIF"

    def execute(self, context):
        scene = context.scene
        rd = scene.render
        # self.report({'INFO'}, "Render started")
        file_format = rd.image_settings.file_format
        render_file_path = rd.filepath

        if file_format != 'PNG':
            self.report({'ERROR'}, "Render file format must be PNG")
            show_message("Render file format must be PNG", "Error", 'ERROR')
            return {'CANCELLED'}

        print('Render start')
        bpy.ops.render.render(animation=True)

        images = []
        for file in glob.glob(render_file_path + "*.png"):
            file = Path(file)
            frame = Image.open(file)
            images.append(frame)
        images[0].save(render_file_path + "/output.gif",
                       save_all=True,
                       append_images=images[1:],
                       optimize=False,
                       duration=42,
                       loop=0,
                       )

        print("Render end")
        return {'FINISHED'}


class BlenderGIFRenderPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    check_update: bpy.props.BoolProperty(
        name="Check for Update",
        description="If enabled, addon will check for updates",
        default=True,
    )

    def draw(self, context):
        self.layout.label(text="BlenderGIFRender Preferences")
        # self.layout.prop(self, "check_update")
        self.layout.operator("wm.url_open", text="BlenderGIFRender on Github").url = AddonSettings.GITHUB_URL


def show_message(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def ensure_dependencies(packages):
    """ `packages`: list of tuples (<import name>, <pip name>) """

    if not packages:
        return

    import site
    import importlib
    import importlib.util

    user_site_packages = site.getusersitepackages()
    if user_site_packages not in sys.path:
        sys.path.append(user_site_packages)

    modules_to_install = [module[1] for module in packages if not importlib.util.find_spec(module[0])]
    if not modules_to_install:
        return

    if bpy.app.version < (2, 91, 0):
        python_binary = bpy.app.binary_path_python
    else:
        python_binary = sys.executable

    import subprocess
    subprocess.run([python_binary, '-m', 'ensurepip'], check=True)
    # subprocess.run([python_binary, '-m', 'pip', 'install', *modules_to_install, '--user'], check=True)
    subprocess.run([python_binary, '-m', 'pip', 'install', *modules_to_install], check=True)

    importlib.invalidate_caches()


ensure_dependencies([
    ('PIL', 'Pillow')
])


def register():
    bpy.utils.register_class(GIFRenderOperator)
    bpy.utils.register_class(BlenderGIFRender)
    bpy.utils.register_class(BlenderGIFRenderPreferences)


def unregister():
    bpy.utils.unregister_class(GIFRenderOperator)
    bpy.utils.unregister_class(BlenderGIFRender)
    bpy.utils.unregister_class(BlenderGIFRenderPreferences)
    del bpy.types.Scene.my_bool
    del bpy.types.Scene.my_enum
    del bpy.types.Scene.render_file_format


if __name__ == "__main__":
    # bpy.utils.register_class(BlenderGIFRender)
    register()
