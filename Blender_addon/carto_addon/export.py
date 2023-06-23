




def exe(safe_path):
    
    #modules
    import os

    
    if "bpy" in locals():
        import importlib
        importlib.reload(get_objects)
        importlib.reload(bake)

    else:
        from . import get_objects
        from . import bake




    import bpy
    mytool = bpy.context.scene.CARTO_panel
    
    # prepare safing directory
    if not os.path.exists(safe_path):
        os.makedirs(safe_path)

    ######## export every remaining mesh each alone #######
    obs = get_objects.exe()
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    


############################################################################
###### for Red Colors mesh if chosen #######    
    try:
        if mytool['static_red'] == True:
            if len(obs)>1:
                static_mesh = 1
            else:
                static_mesh=0
            
            obj = bpy.data.objects[obs[static_mesh]]
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.duplicate(linked = False)
            copy = bpy.context.selected_objects[0]
            copy.select_set(True)
            bpy.context.view_layer.objects.active = copy
                
            bake.exe('RED', copy)
            
            bpy.ops.object.convert(target="MESH")
            
            ##### for accurate centering and scale
            repeat=0
            while repeat<2:
                #center to mass volume
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
                #center to origin
                copy.location[0]=0
                copy.location[1]=0
                copy.location[2]=0
                repeat+=1
            
            for i in range(0,3):
                #scale
                copy.scale[0]=0.02
                copy.scale[1]=0.02
                copy.scale[2]=0.02    
            
            path = os.sep.join([safe_path,'static_red'])
            bpy.ops.export_scene.gltf(filepath=path, use_selection=True, export_materials = 'EXPORT', export_colors = False)

            bpy.ops.object.delete()
    except:
        pass  
        
        
############################################################################
###### for vertex Color meshes #######         
    for ob in obs:
        try:
            mytool[ob]
            if mytool[ob] == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None
                obj = bpy.data.objects[ob]
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                
                bpy.ops.object.duplicate(linked = False)
                copy = bpy.context.selected_objects[0]
                copy.select_set(True)
                
                bake.exe('VERTEX', copy)
                
                bpy.ops.object.convert(target="MESH")
                
                        
                ##### for accurate centering and scale
                repeat=0
                while repeat<2:
                    #center to mass volume
                    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

                    #center to origin
                    copy.location[0]=0
                    copy.location[1]=0
                    copy.location[2]=0
                    repeat+=1
                        
                for i in range(0,3):
                    #scale
                    copy.scale[0]=0.02
                    copy.scale[1]=0.02
                    copy.scale[2]=0.02 
                
                path = os.sep.join([safe_path,ob])
                bpy.ops.export_scene.gltf(filepath=path, use_selection=True, export_materials = 'EXPORT', export_colors = False)
                
                bpy.ops.object.delete()
        
        except:
            pass
        
    return()