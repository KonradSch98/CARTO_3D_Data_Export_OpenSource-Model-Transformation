""" this function basically writes all the mesh objects on the scene in one list"""


def exe():
    import bpy 
    
    #get list with all objects in collection
    obs = []
    for obj in bpy.data.collections['Collection'].all_objects:
        obs.append(obj.name)
    #remove "Empty"s used for materials
    try:
        for ob in obs:
            if 'Empty' in ob:
                obs.remove(ob)
    except:
        pass
    
    return(obs)