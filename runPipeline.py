import sys,os


dockerCodeRoot = '/home/jovyan/'
dockerQA4IQIroot = '/home/jovyan/qa4iqi/'
dockerNewDataRoot = '/home/jovyan/data/newData/'

sys.path.append(dockerCodeRoot)
from niftiMetadata import main as getNiftiMetadata
from regRefToCT import main as regRefToCT # Register reference data to CT
from extractFeats import main as extractFeats

def main():  
 
    featCateg = 'pyRadiomics'

    # Dicom to nifti transformation + metadata extraction
    inputDir = dockerNewDataRoot
    outNiftiDir = '/home/jovyan/nii/'
    os.makedirs(outNiftiDir)
    
    getNiftiMetadata(inputDir,outNiftiDir)
    
    # Volume registration
    outMasksDir = '/home/jovyan/RegisteredMasks/' 
    os.makedirs(outMasksDir)
    
    regRefToCT(outNiftiDir,outMasksDir) 
    
    # Extract features
    outFeatsDir = dockerQA4IQIroot + 'out_radiomics/'
    os.makedirs(outFeatsDir)

    extractFeats(outNiftiDir,outMasksDir,outFeatsDir,featCateg)


if __name__ == "__main__":
    main()