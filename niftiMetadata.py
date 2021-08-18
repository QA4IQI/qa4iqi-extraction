#!/usr/bin/env python
# coding: utf-8

import sys,os
import pydicom
import fnmatch
import pandas

# Convert to nifti
import dicom2nifti

# Global variable
null = None

def main(inputDir,outDir):
    
    # Create outDir if it doesn't exist
    createOutDir(outDir)
    
    # 1. Loop through dicom directories
    # 2. Generate dicom volume in .nii format
    # 3. Store dicom metadata as .csv  
    allMeta_df = pandas.DataFrame({})
        
    dicomFolderDepth = 1
    dirCount = 0
    failed = 0
    
    for root,dirs,files in os.walk(inputDir):
        if root[len(inputDir):].count(os.sep) < dicomFolderDepth:
            for dicomId in dirs:  
                
                dirCount += 1
                dicomDir = os.path.join(root,dicomId)
                
                # Skip dose reports
                dicomIdSplit = dicomId.split('_')
                if len(dicomIdSplit)==3:
                    
                    # Get series date to create dicomId
                    try:
                        dicomMeta,studyId,scannerCode = generateStudyId(dicomId,dicomDir)
                        print(str(dirCount) + '/' + str(len(dirs)) + ' ' + dicomId + ' ' + studyId)
                    
                        try:
                            convertToNifti(dicomDir,outDir,studyId)                    
                            allMeta_df = extractStoreDicomMeta(allMeta_df,dicomMeta,dicomId,studyId,scannerCode)
                        except:
                            print('Failed conversion...')
                            failed += 1
                    except:
                        print(str(dirCount) + '/' + str(len(dirs)) + ' ' + dicomId + ' folder with no Dicom file')
    
    print('Failed: ' + str(failed))
    
    # saving the dataframe 
    allMeta_df.to_csv(outDir + 'metadata.csv')

###################    
def createOutDir(outDir):
    
    # Create output folder if it doesn't exist
    try:
        os.mkdir(outDir)
    except:
        
        if(os.path.exists(outDir)):
            pass
        else:
            print('OutDir could not be created!')
            sys.exit(1)

######################
def generateStudyId(dicomId,dicomDir): 
    # Get series date for studyId
    ## Take first dicom file as sample 
    dicomFiles = os.listdir(dicomDir)
            
    ## Get series description from metadata
    dicomMeta = pydicom.dcmread(dicomDir + '/' + dicomFiles[0])
            
    ## Series Date
    serInstitution = dicomMeta.get('InstitutionName',null)
    # >> Pseudonymized... serDevice = dicomMeta.get('DeviceSerialNumber',null)
    
    serModelRaw = dicomMeta.get('ManufacturerModelName',null)
    serModelSplit = serModelRaw.split()
    serModel = ''
    
    for word in serModelSplit:
        serModel = serModel + word
    
    studyId = 's-' + str(serInstitution) + '_' + str(serModel) + '_'  + dicomId
    
    scannerCode = str(serInstitution) + '_' + str(serModel)
    
    return dicomMeta, studyId, scannerCode

########################
def convertToNifti(dicomDir,outDir,studyId):
    
    dicom2nifti.convert_directory(dicomDir,outDir,compression=False,reorient=False)
    
    niftiFiles = [f for f in os.listdir(outDir) if fnmatch.fnmatch(f,'*.nii')] # Get only nifti files
    outIdCT = [f for f in niftiFiles if fnmatch.fnmatch(f,'[!s-]*.nii')] # Exclude pre-computed series
         
    # Identify output file with correct naming
    correctOutNiftiName = outDir + studyId + '.nii'
    os.rename(outDir + outIdCT[0], correctOutNiftiName) 
    
########################
def extractStoreDicomMeta(allMeta_df,dicomMeta,dicomId,studyId,scannerCode):
    # Create dataframe from dicom metadata
    dataRow = {}
    
    dTags_simple = ['InstitutionName','DeviceSerialNumber',
                    'Manufacturer','ManufacturerModelName',
                    'SeriesDate','SeriesDescription','AcquisitionNumber','SeriesNumber','PatientPosition',
                    'SliceThickness','CTDIvol','ExposureModulationType','KVP','ReconstructionDiameter',
                    'FilterType','SpiralPitchFactor']
    
    dTags_double = ['PixelSpacing','ConvolutionKernel']
    
    dataRow['StudyId'] = studyId
    dataRow['ScannerCode'] = scannerCode
    dataRow['DicomId'] = dicomId
         
    ## Simple dicom tags
    for tag_s in dTags_simple:
        tagS_sample = dicomMeta.get(tag_s,null)
        dataRow[tag_s] = tagS_sample
                        
    ## Double dicom tags
    for tag_d in dTags_double:
        tagD_sample = dicomMeta.get(tag_d,null)
        dataRow[tag_d + '_0'] = tagD_sample[0]
        
        try:
            dataRow[tag_d + '_1'] = tagD_sample[1]
        except:
            dataRow[tag_d + '_1'] = null
                    
    allMeta_df = allMeta_df.append(dataRow, ignore_index=True)
        
    return allMeta_df
        
if __name__ == "__main__":
    main(sys.argv[1:])
    
    