import streamlit as st
import pandas as pd
import os

def seperateByRace(file, target, name, race):
    """Separates Data by Race"""
    racer = file[file["race.demographic"].str.contains(race, case=False, na=False)]
    output_file_path = os.path.join(target, f"{name}.csv")
    racer.to_csv(output_file_path, index=False)
    return output_file_path

def matchingDNA(race, counts, target, name):
    """Matches Sample ID from phenotypes to counts"""
    phenotypeData = pd.read_csv(race)
    colA1 = phenotypeData.iloc[:, 0]
    newFile = counts[['Ensembl_ID'] + [col for col in colA1 if col in counts.columns[1:]]]
    output_file_path = os.path.join(target, f"{name}.csv")
    newFile.to_csv(output_file_path, index=False)
    return output_file_path

# Streamlit App Configuration
st.set_page_config(
    page_title="Race-Based Dataset Segregation",
    page_icon=":dna:",
    layout="wide"
)

# Advanced Custom CSS for modern, dark-themed design
st.markdown("""
    <style>
    /* Global Background and Text */
    .reportview-container {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #bb86fc;
        color: #000;
        font-weight: bold;
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3700b3;
        color: #ffffff;
        transform: scale(1.05);
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #bb86fc;
        font-family: 'Roboto', sans-serif;
    }
    
    /* File Uploader Styling */
    .stFileUploader {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Container Styling */
    .stContainer {
        background-color: #1e1e1e;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Success and Error Message Styling */
    .stSuccess {
        background-color: #03dac6;
        color: #000;
        border-radius: 10px;
    }
    .stError {
        background-color: #cf6679;
        color: #ffffff;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# App Title with Subheader
st.title("🧬 Dataset Segregation by Race")
st.subheader("Separate and Match Genetic Data Across Racial Demographics")

# Create two columns for file uploaders
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Phenotype File")
    phenotype_file = st.file_uploader("Upload Phenotype CSV", type=["csv"], key="phenotype")

with col2:
    st.markdown("### 📊 Counts File")
    counts_file = st.file_uploader("Upload Counts CSV", type=["csv"], key="counts")

if phenotype_file and counts_file:
    # Race Selection with Info
    st.markdown("### 🌍 Race Selection")
    st.info("Choose one or more racial demographics to process")

    # Improved Race Selection
    races = ['white', 'black or african american', 'not reported', 'asian', 'american indian or alaska native']
    selected_races = st.multiselect(
        "Select Races to Separate", 
        races, 
        help="Select the racial demographics you want to segregate and analyze"
    )

    if selected_races:
        try:
            # Existing processing logic remains the same
            os.makedirs("temp", exist_ok=True)
            phenotype_path = os.path.join("temp", phenotype_file.name)
            counts_path = os.path.join("temp", counts_file.name)

            with open(phenotype_path, "wb") as f:
                f.write(phenotype_file.read())  
            with open(counts_path, "wb") as f:
                f.write(counts_file.read())

            phenotype_data = pd.read_csv(phenotype_path)
            counts_data = pd.read_csv(counts_path)

            os.makedirs("temp", exist_ok=True)

            # Create a container to display processing results
            results_container = st.container()

            with results_container:
                st.markdown("### 🔍 Processing Results")
                for race in selected_races:
                    # Existing race processing logic
                    race_file_path = seperateByRace(phenotype_data, "temp", race, race)
                    output_file_path = matchingDNA(race_file_path, counts_data, "temp", f"matched_{race}")
                    
                    # Improved result display
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.success(f"Processed Race: {race}")
                    with col2:
                        with open(output_file_path, "rb") as file:
                            st.download_button(
                                label="Download", 
                                data=file, 
                                file_name=f"matched_{race}.csv", 
                                mime="text/csv",
                                key=f"download_{race}"
                            )

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload both files and select at least one race.")