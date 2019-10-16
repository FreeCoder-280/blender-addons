# blender-addons
#
# Master by Tom Rethaller (https://github.com/trethaller/blender-addons)
# Branch by (FreeCoder-280 :-)
#----------------------------------------------------------------------------

Fork (Blender2.8+UI)
----

Install "space_view3d_align_faces.py" (Edit - Preferences - Add-ons - Install...)

Enable the just installed Add-on "Mesh: Align by faces" (mark it active)

The "Align" tab contains the "Align by Face" region

- "Workflow:" contains the same steps as the Master script
  => Editmode: Choose one face in each of your objects you want to snap (align) together.
  => Objectmode: Select the object which will be moved, then add the second object to this selection.

- Button "FaceToFace ObjA to ObjB" is greyed out until you select two(!) mesh objects
  => Push the button and enjoy the magic

#----------------------------------------------------------------------------

Links (Master)
-----

https://cgmasters.net/free-tutorials/blender-tutorial-align-2-faces/
https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Align_by_faces/
https://github.com/trethaller/blender-addons

#----------------------------------------------------------------------------

Blender Wiki (Master)
------------

Very simple script that aligns two objects using their active faces. 

Workflow: 
• Enter editmode on object A 
• Select desired face on object A 
• Exit editmode 
• Enter editmode on object B 
• Select desired face on object B 
• Exit editmode 
• Select A and B (order matters) 
• Invoke script (Spacebar > search "Align by faces") 

Result: A is moved and aligned on B, the two faces matching perfectly 
Category: Script (no GUI)
