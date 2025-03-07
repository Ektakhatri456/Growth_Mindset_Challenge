#Project-1: Growth Mindset Challenge.

import streamlit as st # type: ignore
import pandas as pd # type: ignore
import os
from io import BytesIO

#Building profile:
st.sidebar.image("https://avatars.githubusercontent.com/u/170619187?s=400&u=f758c87ccd8a92db5993514049855df20f7d80aa&v=4", width=100)
st.sidebar.markdown("### Ekta Khatri")
st.sidebar.markdown("💼 **Developer**")
st.sidebar.markdown("[🔗 Streamlit] (https://share.streamlit.io/user/ektakhatri456)")
st.sidebar.markdown("[🔗 LinkedIn] (https://www.linkedin.com/in/ekta-khatri-7b6b4a1a8/)")


#setup our app:

st.set_page_config(page_title="💿Data sweeper", layout='wide')
st.title("💿Data sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

#uploading files in streamlit:

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
# Corrected the typo here:

        file_ext = os.path.splitext(file.name)[-1].lower()

# Check file type and read accordingly:

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else: 
            st.error(f"Unsupported file type: {file_ext}")
            continue

# Display file details

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB") #It will display detail about each file within the loop:

# Show 5 rows of the data frame

        st.write("🔍Preview the Head of the Dataframe")
        st.dataframe(df.head())

# Data Cleaning Options:

        st.subheader("🛠Data Cleaning Options")
        if st.checkbox(f"File Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())  # Fillna ---> for filling missing values
                    st.write("Missing Values have been filled!")

#Selecting columns to convert:

        st.subheader("🎯Select columns to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", list(df.columns), default=list(df.columns))

        df = df[columns]

#Creating some Visualizations:

        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:,:2])    # ':'---> from start , ':2'----> till the end

#Converting the file (CSV to Excel):
        st.subheader("🔄Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV", "Excel"],key=file.name)  #st.radio() --> a button to select one option from a list of options
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "text/xlsx"
            buffer.seek(0)

# Creating Download button:

            st.download_button(
                label="⬇ Download {file.name} as {conversion_type}}",
                data = buffer,
                file_name = file_name,
                mime = mime_type
                )

st.success("🎉 All files processed!")
