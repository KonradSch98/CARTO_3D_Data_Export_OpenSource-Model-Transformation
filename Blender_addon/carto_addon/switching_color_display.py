""" Switch between Vertex color or Material display Mode.
INPUT:
none: it toggles.
for type='VERTEX' it changes to vertex mode.
for type='MATERIAL' it changes to material mode."""


def exe(type = None):
    import bpy
    areas = bpy.context.screen.areas
    
    if type == None:
        for area in areas: 
            if area.type == 'VIEW_3D':
                for space in area.spaces: 
                    if space.type == 'VIEW_3D':
                        shader = space.shading.type
                        
        if shader == 'SOLID':
            for area in areas: 
                if area.type == 'VIEW_3D':
                    for space in area.spaces: 
                        if space.type == 'VIEW_3D':
                            space.shading.type = 'MATERIAL'
                            
        if shader == 'MATERIAL':
            for area in areas: 
                if area.type == 'VIEW_3D':
                    for space in area.spaces: 
                        if space.type == 'VIEW_3D':
                            space.shading.type = 'SOLID'
                            space.shading.color_type = 'VERTEX' 
                        
    if type == 'VERTEX':
        for area in areas: 
            if area.type == 'VIEW_3D':
                for space in area.spaces: 
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'SOLID'
                        space.shading.color_type = 'VERTEX'
    
    if type == 'MATERIAL':
        for area in areas: 
            if area.type == 'VIEW_3D':
                for space in area.spaces: 
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'