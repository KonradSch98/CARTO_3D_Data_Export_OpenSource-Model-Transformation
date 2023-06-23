""" this function is an addition to the file explorer tabs to 
get the last part of the given path string.
INPUT: the 'filename' variable given by the execution the 
filebrowser operator"""



def exe(filename):
        
    path_elements = filename.split('\\')
    #get patient folder name
    last_dir = path_elements.pop()
    while 'Patient' not in last_dir:
	    last_dir =  path_elements.pop()
	
    #strip it
    dir = last_dir.replace('/' or '\\', '')
    
    return(dir)