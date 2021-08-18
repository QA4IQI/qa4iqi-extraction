import os
import numpy as np

import SimpleITK as sitk

# pyRadiomics 
## Package
from radiomics import featureextractor

## Parameters
paramDir = '/home/jovyan/params/'
paramsFile = os.path.join(paramDir, 'QA4IQI_featParams.yaml')

def main(roiName,ctDir,ctFiles,masksRoiDir,outFeatsDir):
    
    # Set pyRadiomics parameters
    extractor = featureextractor.RadiomicsFeatureExtractor(paramsFile)

    # Compute all radiomics features
    ids = []
    feats = {}
    
    niigz = '.nii.gz'
    remove_nii = len(niigz)
    
    numCTs = len(ctFiles)
    
    for ctNum,ctFile in enumerate(ctFiles):
        
        ctPath = ctDir + ctFile
    
        ctId = ctFile[:-remove_nii]
        ids.append(ctId)
        
        print(str(ctNum + 1) + '/' + str(numCTs) + ': ' + ctId)
        
        refMaskPath = masksRoiDir + 'regROI-' + roiName[-1] + '_' + ctId + niigz
        
        ctVol = sitk.ReadImage(ctPath)
        refMask = sitk.ReadImage(refMaskPath)
    
        feats[ctNum] = extractor.execute (ctVol, refMask, label=1 )
        
    # A list of the valid features, sorted
    featureNames = list(sorted(filter ( lambda k: k.startswith("original_"), feats[0] )))
    
    # Convert to array
    feats_array = np.zeros((numCTs,len(featureNames)))
    
    for case_id in range(0,numCTs):
        a = np.array([])
        for feature_name in featureNames:
            a = np.append(a, feats[case_id][feature_name])
        feats_array[case_id,:] = a
            
    # May have NaNs
    feats_array = np.nan_to_num(feats_array)  
    
    # Use the right format
    dataSet = np.column_stack((np.array(ids),feats_array))
    
    # Save results
    np.savetxt(outFeatsDir + 'pyRadiomicsFeats_' + roiName + '.csv', dataSet, delimiter= ',', fmt='%s')
    
