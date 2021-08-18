#!/usr/bin/env python
# coding: utf-8

import os
import fnmatch

# Feature modules
from feats_pyRadiomics import main as extractPyRadiomics

# Liver ROIs
# ROI-0, ROI-1: Normal liver tissue
# ROI-2, ROI-3: Benign cysts
# ROI-4: Hemangioma
# ROI-5: Liver metastasis
rois = ['LivROI-0','LivROI-1','LivROI-2','LivROI-3','LivROI-4','LivROI-5']

def main(ctDir,masksDir,outFeatsDir,featCateg):
    
    # Create outDir if it doesn't exist
    createOutDir(outFeatsDir)
    
    ctFiles = [f for f in os.listdir(ctDir) if fnmatch.fnmatch(f,'s-*.nii.gz' )] # Registered CT series
    
    for roiName in rois:
        masksRoiDir = masksDir + roiName[-1] + '/'
            
        if (featCateg=='pyRadiomics'):
            print('Extracting pyradiomics for ' + roiName)
            extractPyRadiomics(roiName,ctDir,ctFiles,masksRoiDir,outFeatsDir)
            
    
###################    
def createOutDir(outDir):
    
    # Create output folder for extracted features if it doesn't exist
    try:
        os.mkdir(outDir)
    except:
        if(os.path.exists(outDir)):
            pass
        else:
            print('outDir for extracted features could not be created!')
            sys.exit(1)  

if __name__ == "__main__":
    main(sys.argv[1:])