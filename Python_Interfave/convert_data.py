import os





def convert_data(file, mesh_or_car, save_path, file_count):
    """
    Function to read and convert various data from exported CARTO files

    Get mesh data with 'mesh_or_car = 0' and and car data with 'mesh_or_car = 1'.
    The converted data is written to a new file for mesh or LAT values respectively

    Args:
        file (str): Full name of the file. mesh or car file
        mesh_or_car (int): specifies whether its a mesh or car file 
        save_path (str): Path where the converted data will be stored
        file_count (int): specifies the i-th file of one patient
    """
    
    
    

    # Converting the mesh file
    # saves vertex, face and color data
    if mesh_or_car == 0:

        mesh_file = open(file, 'r')
        next_line = mesh_file.readline()

        # Skip the first irrelevant lines
        while next_line != "[VerticesSection]\n":
            next_line = mesh_file.readline()
        next(mesh_file)
        next(mesh_file)


        # Read the vertices
        vertices = []
        # Keep reading as long as there are vertex lines
        next_line = mesh_file.readline()
        while next_line != '\n':
            vertices.append(next_line.split())
            next_line = mesh_file.readline()



        # Skip the next 3 lines until the next data starts
        for i in range(3):
            next(mesh_file)

        # Read the faces
        faces = []
        # Keep reading as long as there are face lines
        next_line = mesh_file.readline()
        while next_line != '\n':
            faces.append(next_line.split())
            next_line = mesh_file.readline()



        # Skip the next 3 lines until the next data starts
        for i in range(4):
            next(mesh_file)

        # Read the colors
        colors = []
        # Keep reading as long as there are color lines
        next_line = mesh_file.readline()
        while next_line != '\n':
            colors.append(next_line.split())
            next_line = mesh_file.readline()

        index = []
        lat = []
        lat_scale = []

        #get LAT values from color section
        for i in range(len(colors)):
            if float(colors[i][4]) != -10000.0:
                index.append(colors[i][0])
                lat.append(float(colors[i][4]))


        # Scale LAT values for use in Blender
        max_LAT = max(lat)
        min_LAT = min(lat)
        lat_range = abs(min_LAT) + max_LAT

        if lat_range != 0:
            for i in range(len(lat)):
                lat_scale.append((lat[i] + abs(min_LAT)) * 0.85 / lat_range)
        else:
            for i in range(len(lat)):
                lat_scale.append((lat[i] * 0.85 / lat[i]))


        # Prepare new file / directory
        working_dir = os.getcwd()   # Save current directory to come back later
        os.chdir(save_path)

        # Open and write to mesh file
        new_file = open('Mesh_exp_%i.txt' %file_count, 'w')
        # Write information header
        new_file.write(str(len(vertices)) + '\t' + str(len(faces)) + '\t' + str(len(lat_scale)) + '\n' )

        # Write the vertices
        for i in range(len(vertices)):
            new_file.write(vertices[i][2] + '\t\t' + vertices[i][3] + \
                                            '\t\t' + vertices[i][4] + '\n')

        # Write the faces / triangles
        for i in range(len(faces)):
            new_file.write(faces[i][2] + '\t' + faces[i][3] + \
                                         '\t' + faces[i][4] + '\n')

        # Write colors
        for i in range(len(lat)):
            new_file.write(index[i] + '\t' + str("{:.5f}".format(lat_scale[i])) + '\n')

        # Close and go back to data directory
        new_file.close()
        os.chdir(working_dir)



    # Converting the car file / LAT data
    # simply takes the index and LAT value from car without change
    elif mesh_or_car == 1:

        car_file = open(file, 'r')
        next(car_file)                # Skip the first irrelevant line

        lines = car_file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].split()

        car_data = []
        lat = []

        for i in range(len(lines)):
            car_data.append(list(lines[i][2].split()))
            lat.append(int(lines[i][12]))


        # Scale LAT values for use in Blender
        max_LAT = max(lat)
        min_LAT = min(lat)
        lat_range = abs(min_LAT) + max_LAT
        for i in range(len(car_data)):
            car_data[i].append((lat[i] + abs(min_LAT)) * 0.85 / lat_range)

        # Prepare new file / directories
        working_dir = os.getcwd()   # Save current directory to come back later
        os.chdir(save_path)


        # Open and write to file
        new_file = open('Mesh_LAT_%i.txt' %file_count, 'w')
        # Write information header
        new_file.write(str(len(car_data)) + '\n')

        # Write the car_data
        for i in range(len(car_data)):
             new_file.write(car_data[i][0] + '\t\t' + str(car_data[i][1]) + \
                            '\n')

        # Close and go back to data directory
        new_file.close()
        os.chdir(working_dir)
