bl_info = {
    "name": "CARTO 3D panel",
    "author": "Konrad Schindler",
    "version": (1, 1),
    "blender": (2, 93, 2),
    "location": "View3D > UI > CARTO 3D",
    "description": "Panel to transfer clinical .txt data into 3D objects to view in MS HoloLens",
    "warning": "",
    "doc_url": "",
    "category": "UI Panel",
}


""" This is the main script of the CARTO3D Panel, containing all the tabs and features.

In the first part 'Import Data' the user first selects the patient_folder
e.g. 'Patient 2014_03_10' in the file explorer.
By hitting the Import button, the meshes are loaded, registered as properties
and already a little bit reduced in their complexity.

In the second part the user can chose a different destination path for the
export, if this is desired. But its not mandatory.
By hitting the Keep/Remove button, the 'not selected' will get removed 
for convenience in viewport.

In the properties tab the user can have a look at the static LAT measurements
as well as the static material version.
The 'Smooth/Flat Shade' Button is selfexplanetory and simply toggles the shading.
For the meshes resolutions there is a dropdown menu to chose from.
MIND that it is mandatory to hit the 'Apply' Button to really assign this 
property, also for later export.

The 'Export' tab and button exports all chosen meshes to a .glbfile.

!!!
To get the CARTO3D panel simply run this script.
You probably have to adjust the directory paths here down below 
and in the 'add_red_material.py' script
according to your computer.
!!!

"""









###############################################################################
        ### import scripts and modules ###

import os
import sys

if "bpy" in locals():
    import importlib
    importlib.reload(export)
    importlib.reload(get_objects)
    importlib.reload(import_meshes)
    importlib.reload(add_red_material)
    importlib.reload(path_split)
    importlib.reload(resolutions)
    importlib.reload(switching_color_display)
    importlib.reload(tricount_fct)
    importlib.reload(add_red_material)

    

else:
    from . import export
    from . import get_objects
    from . import import_meshes
    from . import add_red_material
    from . import path_split
    from . import resolutions
    from . import switching_color_display
    from . import tricount_fct
    from . import add_red_material




import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator



###############################################################################
        ### DEFAULT paths where the file explorer will generelly open ###

try:
    for root, dirs, subdirs in os.walk('D:/'):
        for d in dirs:
            if d=='CARTO System':
                for root, subdirs, files in os.walk(os.path.join(root,d)):
                    for a in subdirs:
                        if a=='patient_data':
                            data_path = os.path.join(root,a,'')

except:
    data_path=r'C:/'


#safe_DEFAULT_dir = path_split.exe(safe_path)
tricount = []
subsurf_levels = []




###############################################################################
        ### panel properties ###

#reset all assigned properties
#bpy.context.scene.property_unset('CARTO_panel')

#class to define dynamic and static PropertyGroup
class MyProperties(bpy.types.PropertyGroup):
    __annotations__ = {}
    #path where to import from
    patient_folder : bpy.props.StringProperty(name='',default='', options={'SKIP_SAVE'})
    #path where to store when export
    safe_folder : bpy.props.StringProperty(name='', default='', options={'SKIP_SAVE'})
    #dropdown property for mesh resolutions
    scaling : bpy.props.EnumProperty(
        name = 'Resolution',
        description = 'sample text',
        items = [('OP1', 'original', '',1),
                ('OP2', '3k', '', 2),
                ('OP3', '9k', '', 3)],
        default = 1
    )




###############################################################################
        ### tab defining classes ###

#class for first tab -- loading panel
class LOAD_PT_panel_context(bpy.types.Panel):
    #tab name
    bl_label = "Import Data"
    #tab identity - has to be unique - has to be registered
    bl_idname = "LOAD_PT_panel_context"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #panel where is has to appear
    bl_category = "CARTO 3D"
 
    #add Property fields  appearing inside the box     
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.CARTO_panel
        
        #this is a button
        layout.operator("loadbutton.myop_operator", icon = 'FILEBROWSER')
        #this is a field according to a property
        layout.prop(mytool, 'patient_folder')
        layout.operator("importbutton.myop_operator")




#class for second tab -- chosing panel
class CHOSE_PT_panel_context(bpy.types.Panel):
    bl_label = "Chose and Export Meshes"
    bl_idname = "CHOSE_PT_panel_context"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CARTO 3D"
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.CARTO_panel
        
        obs = get_objects.exe()
        obs.append('static_red')

        for n in range(len(obs)):
            layout.prop(mytool, obs[n]) 
        layout.operator("chosebutton.myop_operator", icon = 'TRASH')
    

            

