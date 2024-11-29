import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Dataset Creation Tool",
    page_icon="🔬",
    layout="wide"
)


# Main title with icon
st.markdown("# 🧬 Dataset Creation", unsafe_allow_html=True)
st.markdown("""
    <p color: "white"; font-size: 5.2rem; margin-bottom: 2rem;'>
        Module to Create Dataset for Machine Learning Modelling
    </p>
    """, unsafe_allow_html=True)


# File Uploaders
st.markdown("""
    <h2 style='color: #57b1ff; margin-top: 2rem;'>
        📤 Upload Input Files
    </h2>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='upload-section'>
        <h4 style='color: #57b1ff;'>DEG Genes File</h4>
        """, unsafe_allow_html=True)
    deg_file = st.file_uploader("", type=['csv'], key="deg")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='upload-section'>
        <h4 style='color: #57b1ff;'>Combined Dataset</h4>
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
        <h2 style='color: #57b1ff; margin-top: 2rem;'>
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
        <h2 style='color: #57b1ff; margin-top: 2rem;'>
            📊 Created Counts Dataset
        </h2>
        """, unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(regulated_genes, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Save Option
    st.download_button(
        label="Download Filtered Genes",
        data=regulated_genes.to_csv(index=True),
        file_name='Dataset.csv',
        mime='text/csv'
    )