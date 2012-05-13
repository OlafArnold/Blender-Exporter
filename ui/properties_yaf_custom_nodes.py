# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from bpy.types import (NodeTree,
                       NodeSocket,
                       Menu,
                       Node)


# Implementation of custom nodes from Python
# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class YAF_CustomTree(NodeTree):
    bl_idname = 'ACustomTreeType'
    bl_label = 'YafaRay Node Tree'
    bl_icon = 'SMOOTH'

    def draw_add_menu(self, context, layout):
        # layout.label("YafaRay Nodes")
        layout.menu("YAF_MT_AddShader")


# Custom socket type
class YAF_BSDF_CustomSocket(NodeSocket):
    '''Custom node socket type'''
    bl_idname = "BSDF_SocketType"
    bl_label = "BSDF"
    # NodeSocket color
    bl_color = (0.39, 0.78, 0.39, 1.0)

    # Enum items list
    my_items = [
        ("DOWN", "Down", "Where your feet are"),
        ("UP", "Up", "Where your head should be"),
        ("LEFT", "Left", "Not right"),
        ("RIGHT", "Right", "Not left")
    ]

    myEnumProperty = bpy.props.EnumProperty(name="Direction", description="Just an example", items=my_items, default='UP')


# Derived from the Node base type.
class YAF_ShinyDiffuseNode(Node):
    ''' Shiny Diffuse custom node'''
    bl_idname = 'ShinyDiffuseNodeType'
    bl_label = 'Shiny Diffuse BSDF'
    bl_icon = 'MATERIAL'

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties

    # myStringProperty = bpy.props.StringProperty()
    # myFloatProperty = bpy.props.FloatProperty(default=3.1415926)

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!
    def init(self):
        self.inputs.new('RGBA', "Diffuse Color")
        self.inputs.new('RGBA', "Mirror Color")
        self.inputs.new('FLOAT', "Mirror Amount")
        self.inputs.new('FLOAT', "Transparency")
        self.inputs.new('FLOAT', "Translucency")
        self.inputs.new('FLOAT', "Bump")

        self.outputs.new('BSDF_SocketType', "BSDF")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        mat = bpy.context.active_object.active_material
        layout.prop(mat, "brdf_type")
        layout.prop(mat, "sigma")

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        mat = bpy.context.active_object.active_material
        layout.prop(mat, "brdf_type")
        layout.prop(mat, "sigma")


class YAF_GlossyNode(Node):
    ''' Glossy custom node'''
    bl_idname = 'GlossyNodeType'
    bl_label = 'Glossy BSDF'
    bl_icon = 'SOUND'

    def init(self):
        self.inputs.new('RGBA', "Diffuse Color")
        self.inputs.new('RGBA', "Glossy Color")
        self.inputs.new('FLOAT', "Glossy Amount")
        self.inputs.new('FLOAT', "Bump")

        self.outputs.new('BSDF_SocketType', "BSDF")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        mat = bpy.context.active_object.active_material
        layout.prop(mat, "brdf_type")
        layout.prop(mat, "sigma")

    def draw_buttons_ext(self, context, layout):
        mat = bpy.context.active_object.active_material
        layout.prop(mat, "brdf_type")
        layout.prop(mat, "sigma")


class YAF_MT_AddShader(Menu):
    bl_label = "Shader"

    def draw(self, context):
        layout = self.layout

        layout.operator("node.add_node", text="Shiny Diffuse BSDF").type = 'ShinyDiffuseNodeType'
        layout.operator("node.add_node", text="Glossy BSDF").type = 'GlossyNodeType'


def register():
    bpy.utils.register_class(YAF_CustomTree)
    bpy.utils.register_class(YAF_BSDF_CustomSocket)
    bpy.utils.register_class(YAF_ShinyDiffuseNode)
    bpy.utils.register_class(YAF_GlossyNode)


def unregister():
    bpy.utils.unregister_class(YAF_CustomTree)
    bpy.utils.unregister_class(YAF_BSDF_CustomSocket)
    bpy.utils.unregister_class(YAF_ShinyDiffuseNode)
    bpy.utils.unregister_class(YAF_GlossyNode)


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
