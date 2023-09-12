import os
import logging
import pandas as pd
import radiomics

from collections import OrderedDict

from qa4iqi_extraction.constants import (
    ROI_NAMES,
    ROI_NAME_FIELD,
    DIAGNOSTICS_FEATURES_PREFIX,
    PARAMETER_FILE_NAME,
)

logger = logging.getLogger()


def extract_features(image_path, rois_paths, series_description):
    params_file_path = PARAMETER_FILE_NAME

    radiomics.logger.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())
    radiomics.setVerbosity(
        getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper())
    )

    extractor = radiomics.featureextractor.RadiomicsFeatureExtractor(params_file_path)

    all_features = []

    for roi_index, roi_path in enumerate(rois_paths):
        roi_features = extractor.execute(image_path, roi_path, label=1)

        # Filter out diagnostics features which are not wanted
        roi_features = OrderedDict(
            {
                k: v.item()
                for k, v in roi_features.items()
                if not k.startswith(DIAGNOSTICS_FEATURES_PREFIX)
            }
        )

        # Add ROI to the extracted features and move it to the start
        roi_features[ROI_NAME_FIELD] = ROI_NAMES[roi_index]
        roi_features.move_to_end(ROI_NAME_FIELD, False)

        all_features.append(roi_features)

    features_df = pd.DataFrame.from_records(all_features)

    return features_df
