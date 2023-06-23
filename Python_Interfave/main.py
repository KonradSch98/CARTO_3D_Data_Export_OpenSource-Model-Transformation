'''
Read and transfer patient data from CARTO 3D data to text file

This script reads 3D geometry data from CARTO and converts the information
into a specific text file format for later use in Blender.
'''





import os
import os.path
from check_folders import check_folders
from read_data import read_data





print("\nHello!\n"
      "Please enter the name of one or more patient data sets, e.g.: "
      "'Patient 2014_03_10'\n"
      "For multiple input, the names should be within one folder and "
      "seperated by a semicolon ';'")
patient_folders = [ str(x) for x in input().split(";")]
# Remove potential whitespaces before string
for i in range(len(patient_folders)):
    patient_folders[i] = patient_folders[i].lstrip()


# Check if all the given patient folders can be found
patient_folders = check_folders(patient_folders)


# Prepare directory to save the converted information
print("The 'converted_data' files will be stored in the patient data directory"
      " by default.")
while True:
    print("Do you want to safe it somewhere else?  Yes/No")
    elsewhere = input().casefold()

    if elsewhere=='yes' or elsewhere=='y':
        save_path = input("\nPlease enter your desired directory path:\n")
        if os.path.isdir(save_path) == False:
            try:
                os.makedirs(save_path)
            except OSError:
                print('ERROR occurred while creating the directory.')
                
        else:
            print("Directory already exists.")

        # Complete path if it is not absolut
        if os.path.isabs(save_path) == False:
            working_dir = os.getcwd()
            save_path = os.sep.join([working_dir, save_path])

        print("Stored converted data in: ", save_path)
        break


    elif elsewhere=='no' or elsewhere=='n':
        working_dir = os.getcwd()
        save_path = os.sep.join([working_dir, 'converted_data'])
        if not os.path.exists(save_path):
            os.makedirs(save_path)
           
        break


    else:
        print("\nUnexpected input, please enter 'Yes' or 'No'.")



# Read, convert and save patient data
for i in range(len(patient_folders)):

    # Create converted_data_folder named after input patient folders
    converted_data_folder = os.sep.join([save_path, patient_folders[i]])
    if not os.path.exists(converted_data_folder):
        os.makedirs(converted_data_folder)

    read_data(patient_folders[i], converted_data_folder)

print('Every given data successfully converted. Program finished.\n')