
""" This function counts the mesh tris in case a Subsurf mod is applied.
Will later be used for resolution calculation for decimate mod.""" 


def exe():
    #modules

    
    if "bpy" in locals():
        import importlib
        importlib.reload(get_objects)

    else:
        from . import get_objects


    import bpy
    
    obs = get_objects.exe()
        
    tricount_low=[]
    tricount_high=[]
    subsurf_levels=[]
    
    for ob in obs:
        levels = 1
        while True:
            #select only current object
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            obj = bpy.data.objects[ob]
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            #duplicate it
            bpy.ops.object.duplicate(linked = False)
            copy = bpy.context.selected_objects[0]
            copy.select_set(True)
            #remove all possible modifiers
            bpy.context.object.modifiers.clear()
            #add a subsurf mod
            bpy.ops.object.modifier_add(type='SUBSURF')
            subs = bpy.context.object.modifiers["Subdivision"]
            subs.levels = levels
            subs.render_levels = levels
            #apply the modifier to the mesh
            bpy.ops.object.convert(target="MESH")
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            #triangulate the mesh
            bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
            bpy.ops.object.editmode_toggle()
            mesh = copy.data
            #count the triangal faces of the mesh
            tri_count=0
            for poly in mesh.polygons:
                if len(poly.vertices) == 3:
                    tri_count += 1
            bpy.ops.object.delete()
            
            #save count for lower subsurf levels anyways
            if levels == 1:
                tricount_low.append(tri_count)

            #if the count is lover than 9000, increase the subsurf level
            #and repeat count for higher count
            if tri_count>=9000:
                subsurf_levels.append(levels)
                tricount_high.append(tri_count)
                break
            else:
                levels+=1
                
        
    

    return(tricount_low, tricount_high, subsurf_levels)