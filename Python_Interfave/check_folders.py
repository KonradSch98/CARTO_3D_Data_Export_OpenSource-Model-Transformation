import os





def check_folders(patient_folders):
    """
    This function checks if the input for the folders are correct
    After having called this function, the working directory stays globally changed
    in the one where the searched files are found

    Args:
        patient_folders (list): strings of the given patient folder names

    Returns:
        patient_folders (list): strings of the given patient folder names
    """
    
    
    
    
    # Check for folder name within directory
    def check_directory(name, dir):
        if name == dir:
            return int(True)
        else:
            return int(False)


    # Go through specific directory and search for the given patient_folders
    def search_folders_in_dir(patients, directory):
        incidence = 0
        for i in range(len(patients)):
            for k in range(len(directory)):
                incidence += check_directory(patients[i], directory[k])
        return incidence


    # Reenter patient folders if misspelled the first time e.g.
    def reenter_patient_folders():
        print("\nPlease enter the name of one or more patient data sets again "
              "(e.g. 'Patient 2014_03_10; Patient 2014_03_27'):")
        patient_folders = [ str(x) for x in input().split(";")]

        # Remove potential whitespaces before string
        for i in range(len(patient_folders)):
            patient_folders[i] = patient_folders[i].lstrip()

        return patient_folders



    # At first search the current directory
    found = 0        # Number of patient data folders found so far
    found += search_folders_in_dir(patient_folders, os.listdir())

    # Search for all patient_folders and handle the search path input
    all_patients_found = False
    while all_patients_found == False:

        # No patient data sets have been found so far
        if found == 0:
            print("\nPlease enter the full path where to find the patient "
                  "folders (format like 'C:\\Users\\USERNAME\\Desktop'):")
            path = input()

            # Check if path exists
            while os.path.isdir(path) == False:
                print("\nWARNING: The given path does not exist. You can copy it e.g. "
                      "from the topline of the file explorer.\n"
                      "\t Please enter the full path where to find the patient "
                      "folders (format like 'C:\\Users\\USERNAME\\Desktop'):")
                path = input()

            os.chdir(path)
            found += search_folders_in_dir(patient_folders, os.listdir())

            # None if the patient data sets found in the entered directory
            if found == 0:
                print("\nWARNING: No patient data found in the given directory.\n"
                      "\t Do you want to enter the patient data set names again?"
                      "  Yes/No")
                reenter = input().casefold()
                if reenter=='yes' or reenter=='y':
                    patient_folders = reenter_patient_folders()


        # All patient data sets have been found
        elif found == len(patient_folders):
            all_patients_found = True


        # Some patient data sets are missing or maybe not unique
        else:
            print("\nIt seems that some of the entered patient data names are "
                  "wrong or not all data folders are in the same directory.")
            patient_folders = reenter_patient_folders()
            found = 0
            found += search_folders_in_dir(patient_folders, os.listdir())
            if found == 0:
                print("\nWARNUNG: Non of the patient folders found.")



    print("\nEverything found. Let's start.\n")
    return patient_folders