#!/usr/bin/env python
# coding: utf-8

import sys,getopt
import os
import fnmatch
import shutil

def main(argv):
    
    imgType = 'nii'  
    
    regDir = '' # Mounted volume with registration data 
    outDir = '' # Folder where to store output registration and transformed ROIs
    inputImg = '' # CT volume converted from DICOM to selected imgType
    
    try:
        opts, args = getopt.getopt(argv,"ht:r:i:o:",["imgType=","regDir=","inputImg=","outDir="])
    except getopt.GetoptError:
        print(argv)
        print('Error-registerRefAndROIstoCT.py -t <imgType> -r <regDir> -i <inputImg> -o <outDir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('registerRefAndROIstoCT.py -t <imgType> -r <regDir> -i <inputImg> -o <outDir>')
            sys.exit()
        elif opt in ("-t", "--imgType"):
            imgType = '.' + arg
        elif opt in ("-r", "--regDir"):
            regDir = arg
        elif opt in ("-i", "--inputImg"):
            inputImg = arg
        elif opt in ("-o", "--outDir"):
            outDir = arg
    
    # Add Elastix path to environment variables
    elastixDir = regDir
    elastix_envVar(elastixDir)
    
    # Check imgType
    if imgType != '.nii':
        print('Change registration parameters to match imgType!')
        
    # Path to reference data
    refDataDir = regDir + 'qa4iqi/refData/'
    
    # Get paths
    refImgs = [f for f in os.listdir(refDataDir) if fnmatch.fnmatch(f,'refCT-*')] # Reference scan
    allRois = [f for f in os.listdir(refDataDir) if fnmatch.fnmatch(f,'*ROI-*')] # Reference rois
        
    if len(refImgs) == 0:
        print('No reference CTs found in ' + refDataDir)
    elif len(refImgs) > 1:
        print('Too many reference CTs...')
    else:
        refImg = refDataDir + refImgs[0]   
        
    # Registration parameters for Elastix
    regParams = regDir + 'params/QA4IQI_regParams.txt'
    
    # Create out directory for registered images
    (tmpDir,outDir) = setReg_createDirs(outDir)
    
    inputImgID = inputImg.split("/")[-1][:-len(imgType)]
    
    elastixCall = 'elastix -f ' + inputImg + ' -m ' + refImg + ' -out ' + tmpDir + ' -p ' + regParams
    
    # Call Elastix registration for CT images
    regLog = os.system(elastixCall)
    
    if regLog != 0:
        print('There were errors in the registration process...')
    
    # Scan volume output transform
    transf_params = tmpDir + 'TransformParameters.0.txt'
    
    # Use output transformation to transform reference rois
    transformRois(allRois,inputImgID,refDataDir,tmpDir,outDir,transf_params,imgType)
    
    # Remove temp folder
    shutil.rmtree(tmpDir) 
    
    # Compress original nifti file
    os.system('gzip ' + inputImg) 

    
##############################
def elastix_envVar(elastixDir):
    elastixPath = elastixDir +'elastix-5.0.0-Linux'

    os.environ['PATH'] = elastixPath + '/bin:' + os.environ['PATH']
    os.environ['LD_LIBRARY_PATH'] = elastixPath + '/lib'     

##############################
def setReg_createDirs(outDir):    
    try:
        os.mkdir(outDir)
    except:
        pass         # Folder already exists
        
    # Create temp directory for registration output
    tmpDir = outDir + 'tmp/'
    
    try:
        os.mkdir(tmpDir)  
    except: 
        shutil.rmtree(tmpDir)
        os.mkdir(tmpDir)

    return (tmpDir,outDir)

##############################
def setReg_scanOutput(tmpDir,outDir,inputImgID,imgType):
    regImg = tmpDir + 'result.0' + imgType
    regImg_newID = outDir + 'regCT_' + inputImgID + imgType
    os.rename(r'' + regImg,r'' + regImg_newID)
    
##############################
def transformRois(allRois,inputImgID,refDir,tmpDir,outDir,transf_params,imgType):
    for roi in allRois:
        
        # Get roi path and roiID
        roi_vol = refDir + roi
        roiID = roi.split("-")[3].split(".")[0]
        
        roiDir = outDir + roiID + '/'
        try:
            os.mkdir(roiDir)
        except:
            pass         # Folder already exists
    
        # Transform reference roi with computed transform parameters
        transformixCall = 'transformix -out ' + tmpDir + ' -tp ' + transf_params + ' -in ' + roi_vol
        os.system(transformixCall)
    
        # Change name and path of transformed roi
        regRoi = tmpDir + 'result' + imgType
        regRoi_newID = roiDir + 'regROI-' + roiID + '_' + inputImgID + imgType
        os.rename(r'' + regRoi,r'' + regRoi_newID)
        
        #Compress mask
        os.system('gzip ' + regRoi_newID) 


if __name__ == "__main__":
    main(sys.argv[1:])

