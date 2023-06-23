""" This script imports the meshes from the data previously 
cleaned and prepared by the external python script.
The meshes get imported as well as their static LAT values
which get applied to their surface. 
The meshes will also get already reduced in their complexity
since CARTO usually has some redundant faces in their data.

INPUT: the whole data path for the desired patient data
    eg. 'D:\Documents\CARTO System\patient_data\converted_data\Patient 2014_03_27'

"""



def exe(data_path):

    #moduls
    
    if "bpy" in locals():
        import importlib
        importlib.reload(get_objects)

    else:
        from . import get_objects



    import bpy
    import os
    import colorsys
    
    
    ####### find files #######################

    conv_data = os.listdir(data_path)
    mesh_files = [elem for elem in conv_data if 'Mesh_exp' in elem]


    ####### read data from files #######################

    for k in range(len(mesh_files)):
        
        file = open( data_path + r'/' + mesh_files[k])
        #reads the three numbers at the top into list of strings (vert/face/color counts)
        counts=file.readline().split()                
        #maps the elemets in "Counts" into integers and puts them into a list
        counts = list(map(int,counts))                

        #### read vertices
        vert_data=[]                                  
        i=0   
        #beause we already read counts, the line pointer is already at the second line 
        #read lines as long as line_index is lower than vert_count                                       
        while i<counts[0]:    
            #read next line                        
            line=file.readline()                      
            #store this line (X,Y,Z) (converted as float) as new list_line in rows
            vert_data.append(list(map(float,line.split())))   
            i+=1                                      

        ##### read faces
        face_data=[]
        j=0
        while j<counts[1]:                  
            line=file.readline()
            face_data.append(list(map(int,line.split())))   
            j+=1
        
        ##### read colors
        color_data=[]
        m=0
        while m<counts[2]:                  
            line=file.readline()
            color_data.append(list(map(float,line.split())))   
            m+=1
        
        file.close()


    ####### create meshes #######################
        
        #no edges specifically given
        edges=[]

        #declare a name
        name = "Heart_%i" %(k+1)                                                
        mesh = bpy.data.meshes.new(name)
        #create a new object from name and mesh                                       
        obj = bpy.data.objects.new(name, mesh)  
        #get collection pointer                                 
        col = bpy.data.collections.get("Collection") 
        #associate this object to a collection, so that it's visible                           
        col.objects.link(obj)           
        #show it in the viewport                                        
        bpy.context.view_layer.objects.active = obj    
        #load data from python lists into the mesh                         
        mesh.from_pydata(vert_data, edges, face_data)                           
        bpy.data.objects[name].select_set(True)      
        #set objects origin to geometry                           
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN') 
        #change location     
        bpy.ops.transform.translate(value=(k*150 , 0, 0))    
        
        

    ####### assign colors #######################
                                                                               
        current_mesh = bpy.context.active_object                                
        mesh_data = current_mesh.data                  
        #make new vertex_color layer                         
        assign_color=mesh_data.vertex_colors.new()                              

        l=0
        while l<counts[2]:                                                       
            
            #go through the color data and convert the information
            #from HSV rainbow projection to RGB
            line=color_data[l]
            #pick the first entry as vertex_index                                                   
            vert=line[0]                                                         
            rgb=colorsys.hsv_to_rgb(line[1],1,1)                                 
            rgb=list(rgb)
            #add a 1 just for internal syntax
            rgb.append(1)                                                        
            l+=1
            
            #the original vertex_order is stored in the faces_order and equivalently inside every face
            #go through the faces
            for poly in mesh_data.polygons:                                      
                #go through loops of this face
                for loop_index in poly.loop_indices:                                
                    #get vertex_index for this one
                    loop_vert_index = mesh_data.loops[loop_index].vertex_index   
                    #check if its the vertex of the file 
                    if vert == loop_vert_index:                 
                        #print the color to this face_vertex                  
                        assign_color.data[loop_index].color = rgb                
        
        
        bpy.data.objects[name].select_set(False)                                
        file.close()
        
        
    
    ####### reduce mesh's complexity #######################
    
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.tris_convert_to_quads()
        bpy.ops.mesh.vert_connect_nonplanar()
        #remove all redundant faces
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_interior_faces()
        bpy.ops.mesh.delete(type='FACE')
        #remove close vertices by interpolated value
        dim_vec = obj.dimensions
        merg_val = ( (dim_vec[0] + dim_vec[1] + dim_vec[2] ) / 3 / 70 )**2
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=merg_val)
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        bpy.ops.object.editmode_toggle()
        

        #clear selection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
        
    
    return()