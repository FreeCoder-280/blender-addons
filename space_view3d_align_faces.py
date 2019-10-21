import bpy
import math
from mathutils import Vector
from functools import reduce

bl_info = {
    "name": "Align by faces",
    "description": "Align two objects by their active faces",
    "author": "Tom Rethaller (branch GUI & Blender 2.8 by FreeCoder-280)",
    "version": (0,3,0),
    "blender": (2, 80, 2),
    "location": "3D View > UI",
    "warning": "",
    "category": "Mesh",
    "wiki_url": "https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Align_by_faces/",
    "tracker_url": "https://github.com/trethaller/blender-addons",
#    "support": "TESTING",	# "Testing" may hide the AddOn; defaults to "Community"
}

classes = []

def get_ortho(a,b,c):
    if c != 0.0 and -a != b:
        return [-b-c, a,a]
    else:
        return [c,c,-a-b]

def clamp(v,min,max):
    if v < min:
        return min
    if v > max:
        return max
    return v

def align_faces(from_obj, to_obj):
    fpolys = from_obj.data.polygons
    tpolys = to_obj.data.polygons
    fpoly = fpolys[fpolys.active]
    tpoly = tpolys[tpolys.active]
    
    to_obj.rotation_mode = 'QUATERNION'
    tnorm = to_obj.rotation_quaternion @ tpoly.normal
    
    fnorm = fpoly.normal
    axis = fnorm.cross(tnorm)
    dot = fnorm.normalized().dot(tnorm.normalized())
    dot = clamp(dot, -1.0, 1.0)
    
    # Parallel faces need a new rotation vector
    if axis.length < 1.0e-8:
        axis = Vector(get_ortho(fnorm.x, fnorm.y, fnorm.z))
        
    from_obj.rotation_mode = 'AXIS_ANGLE'
    from_obj.rotation_axis_angle = [math.acos(dot) + math.pi, axis[0],axis[1],axis[2]]
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()     
    
    # Move from_obj so that faces match
    fvertices = [from_obj.data.vertices[i].co for i in fpoly.vertices]
    tvertices = [to_obj.data.vertices[i].co for i in tpoly.vertices]
    
    fbary = from_obj.matrix_world @ (reduce(Vector.__add__, fvertices) / len(fvertices))
    tbary = to_obj.matrix_world @ (reduce(Vector.__add__, tvertices) / len(tvertices))
    
    from_obj.location = tbary - (fbary - from_obj.location)


class OBJECT_OT_AlignByFaces(bpy.types.Operator):
    bl_label = "Align by faces"
    bl_description= "Align two objects by their active faces"
    bl_idname = "object.align_by_faces"

    @classmethod
    def poll(cls, context):
        if not len(context.selected_objects) is 2:
            return False
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                return False
        return True

    def execute(self, context):
        objs_to_move = [o for o in context.selected_objects if o != context.active_object]
        for o in objs_to_move:
            align_faces(o, context.active_object)
        return {'FINISHED'}
# end class
classes += [OBJECT_OT_AlignByFaces]

# Panel
class OBJECT_PT_PreviewsPanel(bpy.types.Panel):
    bl_category = "Align"
    bl_label = "Align by Face"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        # Usage Info
        col = layout.column(align=True)
        rowsub = col.row(align=True)    
        rowsub.label(text="Workflow:")
        rowsub = col.row(align=True)    
        rowsub.label(text="- Select face on objA in editmode")
        rowsub = col.row(align=True)    
        rowsub.label(text="- Select face on objB in editmode")
        rowsub = col.row(align=True)    
        rowsub.label(text="- Select objA and objB in objectmode")
        rowsub = col.row(align=True)    
        rowsub.label(text="(objA will be moved to objB)")

        # Button only enabled if two mesh object are selected
        check_enabled = True
        if not len(context.selected_objects) is 2:
            check_enabled = False
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                check_enabled = False
         # Button for the action
        rowsub = col.row(align=True)
        rowsub.operator("object.align_by_faces", icon="SNAP_ON", text="FaceToFace ObjA to ObjB")
        rowsub.enabled = check_enabled 

# end class
classes += [OBJECT_PT_PreviewsPanel]

def register():
    from bpy.utils import register_class

    for cls in classes:
         register_class(cls)

def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
         unregister_class(cls)

if __name__ == "__main__":
    register()
