import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc

# Page configuration
st.set_page_config(
    page_title="Gene ROC Analysis",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2E4053;
        font-size: 3rem !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding-bottom: 2rem;
    }
    .stHeader {
        color: #34495E;
        background-color: #F8F9F9;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton button {
        background-color: #2E86C1;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton button:hover {
        background-color: #21618C;
    }
    .upload-box {
        border: 2px dashed #BDC3C7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title with emoji
st.markdown("# 🧬 Gene ROC Analysis", unsafe_allow_html=True)

col1, col2 = st.columns(2)

st.header("Input Files")
with col1:
    st.markdown("""
        <div class='upload-box'>
        <h3>📤 Upload UpRegulated Dataset</h3>
        """, unsafe_allow_html=True)
    upregulated_file = st.file_uploader("", type=['csv', 'xlsx'])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='upload-box'>
        <h3>📤 Upload Combined Dataset</h3>
        """, unsafe_allow_html=True)
    combined_dataset_file = st.file_uploader("", type=['csv', 'xlsx'])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ROC Curve AUC Threshold
st.markdown("""
    <h3 style='color: #2E4053;'>🎯 AUC Threshold Selection</h3>
    """, unsafe_allow_html=True)
auc_threshold = st.slider("", min_value=0.5, max_value=1.0, value=0.9, step=0.05)

if upregulated_file and combined_dataset_file:
    # Load data
    data = pd.read_csv(upregulated_file)
    geneID = data.iloc[:,0]
    features_df = data.iloc[:,1:]
    data = data.set_index("Ensembl_ID")
    data = data.round().astype(int)
    data = data.T
    data['label'] = ['cancer' if '-01' in sample else 'normal' for sample in data.index]
    
    # Sample count information
    st.markdown("""
        <h2 style='color: #2E4053; padding: 1rem 0;'>
            📊 Sample Information
        </h2>
        """, unsafe_allow_html=True)
    class_counts = data['label'].value_counts()
    st.write(f"Total cancer samples: {class_counts['cancer']}")
    st.write(f"Total normal samples: {class_counts['normal']}")
    st.write(f"Total samples: {len(data)}")
    
    # Prepare data for ROC
    X = np.asarray(features_df.round().astype(int).T)
    y = np.asarray(data['label'])
    
    y_bin = label_binarize(y, classes=np.unique(y))
    
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(X.shape[1]):
        fpr[i], tpr[i], _ = roc_curve(y_bin.ravel(), X[:, i].ravel())
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # Create ROC DataFrame
    roc_df = pd.DataFrame({
        'Ensembl_ID': geneID,
        'ROC': [roc_auc[i] for i in range(len(geneID))]
    })
    
    # Plot ROC Curve
    st.markdown("""
        <h2 style='color: #2E4053; padding: 1rem 0;'>
            📈 ROC Curve
        </h2>
        """, unsafe_allow_html=True)
    plt.figure(figsize=(10, 8))
    
    high_auc_genes = []
    for i in range(len(geneID)):
        if roc_auc[i] > auc_threshold:
            plt.plot(fpr[i], tpr[i], lw=2, label=f'Gene {geneID[i]} (AUC = {roc_auc[i]:.4f})')
            high_auc_genes.append(geneID[i])
    
    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve for Genes with AUC > {auc_threshold}')
    plt.legend(loc="lower right")
    st.pyplot(plt)
    
    # Display high AUC genes
    st.markdown("""
        <h2 style='color: #2E4053; padding: 1rem 0;'>
            🎯 High AUC Genes
        </h2>
        """, unsafe_allow_html=True)
    st.write(f"Genes with AUC > {auc_threshold}:")
    st.write(high_auc_genes)
    
    # Filter Combined Dataset
    st.markdown("""
        <h2 style='color: #2E4053; padding: 1rem 0;'>
            📑 Filtered Dataset
        </h2>
        """, unsafe_allow_html=True)
    combined_dataset = pd.read_csv(combined_dataset_file)
    regulated_genes = combined_dataset[combined_dataset['Ensembl_ID'].isin(high_auc_genes)]
    st.dataframe(regulated_genes)

    # Download option
    @st.cache_data
    def convert_to_excel(df, file_path):
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='ROC_Results')
        return file_path

    # Save DataFrame to a temporary path
    file_path = convert_to_excel(regulated_genes, "ROC_Results.xlsx")

    st.download_button(
        label="Download ROC_Results as XLSX",
        data=open(file_path, "rb").read(),
        file_name="ROC_Results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )