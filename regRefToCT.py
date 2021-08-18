#!/usr/bin/env python
# coding: utf-8

import sys,os
import fnmatch

dockerRootDir = '/home/jovyan/'

from registerRefAndROIsToCT import main as registerRefAndROIsToCT

def main(inputDir,regNiftiDir):
    
    # Create outDir if it doesn't exist
    createRegNiftiDir(regNiftiDir)
    
    # CT volume format
    imgType = 'nii'
    
    # Args for registration step function
    imgType_arg = '-t' + imgType
    regDir_arg = '-r' + dockerRootDir
    outDir_arg = '-o' + regNiftiDir
    
    # Get all the available .nii CT volumes from the nifti folder
    inputImgs = [f for f in os.listdir(inputDir) if fnmatch.fnmatch(f,'*' + imgType)] # Input scans
    
    # Loop through the available volumes 
    # Register each volume to the reference volume
    for imgNum,inputImg in enumerate(inputImgs, start=1): 
    
        inputImg_arg = '-i' + inputDir + inputImg
        
        # Registration step
        myArgs = [imgType_arg,regDir_arg,inputImg_arg,outDir_arg]
    
        try:
            print(str(imgNum) + '/' + str(len(inputImgs)) + ' Registering reference to ' + inputImg)
            registerRefAndROIsToCT(myArgs)
        except:
            print('ERROR: Registration step failed!')

###################    
def createRegNiftiDir(regNiftiDir):
    
    # Create output folder for niftis if it doesn't exist
    try:
        os.mkdir(regNiftiDir)
    except:
        if(os.path.exists(regNiftiDir)):
            pass
        else:
            print('regNiftiDir could not be created!')
            sys.exit(1)  

if __name__ == "__main__":
    main(sys.argv[1:])