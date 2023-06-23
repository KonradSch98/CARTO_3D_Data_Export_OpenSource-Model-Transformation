""" This function adjusts the surface modifiers apllied on the meshes
according the given resolution in the EnumProperty.
"""


def exe(tricount_low, tricount_high, subsurf_levels):
    
    #modules

    if "bpy" in locals():
        import importlib
        importlib.reload(get_objects)

    else:
        from . import get_objects


    import bpy
    mytool = bpy.context.scene.CARTO_panel
    
    #get current objects
    obs = get_objects.exe()


    for i in range(len(obs)):
        #select only current object
        bpy.context.view_layer.objects.active = None
        bpy.ops.object.select_all(action='DESELECT')
        obj = bpy.data.objects[obs[i]]
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        #set to original - delete all modifiers
        if mytool.scaling == 'OP1':
            bpy.context.object.modifiers.clear()
                            
        #set resolution to 3000 tris    
        if mytool.scaling == 'OP2':
            #add modifier if not already existant
            try:
                subs = bpy.context.object.modifiers["Subdivision"]
                subs.render_levels = subsurf_levels[i]
            except:
                bpy.ops.object.modifier_add(type='SUBSURF')
                subs = bpy.context.object.modifiers["Subdivision"]
                subs.render_levels = subsurf_levels[i]
                
            
            ratio_scale = 3000/tricount_low[i]
            #add modifier if not already existant
            try:
                deci = bpy.context.object.modifiers["Decimate"]
                deci.ratio = ratio_scale
            except:
                bpy.ops.object.modifier_add(type='DECIMATE')
                deci = bpy.context.object.modifiers["Decimate"]
                deci.ratio = ratio_scale
            
        #set resolution to 9000 tris 
        if mytool.scaling == 'OP3':
            #add modifier if not already existant
            try:
                subs = bpy.context.object.modifiers["Subdivision"]
                subs.levels = subsurf_levels[i]
                subs.render_levels = subsurf_levels[i]
            except:
                bpy.ops.object.modifier_add(type='SUBSURF')
                subs = bpy.context.object.modifiers["Subdivision"]
                subs.levels = subsurf_levels[i]
                subs.render_levels = subsurf_levels[i]
                
            ratio_scale = 9000/tricount_high[i]
            #add modifier if not already existant
            try:
                deci = bpy.context.object.modifiers["Decimate"]
                deci.ratio = ratio_scale
            except:
                bpy.ops.object.modifier_add(type='DECIMATE')
                deci = bpy.context.object.modifiers["Decimate"]
                deci.ratio = ratio_scale
    
    
    #clear selection
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    return()