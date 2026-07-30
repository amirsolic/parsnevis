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
    "name" : "parsnevis",
    "author" : "Amirsolic", 
    "description" : "Correcting the formatting of Persian and Arabic texts in Blender",
    "blender" : (4, 2, 0),
    "version" : (1, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import sys
import os
import bpy

addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

import arabic_reshaper
import bidi
from bidi.algorithm import get_display

addon_keymaps = {}
_icons = None
import os



def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


class SNA_PT_PARSNEVIS_83188(bpy.types.Panel):
    bl_label = 'parsnevis'
    bl_idname = 'SNA_PT_PARSNEVIS_83188'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'parsnevis'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
    
    def draw(self, context):
        layout = self.layout
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "ico.png")
        layout.template_icon(icon_value=load_preview_icon(icon_path), scale=9.609999656677246)
        op = layout.operator('sna.formatc_b2bf3', text='format correction', icon_value=663, emboss=True, depress=False)


class SNA_OT_Formatc_B2Bf3(bpy.types.Operator):
    bl_idname = "sna.formatc_b2bf3"
    bl_label = "formatc"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        import arabic_reshaper
        obj = bpy.context.active_object
        if obj and obj.type == 'FONT':
            original_text = obj.data.body
            reshaped_text = arabic_reshaper.reshape(original_text)
            bidi_text = get_display(reshaped_text)
            obj.data.body = bidi_text
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_PT_PARSNEVIS_83188)
    bpy.utils.register_class(SNA_OT_Formatc_B2Bf3)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_PT_PARSNEVIS_83188)
    bpy.utils.unregister_class(SNA_OT_Formatc_B2Bf3)
