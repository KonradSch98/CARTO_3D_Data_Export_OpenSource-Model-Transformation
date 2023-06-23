""" this script transforms the static_red material/vertex colors to an
image texture material by baking. This is necessary for 
illustration in HoloLens.
Input: 
    type = 'RED' or 'VERTEX'
    bpy.data.objects[' '] of appropriate object"""    
    
def exe(type, obj):    
    
    import bpy

    #select object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


############################################################################
###### for Red Colors #######    
    if type == 'RED':
        
        #delete all images
        for im in bpy.data.images:
            bpy.data.images.remove(im)
            
        #delete all materials except the red one
        [bpy.data.materials.remove(m) for m in bpy.data.materials if m.name!='static_heart_material']
         
        ##### UV preperation
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        # Smart UV project for unwrapping the UV
        bpy.ops.uv.smart_project(scale_to_bounds=True)
        # Pack Island for better UV wrapping
        bpy.ops.uv.pack_islands(margin=0)
        bpy.ops.object.editmode_toggle()

        ##### material preperation   
        #select red material
        static_red = bpy.data.materials['static_heart_material']
        tree = static_red.node_tree
        #add image texture
        ima = tree.nodes.new(type='ShaderNodeTexImage')
        ima.location= (-200,500)
        #create new image for baking
        image = bpy.data.images.new(name='Redbake', width=1024, height=1024)
        #assign to node
        ima.image = image
        static_red.node_tree.nodes.active = ima

        ##### Bake preperation
        #change render engine to cycles
        bpy.context.scene.render.engine = 'CYCLES'
        #change bake type to diffuse
        bpy.context.scene.cycles.bake_type = 'DIFFUSE'
        #disable direct and indirect lighting
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False

        ##### bake
        bpy.ops.object.bake(type='DIFFUSE')

        ##### Final material changes
        #create new material
        Red_Mat = bpy.data.materials.new('Red_Mat')
        #apply to active object
        obj.data.materials.append(Red_Mat)
        #active nodes
        Red_Mat.use_nodes=True
        #node shortcut
        tree = Red_Mat.node_tree
        #add image texture
        bake_ima = tree.nodes.new(type='ShaderNodeTexImage')
        #locate it
        bake_ima.location = (-300, 0)
        #assign baking image to node
        bake_ima.image = image
        #connect image output with BSDF
        tree.links.new(  bake_ima.outputs["Color"], tree.nodes['Principled BSDF'].inputs[0])
        #remove old material
        bpy.data.materials.remove(material=static_red)
        #delete first material slot
        obj.active_material_index = 0
        bpy.ops.object.material_slot_remove()
        #assign new material
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.editmode_toggle()
    
    
############################################################################
###### for Vertex Colors #######    
    if type == 'VERTEX':
        
        ##### Material preperation for single objects
        for x in obj.material_slots:
            obj.active_material_index = 0
            bpy.ops.object.material_slot_remove()
            
            
        ##### UV preperation
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        # Smart UV project for unwrapping the UV
        bpy.ops.uv.smart_project(scale_to_bounds=True)
        # Pack Island for better UV wrapping
        bpy.ops.uv.pack_islands(margin=0)
        bpy.ops.object.editmode_toggle()

        ##### material preperation   
        #create new material
        Vert_Mat = bpy.data.materials.new('Vert_Mat_%s' %obj.name)
        #apply to active object
        bpy.context.object.data.materials.append(Vert_Mat)
        #active nodes
        Vert_Mat.use_nodes=True
        #node shortcut
        tree = Vert_Mat.node_tree
        #add VertexColor node
        vertex = tree.nodes.new(type='ShaderNodeVertexColor')
        #locate it
        vertex.location= (-200,300)
        #use objects vertex colors
        #bpy.data.materials['Vert_Mat_%s' %obj.name].node_tree.nodes["Vertex Color"].layer_name = "Col"
        #connect vertex output mit BSDF input
        tree.links.new(  vertex.outputs["Color"], tree.nodes['Principled BSDF'].inputs[0])
        #add image texture
        ima = tree.nodes.new(type='ShaderNodeTexImage')
        #locate it
        ima.location = (-300, 0)
        #create new image for baking
        image = bpy.data.images.new(name='Vertbake_%s' %obj.name, width=1024, height=1024)
        #assign to node
        ima.image = image

        ##### Bake preperation
        #change render engine to cycles
        bpy.context.scene.render.engine = 'CYCLES'
        #change bake type to diffuse
        bpy.context.scene.cycles.bake_type = 'DIFFUSE'
        #disable direct and indirect lighting
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False

        ##### bake
        bpy.ops.object.bake(type='DIFFUSE')

        ##### Final material changes
        #remove vertex node
        tree.nodes.remove(vertex)
        #connect image output with BSDF
        tree.links.new(  ima.outputs["Color"], tree.nodes['Principled BSDF'].inputs[0])
        #assign new material
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.editmode_toggle()