#class for third tab -- properties panel
class PROP_PT_panel_context(bpy.types.Panel):
    bl_label = "Properties"
    bl_idname = "PROP_PT_panel_context"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CARTO 3D"
      
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.CARTO_panel
        
        #with every call of "row()" we start the next row
        row = layout.row()
        row.label(text = 'Colors', icon = 'BRUSHES_ALL')
        row = layout.row()
        row.operator('vertex_mat_button.myop_operator', text = 'Material Toggle', icon = 'OUTLINER_OB_MESH')
        row = layout.row()
        row.label(text = 'Object Resolution', icon = 'FULLSCREEN_ENTER')
        row = layout.row()
        row.operator('smoothbutton.myop_operator' , icon = 'NODE_MATERIAL')
        layout.prop(mytool, 'scaling')
        layout.operator("resbutton.myop_operator")
        
        
        


#class for last tab -- export panel
class EXPORT_PT_panel_context(bpy.types.Panel):
    bl_label = "Export"
    bl_idname = "EXPORT_PT_panel_context"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CARTO 3D"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.CARTO_panel
        
        layout.operator("safebutton.myop_operator", icon = 'FILEBROWSER')
        layout.prop(mytool, 'safe_folder')
        layout.operator("expbutton.myop_operator")        
        
        


###############################################################################
        ### button execution classes ###

#what will happen when hitting the load button in the box:
class OT_load_panel_exec(bpy.types.Operator, ImportHelper):
    """In the file browser chose the Patient folder to import data from"""
    bl_label = "Origin path"
    bl_idname = "loadbutton.myop_operator"
    

    filter_glob: StringProperty(
        default='',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        global safe_path
        global data_path
        global patient
        scene = context.scene
        mytool = scene.CARTO_panel
    
        filename, extension = os.path.splitext(self.filepath)
        #update data_path
        data_path = filename
        #get patient name
        patient = path_split.exe(filename)
        #display selected patient folder
        mytool.patient_folder = patient
        #update safe path
 
        s_path = os.path.dirname(data_path)
        safe_path = os.sep.join([s_path,'3D_Export',''])


        # try:    
        #     current_safe = path_split.exe(safe_path)
        #     if current_safe != patient:
        #         if 'Patient' in current_safe:
        #             safe_path.replace(current_safe,patient)
        #         else: 
        #             path = safe_path
        #             safe_path = os.sep.join ([path,patient])
                
        #except:

        #display accordingly selected patient folder with highest folder
        safe_displ = os.sep.join ([mytool.patient_folder, '3D_Export'])
        mytool.safe_folder = safe_displ
        
        return {'FINISHED'}
    


    def invoke(self, context, event):
        global data_path
        
        self.filepath = data_path
        wm = context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}
    



 
 #what will happen when hitting the import button in the box:
class OT_import_panel_exec(bpy.types.Operator):
    """    """
    bl_label = "Import Data"
    bl_idname = "importbutton.myop_operator"

    
    def execute(self, context):
        global data_path
        global tricount_low
        global tricount_high
        global subsurf_levels
        global patient
        
        try:
            patient
        
            #clear session
            bpy.ops.object.select_all(action='SELECT')      
            bpy.ops.object.delete(use_global=False) 
            #import the meshes from given path      
            import_meshes.exe(data_path)

            #update the boolean properties with new meshes
            bpy.utils.unregister_class(MyProperties)
            obs = get_objects.exe()
            obs.append('static_red')
            for ob in obs:
                MyProperties.__annotations__[ob] = bpy.props.BoolProperty(name=ob, default = 0, options={'SKIP_SAVE'})
            bpy.utils.register_class(MyProperties)
            bpy.types.Scene.CARTO_panel = bpy.props.PointerProperty(type= MyProperties)
            #reset object property values
            mytool = bpy.context.scene.CARTO_panel
            for ob in obs:
                mytool.property_unset(ob)
            mytool.property_unset('scaling')
        except:
            self.report({'ERROR'}, 'First!') 
        
        try:   
            #update values, add static_red material, activate vertex view per default
            tricount_low, tricount_high, subsurf_levels = tricount_fct.exe()
        except:
            self.report({'ERROR'}, 'second!') 
        try:
            add_red_material.exe()
            self.report({'INFO'}, 'All meshes successfully imported from files.')
        except:
            self.report({'ERROR'}, 'thrird!') 
        try:   
            switching_color_display.exe('VERTEX')
        except:
            self.report({'ERROR'}, 'last!')
            #self.report({'ERROR'}, 'First chose a directory in the filebrowser!')
            
        return {'FINISHED'}
    
 



       
