import os
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_lottie import st_lottie

load_dotenv()
LOTTIE_PATH = os.environ["LOTTIE_PATH"]


def add_lottie(path: os.PathLike) -> None:
    with open(path, "r") as file:
        url = json.load(file)

    st_lottie(
        url,
        loop=True,
        quality="high",
        key="DNA",
        height=175,
        width=175
    )


def add_spacer(height=None) -> None:
    """
    Add white space between elements
    """
    if height:
        st.write(f'<div style="padding: {height}px;"></div>', unsafe_allow_html=True)
    else:
        st.write("###")


def dynamic_aggregation(
        aggregate_data: pd.DataFrame,
        mouse_tissue_atlas: pd.DataFrame,
        tissue_target: str
    ) -> pd.DataFrame:
    metrics_values = {
        "Metrics": [
            'Tissue Mean',
            'Tissue Max',
            'Tissue Min',
        ]
    }
    values = []

    # Tissue mean
    tissue_mean = aggregate_data.loc[
        aggregate_data["Tissue Type"] == tissue_target
    ]["Mean Protein Expression"]
    values.append(tissue_mean.values[0])
    # Tissue max
    values.append(mouse_tissue_atlas[tissue_target].max())
    # Tissue min
    values.append(mouse_tissue_atlas[tissue_target].min())

    metrics_values["Values"] = values

    return pd.DataFrame(metrics_values)
    

    


def generate_streamlit(
        mouse_tissue_atlas: pd.DataFrame, 
        aggregate_data: pd.DataFrame, 
        aggregate_data_display: pd.DataFrame, 
    ) -> None:
    """
    Streamlit and element formation
    """

    st.set_page_config(page_title="Mouse Tissue Atlas", page_icon=":mouse:")

    # Header
    st.subheader("Mouse Tissue Atlas")
    st.title("Analytics for various tissue expressions of M. musculus")
    st.write("Dataset found at [Graphia](https://graphia.app/example-data.html)")
    add_spacer(10)
    st.write("---")
    add_spacer(10)

    # Aggregate (Tissue means), Phylogenetic Age counts
    with st.container():
        col1, col2= st.columns(2)
        col1.write("Average measured expression per tissue")
        col1.dataframe(aggregate_data_display.style.highlight_max(axis=0))
        col2.write("Sample set phylogenetic ages")
        col2.dataframe(mouse_tissue_atlas['Phylogenetic Age'].value_counts())
        with col2:
            add_lottie(LOTTIE_PATH)
    add_spacer()

    # Tissue-specific aggregate selection
    st.subheader("Tissue-specific Expression Insights")
    tissues = mouse_tissue_atlas.columns[7:]
    tissue_target = st.selectbox("Select tissue type:", tissues)
    st.dataframe(dynamic_aggregation(
        aggregate_data,
        mouse_tissue_atlas,
        tissue_target,
    ))
    
    add_spacer(40)

    # Bar chart of maximums per tissue
    st.subheader("Maximum measured expression per tissue type")
    st.bar_chart(mouse_tissue_atlas.iloc[:, 7:].max(),use_container_width=True)
    add_spacer(30)

    # Raw dataframe
    st.subheader("Raw dataset")
    st.dataframe(mouse_tissue_atlas)
