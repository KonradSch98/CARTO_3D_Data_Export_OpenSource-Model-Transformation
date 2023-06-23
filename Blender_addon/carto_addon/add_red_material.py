""" this script imports the static red material and then assigns it
to the second mesh, if it exists, otherwise to the first."""

def exe():
    
    
    
    
    ##################################################################################
    
    #path where the 'static_red_heart_material.blend' lies. Path not including the actual file!
    path = r"D:\Eigene Dokumente\Uni\Semester 8\HIWI FMA\Scripts\Blender\serious"
    
    ##################################################################################
    
    
    
    #moduls

    if "bpy" in locals():
        import importlib
        importlib.reload(get_objects)

    else:
        from . import get_objects



    import bpy 
    import os

    
    #clear selection
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    
    #clear materials
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)

    obs = get_objects.exe()
    #2 or 1 mesh
    if len(obs)>1:
        static_mesh = 1
    else:
        static_mesh=0
        
    #select object
    obj = bpy.data.objects[obs[static_mesh]]
    obj.select_set(True) 
    #save objects location
    loc = []
    for i in range(3):
        loc.append(obj.location[i])
    #origin to 3D cursor
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    #goemetry to origin
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    #add empty , relevant for proper look of material
    bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    #select also mesh
    bpy.context.view_layer.objects.active = obj
    #parent empty to mesh
    bpy.ops.object.parent_set(type='OBJECT')


    #append material
    mat = "static_heart_material"
    ending = 'static_red_heart_material.blend\Material'
    whole_path = os.sep.join([path, ending])
    bpy.ops.wm.append(filename = mat, directory = whole_path)


    #asign material to mesh
    mat = bpy.data.materials.get("static_heart_material")
    obj.data.materials.append(mat)
    #edit driver values in material
    val_nodes = ["Value","Value.001","Value.002"]
    trans_drive = ["LOC_X","LOC_Y","LOC_Z"]
    for i in range(3):
        drive = bpy.data.materials["static_heart_material"].node_tree.nodes[val_nodes[i]].outputs[0].driver_add("default_value")
        drive.driver.type = 'SUM'
        var = drive.driver.variables.new()
        var.type = 'TRANSFORMS'
        var.targets[0].id = bpy.data.objects["Empty"]
        var.targets[0].transform_type = trans_drive[i]
    
    #reassign objects location
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    obj.location = loc
    
    #clear selection
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