#what will happen when hitting the destination button in the box:
class OT_safe_panel_exec(bpy.types.Operator, ImportHelper):
    """In the file browser chose the path where to store the exported data,
if different than DEFAULT"""
    bl_label = "Destination path"
    bl_idname = "safebutton.myop_operator"
    
    
    filter_glob: StringProperty(
        default='',
        options={'HIDDEN'}
    )
    

    def execute(self, context):
        global safe_path
        scene = context.scene
        mytool = scene.CARTO_panel
        
        filename, extension = os.path.splitext(self.filepath)
        #get name of highest folder
        h_folder = os.path.basename(filename)
        if h_folder == '':
            h_folder = os.path.basename(filename)
        print(h_folder)
        #update safe path
        safe_path = os.sep.join ([filename,mytool.patient_folder,'3D_Export'])
        #display selected patient folder with highest folder
        safe_displ = os.sep.join ([h_folder,mytool.patient_folder,'3D_Export'])
        mytool.safe_folder = safe_displ
        
        return {'FINISHED'}
    


    def invoke(self, context, event):
        global safe_path
        
        self.filepath = safe_path
        wm = context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}
    





#what will happen when hitting the button in the mesh box
class OT_keepremove_panel_exec(bpy.types.Operator):
    """Selected Hearts are those to keep. The rest will be deleted."""

    bl_label = "Keep and Remove"
    bl_idname = "chosebutton.myop_operator"
    
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.CARTO_panel   
        
        obs = get_objects.exe()
        #select those objects with TRUE input value
        for ob in obs:
            bool = getattr(mytool, ob)
            bpy.data.objects[ob].select_set(bool)
        
        #invers selection
        bpy.ops.object.select_all(action='INVERT')
        #delete all selected
        bpy.ops.object.delete(use_global=False)  
        
        return{'FINISHED'}
  
   


   
#what will happen when hitting the button in the mesh box
class OT_material_panel_exec(bpy.types.Operator):
    """Switch between static red and LAT colors."""
    bl_label = "Keep and Remove"
    bl_idname = "vertex_mat_button.myop_operator"
    
    
    def execute(self, context): 
        
        switching_color_display.exe()
                    
        return{'FINISHED'}  
    
    


      
 #what will happen when hitting the import button in the box:
class OT_smooth_panel_exec(bpy.types.Operator):
    """ make object surface look smooth/flat  """
    bl_label = "Smooth/Flat shade"
    bl_idname = "smoothbutton.myop_operator"
    
    
    def execute(self, context):
        global obs
        
        obs = get_objects.exe()
        bpy.ops.object.select_all(action='DESELECT') 
        #for every object toggle the shade_smooth property
        for ob in obs:
            if bpy.data.objects[ob].data.polygons[0].use_smooth == True:
                bpy.data.objects[ob].select_set(True)
                bpy.ops.object.shade_flat()
            elif bpy.data.objects[ob].data.polygons[0].use_smooth == False:
                bpy.data.objects[ob].select_set(True)
                bpy.ops.object.shade_smooth()
            bpy.data.objects[ob].select_set(False)
        
        return {'FINISHED'}





 #what will happen when hitting the import button in the box:
class OT_res_panel_exec(bpy.types.Operator):
    """    """
    bl_label = "Apply / Display resolution"
    bl_idname = "resbutton.myop_operator"
    
    
    def execute(self, context):
        global tricount_low
        global tricount_high
        global subsurf_levels
        
        resolutions.exe(tricount_low, tricount_high, subsurf_levels)
                    
        return {'FINISHED'}




            
  #what will happen when hitting the import button in the box:
class OT_exp_panel_exec(bpy.types.Operator):
    """  .  """
    bl_label = "Export"
    bl_idname = "expbutton.myop_operator"
    
    
    def execute(self, context):
        global safe_path        
        
        export.exe(safe_path)
        
        return {'FINISHED'}




#################################################################
                ### registrations ####
        
        
#register classes to blender
classes = [MyProperties,LOAD_PT_panel_context, 
            CHOSE_PT_panel_context, PROP_PT_panel_context, 
            EXPORT_PT_panel_context, OT_material_panel_exec, 
            OT_smooth_panel_exec, OT_res_panel_exec, 
            OT_exp_panel_exec, OT_import_panel_exec,
            OT_load_panel_exec, OT_safe_panel_exec,
            OT_keepremove_panel_exec]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.CARTO_panel = bpy.props.PointerProperty(type= MyProperties)
    #reset all property values to default
    #mytool = bpy.context.scene.CARTO_panel
    #props = mytool.keys()
    #for prop in props:
    #    try:
    #        mytool.property_unset(prop)
    #    except:
    #        pass
        
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        #del bpy.types.Scene.CARTO_panel

if __name__ == "__main__":
    register()
    
      