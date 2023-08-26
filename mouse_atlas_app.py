import re
import os
import pandas as pd
from typing import List, Tuple
from dotenv import load_dotenv
from database_helpers import validate_pgql
from streamlit_helper import generate_streamlit

load_dotenv()
DATA_FILE = os.environ["DATA_FILE"]
cwd = os.path.abspath(os.path.dirname('__file__'))
data_path = os.path.abspath(os.path.join(cwd, DATA_FILE))


def extract_and_aggregate(
        data_path: os.PathLike
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Extract raw atlas data, produces aggregate data
    """

    mouse_tissue_atlas = pd.read_csv(data_path)
    aggregate_data = pd.DataFrame(
        {
            'Tissue Type': mouse_tissue_atlas.columns[7:], 
            'Mean Protein Expression': mouse_tissue_atlas.iloc[:,7:].mean().tolist()
        }
    )
    aggregate_data_displayable = aggregate_data.copy()
    aggregate_data_displayable.set_index("Tissue Type", inplace=True)

    return (
        mouse_tissue_atlas,
        aggregate_data,
        aggregate_data_displayable,
    )


def extract_clean_columns(mouse_tissue_atlas: pd.DataFrame) -> List[str]:
    """
    Extract and clean column names from provided data file
    """

    raw_columns = mouse_tissue_atlas.columns.to_list()
    mouse_tissue_atlas_cols = [
            re.sub('[^a-zA-Z\d_]', '', x.replace(' ', '_')) for x in raw_columns
        ]
    
    return mouse_tissue_atlas_cols


# Extract and aggregate CSV data
mouse_tissue_atlas, aggregate_data, aggregate_data_displayable = extract_and_aggregate(
    data_path
)
# Fetches and return all data from aggregate table for validation
result = validate_pgql()

# Deploy streamlit
generate_streamlit(
    mouse_tissue_atlas, 
    aggregate_data, 
    aggregate_data_displayable
    )
