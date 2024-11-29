import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Dataset Creation Tool",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 2.5rem !important;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(to right, #2980b9, #2c3e50);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stButton button {
        width: 100%;
        background-color: #27ae60;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #219a52;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .dataframe-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


# Main title with icon
st.markdown("# 🧬 Dataset Creation", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;'>
        Module to Create Dataset for Machine Learning Modelling
    </p>
    """, unsafe_allow_html=True)


# File Uploaders
st.markdown("""
    <h2 style='color: #2c3e50; margin-top: 2rem;'>
        📤 Upload Input Files
    </h2>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='upload-section'>
        <h4 style='color: #2c3e50;'>DEG Genes File</h4>
        """, unsafe_allow_html=True)
    deg_file = st.file_uploader("", type=['csv'], key="deg")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='upload-section'>
        <h4 style='color: #2c3e50;'>Combined Dataset</h4>
        """, unsafe_allow_html=True)
    dataset_file = st.file_uploader("", type=['csv'], key="dataset")
    st.markdown("</div>", unsafe_allow_html=True)


if deg_file and dataset_file:
    # Read Files
    ensembl_id = pd.read_csv(deg_file)
    dataset = pd.read_csv(dataset_file)

    # Get Ensembl IDs
    ensembl_ids = ensembl_id['Ensembl_ID']
    
    # Display First Few Ensembl IDs
    st.markdown("""
        <h2 style='color: #2c3e50; margin-top: 2rem;'>
            🧬 Gene File Ensembl IDs
        </h2>
        """, unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(ensembl_ids, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Filter Dataset
    regulated_genes = dataset[dataset['Ensembl_ID'].isin(ensembl_ids)]
    regulated_genes = regulated_genes.set_index('Ensembl_ID')

    # Display Filtered Genes
    st.markdown("""
        <h2 style='color: #2c3e50; margin-top: 2rem;'>
            📊 Created Counts Dataset
        </h2>
        """, unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(regulated_genes, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Save Option
    st.markdown("<div style='padding: 2rem 0;'>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Filtered Genes",
        data=regulated_genes.to_csv(index=True),
        file_name='Dataset.csv',
        mime='text/csv'
    )
    st.markdown("</div>", unsafe_allow_html=True)