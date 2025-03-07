import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import time
import io
import os
import sys
import subprocess
import sys 
import calendar
import json
from io import BytesIO
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from openpyxl import Workbook
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="Datapoem.Datateam",
    page_icon="https://green.datapoem.ai/img/datapoem-logo-white.d3e98fcd.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define custom CSS for the option menu and background image
custom_css = f"""
<style>
/* Set the background image */
body {{
    background-image: url('https://datapoem.ai/img/gradient-color-bg.e99d22ef.svg');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Increase the font size and padding of the option menu items */
.css-qrbaxs a {{
    font-size: 20px !important;
    padding: 10px 20px !important;
}}
</style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)


# Create a container for the title and the menu
with st.container():
    selected = option_menu(
        menu_title="",
        options=["Home", "Paid Media", "Non Paid Media", "Competition","Nielsen", "Playground", "QC", 'Setting', "More Feature"],
        icons=["house", "file-ppt", "journals",'journal-richtext' ,"database-fill-exclamation", "graph-up-arrow", "search", "gear", "filter"],  # Provide an empty string for each option if no icons are used
        menu_icon="cast",
        default_index=0,  # Corrected to an integer
        orientation="horizontal",
    )
def login(username, password):
    # This function should be defined to handle login logic
    # For demonstration purposes, let's assume it always returns True
    return True
st.divider()
# Display content based on the selected option
if selected == "Home":
    st.write("Home")
    #if selected == "Home":
        # # Add login form
        # st.subheader("Login")
        # username = st.text_input("Username")
        # password = st.text_input("Password", type="password")
        
        # if st.button("Login"):
        #     if login(username, password):
        #         st.success("Login successful!")
        #         # Place additional code here for what happens after successful login
        #     else:
        #         st.error("Login failed. Please check your username and password.")    
elif selected == "Paid Media":
        # Function to initialize session state
    def initialize_session_state():
        if 'modified_files' not in st.session_state:
            st.session_state.modified_files = {}
            

    # Function to download Excel file
    def download_xlsx(df, label, filename):
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Function to download Excel file
    def download_csv(df, label, filename):
        csv_file = io.BytesIO()
        df.to_excel(csv_file, index=False)
        csv_file.seek(0)
        st.download_button(label=label, data=csv_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Initialize session state
    initialize_session_state()

    with st.sidebar:
        selected = option_menu("Main Menu", ['Data Filtering','Data Cleaning','Null Value Check','Summary','Datapoem Format'],#'Data Quality Check'], 
            icons=['filter','link', 'file-text', 'lightning','rocket','shield'], menu_icon="cast", default_index=0)
    
    #1. Data Filtering:    


# Check if Data Filtering is selected
    if selected == "Data Filtering":
        st.subheader("Data Filtering")

        # Upload CSV file
        uploaded_file = st.file_uploader("Upload your CSV file to prepare the Raw Data for Summary:", type=["csv"], accept_multiple_files=False)

        # Check if a file is uploaded
        if uploaded_file is not None:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)

            # Data processing
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce').dt.strftime('%Y-%m-%d')
                df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')

            columns_to_replace = ['Impressions', 'Clicks', 'Media_Cost', 'Video_Views', 'GRPs']
            df[columns_to_replace] = df[columns_to_replace].fillna(0).replace('', 0)

            # Define filtering conditions
            filter_conditions = {
                'PW_Beloved': (df['Brand'] == 'Beloved'),
                'Axe_Cross': (df['Brand'] == 'Axe') & (df['Category'] == 'Cross-category'),
                'Degree_Cross': (df['Brand'] == 'Degree') & (df['Category'] == 'Cross-category'),
                'DMC_Cross_MB': (df['Brand'] == 'Dove Men+Care') & df['Category'].isin(["Cross-category","Masterbrand"]),
                'Dove_Cross': (df['Brand'] == 'Dove') & (df['Category'] == 'Cross-category'),
                'Dove_MB_Superbowl': (df['Brand'] == 'Dove'),
                'Degree_Deo': df['Brand'].isin(['Degree', 'Degree Men', 'Degree Women']) & df['Category'].isin(['Deodorants', 'Personal Wash']),
                'Axe_Deo': (df['Brand'] == 'Axe') & df['Category'].isin(['Deodorants', 'Hair Care', 'Personal Wash']),
                'DMC_Deo': (df['Brand'] == 'Dove Men+Care') & (df['Category'] == 'Deodorants'),
                'DMC_PW': (df['Brand'] == 'Dove Men+Care') & (df['Category'] == 'Personal Wash'),
                'Dove_Deo': (df['Brand'] == 'Dove') & (df['Category'] == 'Deodorants'),
                'Dove_PW': (df['Brand'] == 'Dove') & (df['Category'] == 'Personal Wash'),
                'Scale': (df['Brand'] == 'Scale')
            }

            # Process and generate individual download buttons
            for key, condition in filter_conditions.items():
                filtered_df = df[condition]

                if not filtered_df.empty:
                    st.write(f"### {key} Paid Media Raw Data")
                    
                    towrite = io.BytesIO()
                    with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
                        filtered_df.to_excel(writer, sheet_name=key, index=False)
                    towrite.seek(0)

                    # Download button for each dataset
                    st.download_button(
                        label=f"Download {key} Paid Media Raw Data",
                        data=towrite,
                        file_name=f"{key} Paid Media Raw Data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    if selected == 'Data Cleaning':
        st.subheader("Data Cleaning Process")
        uploaded_files = st.file_uploader("Upload your excel file(s) for data cleaning process", type=["xlsx"], accept_multiple_files=True)

        # Check if files are uploaded
        if uploaded_files:
            # Loop through uploaded files
            for file in uploaded_files:
                # Read Excel file into a DataFrame
                df = pd.read_excel(file)
                # 1. Date Formatting
                #if 'Date' in df.columns:
                    #df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
                # 2. Remove empty rows
                df = df.dropna(how='all')
                # # 3. Remove empty columns
                # df = df.dropna(axis=1, how='all')
                # 4. Duplicate or Non-Duplicate Entry in Rows
                # columns_list = df.columns.difference(['index']).tolist()
                # df["IsDuplicate"] = df.duplicated(subset=columns_list, keep=False)
                # df['Duplicate/Non Duplicate'] = df['IsDuplicate'].map({True: "Duplicate", False: "Non Duplicate"})
                # 5. Convert Text format to numeric format
                if 'Impressions' in df.columns:
                    df['Impressions'] = pd.to_numeric(df['Impressions'])
                if 'GRPs' in df.columns:
                    df['GRPs'] = pd.to_numeric(df['GRPs'])
                if 'Media_Cost' in df.columns:
                    df['Media_Cost'] = pd.to_numeric(df['Media_Cost'])
                # 6. Blank metrics to Zero
                columns_to_replace = ['Impressions', 'Media_Cost', 'GRPs']
                df[columns_to_replace] = df[columns_to_replace].fillna(0).replace('', 0)
                #7. Metrics Check:
                df['Metrics_Check'] = np.where(df['Impressions'] < df['Media_Cost'], "True", "False")
                #8. Negative Metrics Check:
                columns_to_check = ['Impressions', 'Clicks', 'Media_Cost', 'Video_Views', 'GRPs']
                # Function to determine if any of the specified columns have negative values
                def check_negative_values(row):
                    negative_columns = [col for col in columns_to_check if row[col] < 0]
                    return ', '.join(negative_columns) if negative_columns else 'No Negative Values'
                # Create a new column with the results
                df['Negative Check'] = df.apply(check_negative_values, axis=1)

                #Drop the columns and rename
                df = df.drop(columns=["MSID", "Load_Date", "File_Name"], errors='ignore')   
                df = df.rename(columns={"Driver_Type": "Media Type"})

                # Store the modified DataFrame in the session state
                st.session_state.modified_files[file.name] = df
                def download_xlsx(df, label, filename):
                    if 'Raw' in filename:
                        filename = filename.replace('Raw', 'Processed')
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)  
                    st.download_button(label=label, 
                                       data=excel_file, 
                                       file_name=filename, 
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                       key=f"download_button_{filename}_{label}"
                                       )
                # Display download button for the modified file
                download_xlsx(df, label=f'Download Modified File ({file.name})', filename=file.name)
                
            
        #2. Null Value Check Process:    
    if selected == 'Null Value Check':
            st.subheader("Null Values Checking Process")
            uploaded_files = st.file_uploader("Upload your excel file for null values checking process", type=["xlsx"], accept_multiple_files=True)
            if uploaded_files:
                dfs_to_save = []
                for file in uploaded_files:
                    df = pd.read_excel(file)
                    df['Month'] = df['Date'].apply(lambda x: x.month)
                    df['Year'] = df['Date'].apply(lambda x: x.year)
                        
                    null_cost = df
                    null_imp = df 
                    digtal_cost = null_cost[(null_cost['Master_Channel'] =='Digital') | (null_cost['Master_Channel'] =='Commerce & Search')]
                    tv_cost = null_cost[(null_cost['Master_Channel'] =='TV') | (null_cost['Master_Channel'] =='Radio') | (null_cost['Master_Channel'] =='Print')| (null_cost['Master_Channel'] =='Cinema') | (null_cost['Master_Channel'] =='OOH') | (null_cost['Master_Channel'] =='DOOH')]
                    digtal_imp = null_imp[(null_imp['Master_Channel'] =='Digital') | (null_imp['Master_Channel'] =='Commerce & Search')]
                    tv_grp = null_imp[(null_imp['Master_Channel'] =='TV') | (null_imp['Master_Channel'] =='Radio') | (null_imp['Master_Channel'] =='Print') | (null_imp['Master_Channel'] =='Cinema') | (null_imp['Master_Channel'] =='OOH') | (null_imp['Master_Channel'] =='DOOH') ]
                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Package_Placement_Name']
                    digtal_cost.groupby(col)["Impressions"].sum()
                    
                    
                    #1. Null Media_Cost - Digital,Commerce & Search

                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Package_Placement_Name']
                    digtal_cost_group = digtal_cost.groupby(col)[['Impressions', 'Media_Cost']].sum()
                    digtal_cost_group = digtal_cost_group[digtal_cost_group['Impressions']>10000]
                    digtal_cost_group = digtal_cost_group[digtal_cost_group['Media_Cost']== 0]
                    dfs_to_save.append((digtal_cost.reset_index(), 'Digital Cost Raw'))
                    dfs_to_save.append((digtal_cost_group.reset_index(), 'Digital Cost Summary'))

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = digtal_cost_group
                    # Function to download Excel file
                    def download_xlsx_2(df, label, filename):
                    # Create a BytesIO object to store the Excel file
                        excel_file = io.BytesIO()
                    # Write the DataFrame to the BytesIO object
                        df.to_excel(excel_file, index=False)
                    # Set the cursor to the beginning of the BytesIO object
                        excel_file.seek(0)
                    # Set up download button
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    # Display download button for the modified file
                    download_xlsx_2(digtal_cost_group.reset_index(), label=f'Digtal Cost Null Summary File ({file.name})', filename='Digtal Cost Null Summary File.xlsx')
                    digtal_cost['tuple'] = digtal_cost[col].apply(lambda x: tuple(x),axis=1)
                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = digtal_cost
                    # Display download button for the modified file with unique key
                    download_xlsx_2(digtal_cost[digtal_cost['tuple'].isin(digtal_cost_group.index)], label=f'Digtal Cost Null Raw File ({file.name})', filename='Digtal Cost Null Raw File.xlsx')

                    #2. Null Impressions - Digital,Commerce & Search

                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Package_Placement_Name']
                    digtal_imp_group = digtal_imp.groupby(col)[['Impressions', 'Media_Cost']].sum()
                    digtal_imp_group = digtal_imp_group[digtal_imp_group['Media_Cost']>1000]
                    digtal_imp_group = digtal_imp_group[digtal_imp_group['Impressions']==0]
                    dfs_to_save.append((digtal_imp.reset_index(), 'Digital Imp Raw'))
                    dfs_to_save.append((digtal_imp_group.reset_index(), 'Digital Imp Summary'))

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = digtal_imp_group
                    # Function to download Excel file
                    def download_xlsx_2(df, label, filename):
                    # Create a BytesIO object to store the Excel file
                        excel_file = io.BytesIO()
                    # Write the DataFrame to the BytesIO object
                        df.to_excel(excel_file, index=False)
                    # Set the cursor to the beginning of the BytesIO object
                        excel_file.seek(0)
                    # Set up download button
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    # Display download button for the modified file
                    download_xlsx_2(digtal_imp_group.reset_index(), label=f'Digtal Imp Null Summary File ({file.name})', filename='Digtal Imp Null Summary File.xlsx')
                    digtal_imp['tuple'] = digtal_imp[col].apply(lambda x: tuple(x),axis=1)
                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = digtal_imp
                    # Display download button for the modified file with unique key
                    download_xlsx_2(digtal_imp[digtal_imp['tuple'].isin(digtal_imp_group.index)], label=f'Digtal Imp Null Raw File ({file.name})', filename='Digtal Imp Null Raw File.xlsx')
                    
                    #3. Null GRPs - TV
                    
                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Daypart']
                    tv_grp_group = tv_grp.groupby(col)[['GRPs', 'Media_Cost']].sum()
                    tv_grp_group = tv_grp_group[tv_grp_group['Media_Cost']>50000]
                    tv_grp_group = tv_grp_group[tv_grp_group['GRPs']==0]
                    dfs_to_save.append((tv_grp.reset_index(), 'TV GRP Raw'))
                    dfs_to_save.append((tv_grp_group.reset_index(), 'TV GRP Summary'))

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = tv_grp_group
                    # Function to download Excel file
                    def download_xlsx_2(df, label, filename):
                    # Create a BytesIO object to store the Excel file
                        excel_file = io.BytesIO()
                    # Write the DataFrame to the BytesIO object
                        df.to_excel(excel_file, index=False)
                    # Set the cursor to the beginning of the BytesIO object
                        excel_file.seek(0)
                    # Set up download button
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    # Display download button for the modified file
                    download_xlsx_2(tv_grp_group.reset_index(), label=f'TV Null GRPs Summary File ({file.name})', filename='TV Null GRPs Summary File.xlsx')
                    tv_grp['tuple'] = tv_grp[col].apply(lambda x: tuple(x),axis=1)
                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = tv_grp
                    # Display download button for the modified file with unique key
                    download_xlsx_2(tv_grp[tv_grp['tuple'].isin(tv_grp_group.index)], label=f'TV Null GRPs Raw File ({file.name})', filename='TV Null GRPs Raw File.xlsx')
                    
                    #4. Null Media_Cost - TV

                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Daypart']
                    tv_cost_group = tv_cost.groupby(col)[['GRPs', 'Media_Cost']].sum()
                    tv_cost_group = tv_cost_group[tv_cost_group['GRPs']>1]
                    tv_cost_group = tv_cost_group[tv_cost_group['Media_Cost']== 0]
                    dfs_to_save.append((tv_cost.reset_index(), 'TV Cost Raw'))
                    dfs_to_save.append((tv_cost_group.reset_index(), 'TV Cost Summary'))

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = tv_cost_group
                    # Function to download Excel file
                    def download_xlsx_2(df, label, filename):
                    # Create a BytesIO object to store the Excel file
                        excel_file = io.BytesIO()
                    # Write the DataFrame to the BytesIO object
                        df.to_excel(excel_file, index=False)
                    # Set the cursor to the beginning of the BytesIO object
                        excel_file.seek(0)
                    # Set up download button
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    # Display download button for the modified file
                    download_xlsx_2(tv_cost_group.reset_index(), label=f'TV Null Cost Summary File ({file.name})', filename='TV Null Cost Summary File.xlsx')
                    tv_cost['tuple'] = tv_cost[col].apply(lambda x: tuple(x),axis=1)
                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = tv_cost
                    # Display download button for the modified file with unique key
                    download_xlsx_2(tv_cost[tv_cost['tuple'].isin(tv_cost_group.index)], label=f'TV Null Cost Raw File ({file.name})', filename='TV Null Cost Raw File.xlsx')
                            # Create an in-memory bytes buffer to hold the Excel file content
                    output = io.BytesIO()
                    
                    # # Create a Pandas Excel writer using XlsxWriter engine
                    # with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    #     # Write each DataFrame to a separate sheet in the Excel file
                    #     for df, label in dfs_to_save:
                    #         df.to_excel(writer, sheet_name=label, index=False)
                    
                    # # Set the cursor to the beginning of the BytesIO object
                    # output.seek(0)
                    
                    # # Display download button for the Excel file
                    # st.download_button(label='Download Excel File', data=output.getvalue(), file_name='null_value_check_results.xlsx', mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")





                    break
     
        # Check if "Summary" is selected
    if selected == 'Summary':
            st.subheader("Summary Preparation Process")
            option = st.selectbox(
                "Select the brand to prepare the summary",
                ("Dove PW", "Dove Deo", "DMC PW", "DMC Deo", "Degree Deo", "Axe Deo", "Dove MB + Superbowl", "Dove Cross", "Degree Cross Category", "Axe Cross Category","DMC Cross Category")
            )
            st.write("selected:", option)
            
            # Set the size of the dropdown menu
            st.markdown(
                "<style>.css-1a7xih0{font-size: small !important;}</style>", 
                unsafe_allow_html=True
            )
        #Axe Cross Cateogry Summary:
            if option == 'Axe Cross Category':
            # Function to download Excel file
                def download_xlsx(df, label, filename):
                        excel_file = io.BytesIO()
                        df.to_excel(excel_file, index=False)
                        excel_file.seek(0)
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)    
                if uploaded_files:
                        for file in uploaded_files:
                            Axe_Cross = pd.read_excel(file)
                            Axe_Cross['Date'] = pd.to_datetime(Axe_Cross['Date'])
                            Axe_Cross = Axe_Cross.fillna(0)
                            numeric_columns = ['Impressions', 'Clicks', 'Media_Cost', 'Video_Views']
                            Axe_Cross[numeric_columns] = Axe_Cross[numeric_columns].apply(pd.to_numeric, errors='coerce')
                            Axe_Cross_pivot_table = Axe_Cross.pivot_table(
                                values=['Impressions', 'Clicks', 'Media_Cost'], 
                                index=[Axe_Cross['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'],
                                aggfunc='sum').reset_index()
                            columns_to_clean = [
                                'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 
                                'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'
                            ]
                            Axe_Cross_pivot_table[columns_to_clean] = Axe_Cross_pivot_table[columns_to_clean].replace(0, "")
                            #download_xlsx(Axe_Cross, label='Download Modified File (Mapped)', filename="Axe Cross Category Mapped Raw.xlsx")
                            today_date = datetime.today().strftime('%Y-%m-%d')
                            # Create the dynamic filename
                            filename = f"Axe Cross Category Summary {today_date}.xlsx"
                            download_xlsx(Axe_Cross_pivot_table, label='Download the Axe Cross Category Summary File', filename=filename)

        #Degree Cross Cateogry Summary:
            if option == 'Degree Cross Category':
            # Function to download Excel file
                def download_xlsx(df, label, filename):
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                if uploaded_files:    
                        for file in uploaded_files:
                            Degree_Cross = pd.read_excel(file)
                            Degree_Cross['Date'] = pd.to_datetime(Degree_Cross['Date'])
                            Degree_Cross = Degree_Cross.fillna(0)
                            numeric_columns = ['Impressions', 'Clicks', 'Media_Cost']
                            Degree_Cross[numeric_columns] = Degree_Cross[numeric_columns].apply(pd.to_numeric, errors='coerce')
                            Degree_Cross_pivot_table = Degree_Cross.pivot_table(
                                values=['Impressions', 'Clicks', 'Media_Cost'], 
                                index=[Degree_Cross['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'],
                                aggfunc='sum').reset_index()
                            
                            columns_to_clean = [
                                'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 
                                'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'
                            ]
                            Degree_Cross_pivot_table[columns_to_clean] = Degree_Cross_pivot_table[columns_to_clean].replace(0, "")
                            
                            today_date = datetime.today().strftime('%Y-%m-%d')
                            # Create the dynamic filename
                            filename = f"Degree Cross Category Summary {today_date}.xlsx"
                            download_xlsx(Degree_Cross_pivot_table, label='Download the Degree Cross Category Summary File', filename=filename)  

            #DMC Cross Cateogry Summary:
            if option == 'DMC Cross Category':
            # Function to download Excel file
                def download_xlsx(df, label, filename):
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                if uploaded_files:
                    
                        for file in uploaded_files:
                            DMC_Cross = pd.read_excel(file)
                            DMC_Cross['Date'] = pd.to_datetime(DMC_Cross['Date'])
                            DMC_Cross = DMC_Cross.fillna(0)
                            numeric_columns = ['Impressions', 'Clicks', 'Media_Cost']
                            DMC_Cross[numeric_columns] = DMC_Cross[numeric_columns].apply(pd.to_numeric, errors='coerce')
                            DMC_Cross_pivot_table = DMC_Cross.pivot_table(
                                values=['Impressions', 'Clicks', 'Media_Cost'], 
                                index=[DMC_Cross['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'],
                                aggfunc='sum').reset_index()
                            columns_to_clean = [
                                'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 
                                'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'
                            ]
                            DMC_Cross_pivot_table[columns_to_clean] = DMC_Cross_pivot_table[columns_to_clean].replace(0, "")
                            today_date = datetime.today().strftime('%Y-%m-%d')
                            # Create the dynamic filename
                            filename = f"DMC Cross Category Summary {today_date}.xlsx"
                            download_xlsx(DMC_Cross_pivot_table, label='Download the DMC Cross Category Summary File', filename=filename) 
                            
            #Dove Cross Cateogry Summary:
            if option == 'Dove Cross':
            # Function to download Excel file
                def download_xlsx(df, label, filename):
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                if uploaded_files:
                    
                        for file in uploaded_files:
                            Dove_Cross = pd.read_excel(file)
                            Dove_Cross['Date'] = pd.to_datetime(Dove_Cross['Date'])
                            Dove_Cross = Dove_Cross.fillna(0)
                            numeric_columns = ['Impressions', 'Clicks', 'Media_Cost']
                            Dove_Cross[numeric_columns] = Dove_Cross[numeric_columns].apply(pd.to_numeric, errors='coerce')
                            Dove_Cross_pivot_table = Dove_Cross.pivot_table(
                                values=['Impressions', 'Clicks', 'Media_Cost'], 
                                index=[Dove_Cross['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'],
                                aggfunc='sum').reset_index()
                            #download_xlsx(DMC_Cross, label='Download Modified File (Mapped)', filename="DMC Cross Category Mapped Raw.xlsx")
                            download_xlsx(Dove_Cross_pivot_table, label='Download Modified File (Summary)', filename="Dove Cross Category Summary.xlsx")

            # Dove + Superbowl Cateogry Summary:
            if option == 'Dove MB + Superbowl':
               # Function to download the Excel file
                def download_xlsx_Dove_Superbowl(df, label, filename):
                            excel_file = io.BytesIO()
                            df.to_excel(excel_file, index=False)
                            excel_file.seek(0)
                            st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                Dove_MB_Superbowl_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                dataframes = []
                if Dove_MB_Superbowl_files:                            
                    for file in Dove_MB_Superbowl_files:
                            df = pd.read_excel(file)
                            dataframes.append(df)
                   # Concatenate all DataFrames into a single DataFrame
                    Dove_MB_Superbowl_files_df = pd.concat(dataframes, ignore_index=True)
                    st.write("Dove MB + Superbowl Raw Data")
                    # Display the concatenated DataFrame
                    st.write(Dove_MB_Superbowl_files_df)
                    # Streamlit file uploader for the Campaign Mapping file
                campaign_mapping_file = st.file_uploader("Upload your Campaign Mapping file", type=["xlsx"], accept_multiple_files=False)             
                if campaign_mapping_file is not None:
                                        # Read the Excel file
                            campaign_mapping_file_df = pd.read_excel(campaign_mapping_file)
                            # Rename the column
                            campaign_mapping_file_df.rename(columns={'Prisma Campaign Name': 'Prisma_Campaign_Secondary'}, inplace=True)
                            # Display the DataFrame with the renamed column
                            st.write("Dove MB + Superbowl Campaign Mapping File")
                            st.write(campaign_mapping_file_df)
                 # Merge the Campaign Mapping DataFrame with the Dove MB Superbowl DataFrame
                Dove_MB_merged_final = Dove_MB_Superbowl_files_df.merge(campaign_mapping_file_df[['Prisma_Campaign_Secondary','Superbowl']], on='Prisma_Campaign_Secondary', how='left')
                Dove_MB_merged_final['Superbowl'] = Dove_MB_merged_final['Superbowl'].fillna('Dove Masterbrand Non Superbowl')
                st.write("Dove MB + Superbowl Mapped Data")
                st.write(Dove_MB_merged_final)
                # Convert 'Date' column to datetime and handle missing values
                Dove_MB_merged_final['Date'] = pd.to_datetime(Dove_MB_merged_final['Date'], errors='coerce')
                Dove_MB_merged_df = Dove_MB_merged_final.fillna(0)
                # Ensure specific columns are numeric
                numeric_columns = ['Impressions', 'Clicks', 'Media_Cost','GRPs']
                Dove_MB_merged_df[numeric_columns] = Dove_MB_merged_df[numeric_columns].apply(pd.to_numeric, errors='coerce')
                # Create a pivot table with the required aggregations
                Dove_MB_Superbowl_pivot_table = Dove_MB_merged_df.pivot_table(
                    values=['Impressions', 'Clicks', 'Media_Cost','GRPs'],
                    index=[Dove_MB_merged_df['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience','Superbowl'],
                    aggfunc='sum').reset_index()
                # Download buttons for the processed files
                download_xlsx_Dove_Superbowl(Dove_MB_merged_df, label='Download Modified File (Mapped)', filename="Dove_MB_Superbowl_Mapped_Raw.xlsx")
                download_xlsx_Dove_Superbowl(Dove_MB_Superbowl_pivot_table, label='Download Modified File (Summary)', filename="Dove_MB_Superbowl_Summary.xlsx")          # Read each file into a DataFrame               
                                
  
        #Dove PW Summary:

            if option == 'Dove PW':
                # Function to download Excel file
                def download_xlsx_Dove_PW(df, label, filename):
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                # File uploader for Dove PW files
                Dove_PW_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                dataframes = []
                if Dove_PW_files:
                    for file in Dove_PW_files:
                        df = pd.read_excel(file)
                        dataframes.append(df)
                    Dove_PW_files_df = pd.concat(dataframes, ignore_index=True)
                    
                    # Concatenate columns to create 'Audience_mapping_df' column
                    Dove_PW_files_df['Audience_mapping_df'] = Dove_PW_files_df[['Channel', 'Raw_Partner', 'Audience']].astype(str).agg('-'.join, axis=1)
                    
                    st.write("Dove PW Raw Data")
                    st.write(Dove_PW_files_df)

                # File uploader for Campaign Mapping file
                mapping = st.file_uploader("Upload your Campaign Mapping file", type=["xlsx"], accept_multiple_files=False)
                if mapping is not None:
                    try:
                        # Automatically select the "daypart" sheet
                        daypart_df = pd.read_excel(mapping, sheet_name='Daypart')
                        st.write("Daypart Mapping File - Sheet: daypart")
                        st.write(daypart_df)
                        
                        # Automatically select the "UE" sheet for Audience
                        UE_df = pd.read_excel(mapping, sheet_name='UE')
                        st.write("Universal Estimate Mapping File - Sheet: UE")
                        st.write(UE_df)

                        # Automatically select the "Campaign" sheet for Audience
                        Campaign_df = pd.read_excel(mapping, sheet_name='Dove PW C')
                        st.write("Campaign Mapping File - Sheet: Dove PW C")
                        st.write(Campaign_df)

                        # Automatically select the "Audience" sheet
                        audience_df = pd.read_excel(mapping, sheet_name='Dove PW A')
                        st.write("Audience Mapping File - Sheet: Dove PW A")
                        st.write(audience_df)
                        audience_df['Audience_mapping_df'] = audience_df[['Channel', 'Raw_Partner', 'Audience']].astype(str).agg('-'.join, axis=1)
                        
                    except ValueError as e:
                        st.error(f"Error reading sheets from the mapping file: {e}")
                    
                    # Check if 'Daypart' columns are present
                    if 'Daypart' in Dove_PW_files_df.columns and 'Daypart' in daypart_df.columns:
                        # Merge Dove PW DataFrame with daypart DataFrame
                        Dove_PW_files_df = Dove_PW_files_df.merge(daypart_df, on='Daypart', how='left')
                    else:
                        st.error("Daypart column not found in either the Dove PW data or the Daypart mapping data.")

                    # Check if 'Audience' columns are present
                    if 'Audience' in Dove_PW_files_df.columns and 'Audience' in UE_df.columns:
                        # Merge the resulting DataFrame with audience DataFrame
                        Dove_PW_files_df = Dove_PW_files_df.merge(UE_df, on='Audience', how='left')
                    else:
                        st.error("Audience column not found in either the Dove PW data or the Audience mapping data.")
                    
                    # Check if 'Campaign' columns are present
                    if 'Campaign' in Dove_PW_files_df.columns and 'Campaign' in Campaign_df.columns:
                        # Merge the resulting DataFrame with Campaign DataFrame
                        Dove_PW_files_df = Dove_PW_files_df.merge(Campaign_df, on='Campaign', how='left')
                    else:
                        st.error("Campaign column not found in either the Dove PW data or the Campaign mapping data.")
                    
                    # Check if 'Audience_mapping_df' column is present in both DataFrames
                    if 'Audience_mapping_df' in Dove_PW_files_df.columns and 'Audience_mapping_df' in audience_df.columns:
                        # Merge Dove PW DataFrame with audience DataFrame on 'Audience_mapping_df'
                        Dove_PW_files_df = Dove_PW_files_df.merge(audience_df, on='Audience_mapping_df', how='left')
                    else:
                        st.error("Audience_mapping_df column not found in either the Dove PW data or the Audience mapping data.")
                    
                    # Drop unwanted columns
                    columns_to_drop = ['Audience_mapping_df', 'Channel_y', 'Raw_Partner_y', 'Audience_y']
                    Dove_PW_files_df = Dove_PW_files_df.drop(columns=columns_to_drop, errors='ignore')
                    Dove_PW_files_df = Dove_PW_files_df.rename(columns={
                        'Channel_x': 'Channel',
                        'Raw_Partner_x': 'Raw_Partner',
                        'Audience_x': 'Audience'
                    })
                    
                    

                    # Ensure the Date column is in datetime format
                    Dove_PW_files_df['Date'] = pd.to_datetime(Dove_PW_files_df['Date'], errors='coerce')
                    
                    # Check for non-null and properly formatted Date values
                    if Dove_PW_files_df['Date'].isnull().any():
                        st.error("There are null or improperly formatted Date values in the data.")
                    # Display the mapped data
                    st.write("Mapped Dove PW Data")
                    st.write(Dove_PW_files_df)
                    
                    # Creating pivot table
                    Dove_PW_pivot_table_77 = Dove_PW_files_df.pivot_table(
                        values=['Impressions', 'Clicks', 'Media_Cost', 'GRPs', 'Video_Views'],
                        index=[Dove_PW_files_df['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Hierarchy', 'Product Line', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience', 'Mapped Audience', 'Daypart', 'Bucket', 'Mapped to OLD RROI Logic'],
                        aggfunc='sum'
                    ).reset_index()

                    # Provide download button for mapped data
                    download_xlsx_Dove_PW(Dove_PW_files_df, label="Download Mapped Dove PW Data", filename="Dove_PW_Processed_File.xlsx")
                    download_xlsx_Dove_PW(Dove_PW_pivot_table_77, label='Download Modified File (Summary)', filename="Dove_PW_Summary.xlsx")

                    # Display the pivot table for verification
                    st.write("Pivot Table Summary")
                    st.write(Dove_PW_pivot_table_77)
    if selected == "Datapoem Format":
            st.header("Datapoem Format Preparation Process")
            uploaded_files = st.file_uploader("Upload your Excel file(s) to prepare the datapoem format:", type=["xlsx"], accept_multiple_files=True)
            if uploaded_files is not None:
                for file in uploaded_files:
                    # Read each uploaded file as a DataFrame
                    df = pd.read_excel(file)
                    # Rename the columns
                    df.rename(columns={'Channel': 'Channel Name','Brand':'Brand Name','Master_Channel':'Master Channel','Product_Line':'Product Line','Package_Placement_Name':'Placement Name','Campaign':'Campaign Name','Prisma_Campaign_Secondary':'Merged Campaign name','Raw_Partner':'Platform','Standardized_Partner':'Merged Platform','Media_Cost':'Spends','Mapped Audience':'Merged Audience'}, inplace=True)
                    
                    raw_format = [
                        'HH Universe','Year', 'Month', 'Day','Start Date', 'End Date', 'Number of Days', 
                        'Sub category', 'Business Unit','Model Name', 'Brand or Competition', 'Modeling Brand',
                        'Advertiser', 'Sub Brand', 'Media type', 'Campaign Objective',
                        'Media Channel', 'Merged Media Channel',
                        'Merged TV Channel Name',  'Platform Genre',
                        'Merged Platform Genre', 'Vendor Name', 'Influencer Name', 'Live Cricket or other live events or Not live',
                        'Event Type', 'Language', 'Merged Language', 'Ad Type', 'Merged Ad Type',
                        'Country', 'Market/State','Merged Market/State', 'City', 'Merged City', 'Modeling Market', 'Demographic',
                        'Sessions',  'Leads', 'Engagement', 'Clicks', 'Key Words', 'DOBR Quotes',
                        'Overall Quotes', 'Modeling Metrics (Data POEM will fill in)', 'Likes', 'Shares', 'Engagements', 'SMS',
                        'Push Notification', 'Email', 'App Installs', 'Search Volume', 'Offer Details', 'Coupons', 'Orders', 'Revenue',
                        'BC DEPARTMENT', 'BC SUPER CATEGORY', 'BC CATEGORY', 'BC SUB CATEGORY', 'BRAND OWNER HIGH', 'BRAND FAMILY',
                        'BRAND HIGH', 'BRAND LOW', 'BRAND OWNER LOW', '$', 'Units', 'Avg Unit Price', 'Any Promo Unit Price', 'No Promo Unit Price',
                        'Disp w/o Feat Unit Price', 'Feat w/o Disp Unit Price', 'Feat & Disp Unit Price', 'Any Disp Unit Price', 'Any Feat Unit Price',
                        'Any Price Decr Unit Price', 'TDP', '%ACV', 'Any Promo $', 'No Promo $']

                    DP_format_columns = pd.DataFrame(columns=raw_format)
                    DP_Format = pd.concat([df, DP_format_columns], axis=1)
                    DP_Format['Date'] = pd.to_datetime(DP_Format['Date'])
                    DP_Format['Year'] = DP_Format['Date'].dt.year
                    DP_Format['Month'] = DP_Format['Date'].dt.month
                    DP_Format['Day'] = DP_Format['Date'].dt.day
                    DP_Format['Date'] = DP_Format['Date'].dt.date             

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = DP_Format

                    def download_xlsx_4(df, label, filename):
                        excel_file = io.BytesIO()
                        df.to_excel(excel_file, index=False)
                        excel_file.seek(0)
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                    # Call the function to display download button for the modified file
                    download_xlsx_4(DP_Format, label=f'Download Modified File ({file.name})', filename=file.name)
          

elif selected == "Non Paid Media":
    st.subheader("Non Paid Media")


    # Function to save uploaded files in a folder
    def save_uploaded_files(uploaded_files, save_dir="uploaded_folder"):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        file_data = []
        
        for uploaded_file in uploaded_files:
            folder_name = uploaded_file.name.split("/")[0]  # Assuming folder name is part of file name
            file_name = uploaded_file.name.split("/")[-1]  # Get file name only
            
            folder_path = os.path.join(save_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            file_data.append({"Folder Name": folder_name, "File Name": file_name, "File Path": file_path})
        
        return file_data

    def save_uploaded_files(uploaded_files):
        file_data = []
        
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, encoding="latin1")
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file, engine="openpyxl")  # Read the file
                    
            # Process "Email" files
            if "Email" in uploaded_file.name:  
                required_columns = ["date", "sent", "cost"]
                if all(col in df.columns for col in required_columns):
                    df["date"] = pd.to_datetime(df["date"])  # Convert date column
                    start_date = df["date"].min()
                    end_date = df["date"].max()
                    impressions = df["sent"].sum()
                    spends = df["cost"].sum()
                    
                    # Simulated File Path
                    file_path = f"/uploaded_files/{uploaded_file.name}"

                    file_data.append({
                        "File Path": file_path,
                        "File Name": uploaded_file.name,
                        "Start Date": start_date,
                        "End Date": end_date,
                        "Impressions": impressions,
                        "Spends": spends
                    })

            # Process "Website" files
            if "Website Sessions" in uploaded_file.name:  
                required_columns = ["Date", "Sessions"]
                if all(col in df.columns for col in required_columns):
                    df["Date"] = pd.to_datetime(df["Date"])  # Convert date column
                    start_date = df["Date"].min()
                    end_date = df["Date"].max()
                    impressions = df["Sessions"].sum()

                    # Simulated File Path
                    file_path = f"/uploaded_files/{uploaded_file.name}"

                    file_data.append({
                        "File Path": file_path,
                        "File Name": uploaded_file.name,
                        "Start Date": start_date,
                        "End Date": end_date,
                        "Impressions": impressions,
                    })

            if "website sessions" in uploaded_file.name:  
                required_columns = ["Date", "Sessions"]
                if all(col in df.columns for col in required_columns):
                    df["Date"] = pd.to_datetime(df["Date"])  # Convert date column
                    start_date = df["Date"].min()
                    end_date = df["Date"].max()
                    impressions = df["Sessions"].sum()

                    # Simulated File Path
                    file_path = f"/uploaded_files/{uploaded_file.name}"

                    file_data.append({
                        "File Path": file_path,
                        "File Name": uploaded_file.name,
                        "Start Date": start_date,
                        "End Date": end_date,
                        "Impressions": impressions,
                    }) 

            if "all other categories sessions" in uploaded_file.name:  
                required_columns = ["Date", "Sessions Start"]
                if all(col in df.columns for col in required_columns):
                    df["Date"] = pd.to_datetime(df["Date"])  # Convert date column
                    start_date = df["Date"].min()
                    end_date = df["Date"].max()
                    impressions = df["Sessions Start"].sum()

                    # Simulated File Path
                    file_path = f"/uploaded_files/{uploaded_file.name}"

                    file_data.append({
                        "File Path": file_path,
                        "File Name": uploaded_file.name,
                        "Start Date": start_date,
                        "End Date": end_date,
                        "Impressions": impressions,
                    }) 


        return file_data

    def generate_csv(file_data):
        df = pd.DataFrame(file_data)[["File Path", "File Name", "Start Date", "End Date", "Impressions", "Spends"]]
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()

    st.title("File Upload & Processing")

    uploaded_files = st.file_uploader("Upload multiple files", accept_multiple_files=True)

    if uploaded_files:
        file_data = save_uploaded_files(uploaded_files)

        if file_data:
            st.success("Files processed successfully!")

            # Generate CSV
            csv_file = generate_csv(file_data)

            # Provide CSV for download
            st.download_button(
                label="Download CSV with Summary",
                data=csv_file,
                file_name="uploaded_files_summary.csv",
                mime="text/csv"
            )


    # # Text inputs for the user to input dates
    # input_date_1_str = st.text_input("Enter the first date (dd-mm-yyyy)", "01-05-2024")
    # input_date_2_str = st.text_input("Enter the second date (dd-mm-yyyy)", "31-05-2024")
    
    # try:
    #     # Convert input dates to datetime objects
    #     input_date_1 = pd.to_datetime(input_date_1_str, format='%d-%m-%Y')
    #     input_date_2 = pd.to_datetime(input_date_2_str, format='%d-%m-%Y')
    #     days_between_inputs = (input_date_2 - input_date_1).days
    #     st.write(f"Number of days between {input_date_1.date()} and {input_date_2.date()} is: {days_between_inputs + 1} days")
    # except ValueError:
    #     st.write("Please enter valid dates in the format dd-mm-yyyy.")
    
    # # File uploader for non-digital coupon file
    # uploaded_file = st.file_uploader("Choose a Non Digital Coupon File", type=['xlsx'])

    # if uploaded_file is not None:
    #     # Read the uploaded Excel file
    #     df = pd.read_excel(uploaded_file)
    #     # Display some information More More Feature More Feature the uploaded file
    #     st.write("### Uploaded the Non Digital Coupon File:")
    #     st.write(df)

    #     # Ensure the date columns are in datetime format
    #     df['Issue_Date'] = pd.to_datetime(df['Issue_Date'], format='%Y-%m-%d')
    #     df['Expire_Date'] = pd.to_datetime(df['Expire_Date'], format='%Y-%m-%d')

    #     # Calculate the Expire_Date(DP) column
    #     df['Expire_Date(DP)'] = df.apply(
    #         lambda row: row['Issue_Date'] + pd.DateOffset(weeks=8) 
    #         if row['ConsumerRedemptionPeriod'] in [9, 10] 
    #         else row['Expire_Date'], 
    #         axis=1
    #     )

    #     # Calculate the number of overlapping days with the input date range
    #     def calculate_overlapping_days(row, start_date, end_date):
    #         if (start_date >= row['Issue_Date'] and end_date <= row['Expire_Date(DP)']) or (start_date < row['Expire_Date(DP)'] and end_date > row['Issue_Date']):
    #             return (min(row['Expire_Date(DP)'], end_date) - max(row['Issue_Date'], start_date)).days + 1
    #         else:
    #             return 0

    #     df['Date Range'] = df.apply(calculate_overlapping_days, axis=1, start_date=input_date_1, end_date=input_date_2)

    #     # Calculate the final cost
    #     df['Final Cost'] = df['WeeklyCost'] / 7 * df['Date Range']

    #     # Display the updated DataFrame with the new columns including Final Cost
    #     st.write("### Calculated Non Digital Coupon Data:")
    #     st.write(df)

    #     # Optionally, allow the user to download the updated DataFrame as an Excel file
    #     @st.cache_data
    #     def convert_df_to_excel(df):
    #         output = io.BytesIO()
    #         with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    #             df.to_excel(writer, index=False, sheet_name='Sheet1')
    #         return output.getvalue()

    #     excel_data = convert_df_to_excel(df)

    #     st.download_button(
    #         label="Download updated file as Excel",
    #         data=excel_data,
    #         file_name="updated_coupon_file.xlsx",
    #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     )

elif selected == "Competition":
    st.subheader("Pathmatics")
    # Upload the file
    uploaded_file = st.file_uploader("Choose a Pathmatics CSV File", type=['csv'])

    if uploaded_file is not None:
        try:
            # Read the CSV file and skip the first row
            df = pd.read_csv(uploaded_file, skiprows=1)
            # Display the dataframe
            st.write("### Uploaded the Pathmatics CSV File File:")
            st.write(df)
            
        except Exception as e:
            st.error(f"Error: {e}")

       
        #Axe Deo Brand

        Axe_Deo_Brand = df[df['Category Level 8'].isin(['Personal Care',"Men's Body Washes, Exfoliants & Scrubs","Men's Deodorants & Antiperspirants Sprays & Body Sprays"])]
        Axe_Deo_Brand_1 = Axe_Deo_Brand[Axe_Deo_Brand['Brand Root'].isin(['Axe Products'])]
        st.write(Axe_Deo_Brand_1)

        #Axe Deo Competition

        Axe_Deo_Competition = df[df['Category Level 8'].isin(['Personal Care',"Men's Body Washes, Exfoliants & Scrubs","Men's Deodorants & Antiperspirants Sprays & Body Sprays"])]
        Axe_Deo_Competition_1 = Axe_Deo_Competition[~Axe_Deo_Competition['Brand Root'].isin(['Axe Products'])]
        st.write(Axe_Deo_Competition_1)
        
    #st.subheader("Kantar")
    
elif selected == "Nielsen":
    
        # Function to read text file and convert to DataFrame
    def convert_to_dataframe(uploaded_file):
        # Read the text file with '|' delimiter
        df = pd.read_csv(uploaded_file, delimiter='|', dtype={'UPC': 'object'})
        # Check if 'Period Description' column exists
        if 'Period Description' in df.columns:
            # Extract dates from 'Period Description' if the file name contains "prd"
            if 'prd' in uploaded_file.name.lower():
                df['Date'] = pd.to_datetime(df['Period Description'].str.extract(r'(\d{2}/\d{2}/\d{2})')[0], format='%m/%d/%y')
        return df

    # Function to download DataFrame as CSV file
    def download_csv_raw(df, label, filename='Nielsen_Raw_Data.csv'):
        output = io.StringIO()
        df.to_csv(output, index=False)
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")

    def download_csv_pc(df, label, filename='PC_Filtered_Raw_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")

    def download_csv_BnW(df, label, filename='BnW_Filtered_Raw_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")

    def download_csv_NIC(df, label, filename='NIC_Filtered_Raw_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")
    def download_csv_NIC_Competition(df, label, filename='PC_Filtered_Raw_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv") 

    def download_csv_Mars(df, label, filename='Mars_Brands_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")     
    
    def sidebar_filters_Unilever(data):
        st.sidebar.header("Filter by Market Description")
        MARKET_DESCRIPTION = st.sidebar.multiselect("Select the MARKET_DESCRIPTION:", options=data["Market Description"].unique())
        data = data[data["Market Description"].isin(MARKET_DESCRIPTION)]
        st.sidebar.header("Filter by Brand")
        BRAND = st.sidebar.multiselect("Select the Brand:", options=data["BRAND"].unique())
        data = data[data["BRAND"].isin(BRAND)]
        st.sidebar.header("Filter by Category")
        CATEGORY = st.sidebar.multiselect("Select the CATEGORY:", options=data["CATEGORY"].unique())
        data = data[data["CATEGORY"].isin(CATEGORY)]
        st.sidebar.header("Filter by SUB Category")
        SUB_CATEGORY = st.sidebar.multiselect("Select the SUB CATEGORY:", options=data["SUB CATEGORY"].unique())
        data = data[data["SUB CATEGORY"].isin(SUB_CATEGORY)]
        return data
    def generate_Unilever_pivot_table(filtered_data):
        pivot_table = filtered_data.pivot_table(index=['Market Description', 'BRAND','CATEGORY','SUB CATEGORY'], values='$', aggfunc='sum')
        pivot_table.reset_index(inplace=True) 
        return pivot_table
    
    def sidebar_filters_Mars(data):
        st.sidebar.header("Filter by Brand")
        BRAND = st.sidebar.multiselect("Select the Brand:", options=data["BRAND"].unique())
        data = data[data["BRAND"].isin(BRAND)]
        st.sidebar.header("Filter by Category")
        CATEGORY = st.sidebar.multiselect("Select the CATEGORY:", options=data["MARS_CATEGORY"].unique())
        data = data[data["MARS_CATEGORY"].isin(CATEGORY)]
        st.sidebar.header("Filter by SUB Category")
        SUB_CATEGORY = st.sidebar.multiselect("Select the SUB CATEGORY:", options=data["MARS_SUB-CATEGORY"].unique())
        data = data[data["MARS_SUB-CATEGORY"].isin(SUB_CATEGORY)]
        return data
    def generate_Mars_pivot_table(filtered_data):
        pivot_table = filtered_data.pivot_table(index=['BRAND','MARS_CATEGORY','MARS_SUB-CATEGORY'], values='$', aggfunc='sum')
        pivot_table.reset_index(inplace=True) 
        return pivot_table
    
    def main():
        st.subheader('Nielsen')
        # Set title and description
        st.subheader('')
        # Upload text files
        uploaded_files = st.file_uploader("Choose Mars Text files", type=['txt'], accept_multiple_files=True)
        uploaded_file_names = set()  # Set to store uploaded file names
        dfs = []  # List to store DataFrames
        file_rows = {} 
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Check if the file is already uploaded
                if uploaded_file.name not in uploaded_file_names:
                    uploaded_file_names.add(uploaded_file.name)  # Add the file name to the set
                    # Read and convert each text file
                    df = convert_to_dataframe(uploaded_file)
                    dfs.append(df)  # Append the DataFrame to the list
                    file_rows[uploaded_file.name] = df.shape[0]  # Store the number of rows
                    file_name = uploaded_file.name  # Get the name of the uploaded file
                    # Display the file name and DataFrame
                    st.write(f"File Name: {file_name}")
                    st.write(df)
                else:
                    st.warning(f"File '{uploaded_file.name}' is already uploaded and cannot be browsed again.")
          # Merge DataFrames if multiple files are uploaded
        if len(dfs) > 0:
            Nielsen_Raw_Data = dfs[0]  # Initialize Nielsen_Raw_Data with the first DataFrame
            for df in dfs[1:]:
                # Adjust keys accordingly
                if 'Period Key' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['Period Key'], how='left')
                if 'Market Key' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['Market Key'], how='left')
                if 'PRODUCT KEY' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['PRODUCT KEY'], how='left')
            Nielsen_Raw_Data['DP_Date'] = pd.to_datetime(Nielsen_Raw_Data['Period Description'].str.extract(r'(\d{2}/\d{2}/\d{2})')[0], format='%m/%d/%y')
            Nielsen_Raw_Data['DP_Day'] = Nielsen_Raw_Data['DP_Date'].dt.day    
            Nielsen_Raw_Data['DP_Month'] = Nielsen_Raw_Data['DP_Date'].dt.month
            Nielsen_Raw_Data['DP_Year'] = Nielsen_Raw_Data['DP_Date'].dt.year
            Nielsen_Raw_Data['UPC'] = Nielsen_Raw_Data['UPC'].apply(lambda x: str(x).zfill(12))
            # Drop the 'Period Description' column
            # Nielsen_Raw_Data.drop(columns=['Period Description','Market Key','PRODUCT KEY','Period Key'], inplace=True)
            desired_order = [
                "DP_Date",
                "DP_Day", 
                "DP_Month",
                "DP_Year",
                "Market Key",
                "Market Description",
                "PRODUCT KEY",
                "MARS_CATEGORY",
                "MARS_SUB-CATEGORY",
                "UPC",
                "BASE SIZE",
                "BRAND",
                "BRAND FAMILY",
                "BRAND HIGH",
                "BRAND OWNER",
                "ITEM",
                "Period Key",
                "Period Description",
                "$",
                "Units",
                "Avg Unit Price",
                "Any Promo Unit Price",
                "No Promo Unit Price",
                "TDP",
                "%ACV",
                "Any Promo $",
                "No Promo $",
                "Feat & Disp $",
                "Any Disp $",
                "Any Feat $"
            ]
            Nielsen_Raw_Data = Nielsen_Raw_Data[desired_order]
            merged_rows = Nielsen_Raw_Data.shape[0]  
            st.write("Nielsen Raw Data:")
            st.write(Nielsen_Raw_Data)
            st.write(f"Number of rows in Nielsen_Raw_Data: {merged_rows}")
            st.write("Number of rows in each uploaded file:")
            for file_name, num_rows in file_rows.items():
                st.write(f"{file_name}: {num_rows}")
            download_csv_raw(Nielsen_Raw_Data, label="Download Mars_Raw_Data (csv)",filename="Mars_Raw_Data.csv")

            #Mars Brand:
                    
            Mars = Nielsen_Raw_Data[Nielsen_Raw_Data['BRAND OWNER'].isin(['MARS INCORPORATED'])]
            Mars_1 = Mars[Mars['BRAND HIGH'].str.contains('M&M', na=False)]
            Mars_1 = Mars_1.assign(
                DP_Organisation='Mars',
                DP_Business_Unit='FMCG',
                DP_Category='CONFECTIONERY',
                DP_Sub_category='CONFECTIONERY',
                DP_Brand='',
                DP_Total_Brand='',
                DP_Brand_Type = 'Brand')
            Mars_Brand_Data = pd.concat([Mars_1])   
            download_csv_Mars(Mars_Brand_Data, label="Download Mars_Brands_Data (csv)",filename="Mars_Brand_Data.csv")
            
            #Mars Competition:
                    
            Mars_Snickers_Competition = Nielsen_Raw_Data[Nielsen_Raw_Data['BRAND OWNER'].isin(['MARS INCORPORATED'])]
            Mars_Snickers_Competition_1 = Mars_Snickers_Competition[Mars_Snickers_Competition['BRAND'].str.contains('SNICKERS', na=False)]
            Mars_Snickers_Competition_1 = Mars_Snickers_Competition_1.assign(
                DP_Organisation=Mars_Snickers_Competition_1['BRAND OWNER'],
                DP_Business_Unit='FMCG',
                DP_Category='CONFECTIONERY',
                DP_Sub_category='CONFECTIONERY',
                DP_Brand='Snickers',
                DP_Total_Brand='Snickers',
                DP_Brand_Type = 'Competition',
                Competition_of = "Mars M&M"
                )
            Mars_Reese_Competition = Nielsen_Raw_Data[Nielsen_Raw_Data['BRAND OWNER'].isin(["HERSHEY CHOCOLATE, USA"])]
            Mars_Reese_Competition_1 = Mars_Reese_Competition[Mars_Reese_Competition['BRAND'].str.contains("REESE'S", na=False)]
            Mars_Reese_Competition_1 = Mars_Reese_Competition_1.assign(
                DP_Organisation=Mars_Reese_Competition_1['BRAND OWNER'],
                DP_Business_Unit='FMCG',
                DP_Category='CONFECTIONERY',
                DP_Sub_category='CONFECTIONERY',
                DP_Brand="Reese'S",
                DP_Total_Brand="Reese'S",
                DP_Brand_Type = 'Competition',
                Competition_of = "Mars M&M"
                )
            Mars_kinder_Competition = Nielsen_Raw_Data[Nielsen_Raw_Data['BRAND OWNER'].isin(["FERRERO U S A INC"])]
            Mars_kinder_Competition_1 = Mars_kinder_Competition[Mars_kinder_Competition['BRAND'].str.contains("KINDER", na=False)]
            Mars_kinder_Competition_1 = Mars_kinder_Competition_1.assign(
                DP_Organisation=Mars_kinder_Competition_1['BRAND OWNER'],
                DP_Business_Unit='FMCG',
                DP_Category='CONFECTIONERY',
                DP_Sub_category='CONFECTIONERY',
                DP_Brand='Kinder',
                DP_Total_Brand='Kinder',
                DP_Brand_Type = 'Competition',
                Competition_of = "Mars M&M"
                )
            Mars_Competition_Data = pd.concat([Mars_Reese_Competition_1,Mars_kinder_Competition_1,Mars_Snickers_Competition_1])   
            download_csv_Mars(Mars_Competition_Data, label="Download Mars_Competition_Data (csv)",filename="Mars_Competition_Data.csv")
            enable_filters = st.checkbox("Enable Sidebar Filters and Pivot Table")

            if enable_filters:
                filtered_data = sidebar_filters_Mars(Nielsen_Raw_Data)
                st.write("Filtered Data:")
                st.write(filtered_data)
                download_csv_raw(filtered_data, label="Download Filtered_Raw_Data (CSV)", filename='Filtered_Raw_Data.csv')

                # Generate pivot table from filtered data
                pivot_table = generate_Mars_pivot_table(filtered_data)
                st.write("Pivot Table:")
                st.write(pivot_table)
                download_csv_raw(pivot_table, label="Download Pivot_Table_Data (CSV)", filename='Pivot_Table_Data.csv')

          
    if __name__ == "__main__":            
        main()           

    # Main function to run the Streamlit web application
    def main():
        # Upload text files
        uploaded_files = st.file_uploader("Choose Unilevel Text files", type=['txt'], accept_multiple_files=True)

        uploaded_file_names = set()  # Set to store uploaded file names
        dfs = []  # List to store DataFrames
        file_rows = {}  # Dictionary to store number of rows for each file

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Check if the file is already uploaded
                if uploaded_file.name not in uploaded_file_names:
                    uploaded_file_names.add(uploaded_file.name)  # Add the file name to the set
                    # Read and convert each text file
                    df = convert_to_dataframe(uploaded_file)
                    dfs.append(df)  # Append the DataFrame to the list
                    file_rows[uploaded_file.name] = df.shape[0]  # Store the number of rows
                    file_name = uploaded_file.name  # Get the name of the uploaded file
                    # Display the file name and DataFrame
                    st.write(f"File Name: {file_name}")
                    st.write(df)
                else:
                    st.warning(f"File '{uploaded_file.name}' is already uploaded and cannot be browsed again.")

        # Merge DataFrames if multiple files are uploaded
        if len(dfs) > 0:
            Nielsen_Raw_Data = dfs[0]  # Initialize Nielsen_Raw_Data with the first DataFrame
            for df in dfs[1:]:
                # Adjust keys accordingly
                if 'Period Key' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['Period Key'], how='left')
                if 'Market Key' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['Market Key'], how='left')
                if 'PRODUCT KEY' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['PRODUCT KEY'], how='left')
            Nielsen_Raw_Data['DP_Date'] = pd.to_datetime(Nielsen_Raw_Data['Period Description'].str.extract(r'(\d{2}/\d{2}/\d{2})')[0], format='%m/%d/%y')
            Nielsen_Raw_Data['DP_Day'] = Nielsen_Raw_Data['DP_Date'].dt.day    
            Nielsen_Raw_Data['DP_Month'] = Nielsen_Raw_Data['DP_Date'].dt.month
            Nielsen_Raw_Data['DP_Year'] = Nielsen_Raw_Data['DP_Date'].dt.year
            Nielsen_Raw_Data['UPC'] = Nielsen_Raw_Data['UPC'].apply(lambda x: str(x).zfill(12))
            # Drop the 'Period Description' column
            # Nielsen_Raw_Data.drop(columns=['Period Description','Market Key','PRODUCT KEY','Period Key'], inplace=True)
            desired_order = [
                "DP_Date",
                "DP_Day", 
                "DP_Month",
                "DP_Year",
                "Market Key",
                "Market Description",
                "PRODUCT KEY",
                "CATEGORY",
                "SUB CATEGORY",
                "UPC",
                "BASE SIZE",
                "BRAND",
                "BRAND FAMILY",
                "BRAND LOW",
                "BRAND OWNER",
                "DEPARTMENT",
                "PRODUCT SIZE",
                "TARGET GROUP AGE",
                "TARGET GROUP GENDER",
                "ITEM",
                "Period Key",
                "Period Description",
                "$",
                "Units",
                "Avg Unit Price",
                "Any Promo Unit Price",
                "No Promo Unit Price",
                "TDP",
                "%ACV",
                "Any Promo $",
                "No Promo $",
                "Feat & Disp $",
                "Any Disp $",
                "Any Feat $"
            ]
            Nielsen_Raw_Data = Nielsen_Raw_Data[desired_order]
            merged_rows = Nielsen_Raw_Data.shape[0]
            st.write("Nielsen Raw Data:")
            st.write(Nielsen_Raw_Data)
            st.write(f"Number of rows in Nielsen_Raw_Data: {merged_rows}")
            st.write("Number of rows in each uploaded file:")
            for file_name, num_rows in file_rows.items():
                st.write(f"{file_name}: {num_rows}")
            download_csv_raw(Nielsen_Raw_Data, label="Download Unilever_Raw_Data (csv)",filename="Unilever_Raw_Data.csv")
         
            #Bar:
                    
            Bar_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['CATEGORY'].isin(['SOAP'])]
            Bar_2 = Bar_1[Bar_1['SUB CATEGORY'].isin(['BAR'])]
            Bar_3 = Bar_2[Bar_2['Market Description'].isin(['Total US xAOC'])]
            Bar_4 = Bar_3[Bar_3['BRAND'].isin(['DOVE (UNILEVER HOME & PERSONAL CARE)'])]
            Bar_5 = Bar_4[~Bar_4['BRAND FAMILY'].isin(['DOVE MEN + CARE (UNILEVER HOME & PERSONAL CARE)'])]
            Bar_5 = Bar_5.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Personal Care',
                DP_Category='Skin Cleansing',
                DP_Sub_category='Bar',
                DP_Brand='PC Dove Bar',
                DP_Total_Brand='PC PW Dove')
            
            #Bodywash

            Bodywash_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['CATEGORY'].isin(['BODY WASH','EXFOLIATOR/SCRUBS'])]
            Bodywash_2 = Bodywash_1[Bodywash_1['SUB CATEGORY'].isin(['CHILD','UNISEX','WOMEN'])]
            Bodywash_3 = Bodywash_2[Bodywash_2['Market Description'].isin(['Total US xAOC'])]
            Bodywash_4 = Bodywash_3[Bodywash_3['BRAND'].isin(['DOVE (UNILEVER HOME & PERSONAL CARE)'])]
            Bodywash_5 = Bodywash_4[~Bodywash_4['BRAND FAMILY'].isin(['DOVE MEN + CARE (UNILEVER HOME & PERSONAL CARE)'])]
            Bodywash_5 = Bodywash_5.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Personal Care',
                DP_Category='Skin Cleansing',
                DP_Sub_category='Bodywash',
                DP_Brand='PC Dove BW',
                DP_Total_Brand='PC PW Dove')

            #PW DMC

            PW_DMC_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            PW_DMC_2 = PW_DMC_1[PW_DMC_1['BRAND FAMILY'].isin(['DOVE MEN + CARE (UNILEVER HOME & PERSONAL CARE)'])]
            PW_DMC_3 = PW_DMC_2[PW_DMC_2['CATEGORY'].isin(['BODY WASH','EXFOLIATOR/SCRUBS','SOAP'])]
            PW_DMC_3 = PW_DMC_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Personal Care',
                DP_Category='Skin Cleansing',
                DP_Sub_category='PW DMC',
                DP_Brand='PC DMC PW',
                DP_Total_Brand='PC DMC PW')

            ########################################### Deodorant ##########################################################

            #Deo DMC

            Deo_DMC_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Deo_DMC_2 = Deo_DMC_1[Deo_DMC_1['BRAND FAMILY'].isin(['DOVE MEN + CARE (UNILEVER HOME & PERSONAL CARE)'])]
            Deo_DMC_3 = Deo_DMC_2[Deo_DMC_2['CATEGORY'].isin(['AP & DEO','DEODORANT'])]
            Deo_DMC_3 = Deo_DMC_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Personal Care',
                DP_Category='Skin Cleansing',
                DP_Sub_category='PW DMC',
                DP_Brand='PC DMC Deo',
                DP_Total_Brand='PC DMC Deo')

            #Deo Dove

            Deo_Dove_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Deo_Dove_2 = Deo_Dove_1[Deo_Dove_1['CATEGORY'].isin(['AP & DEO','DEODORANT'])]
            Deo_Dove_3 = Deo_Dove_2[Deo_Dove_2['SUB CATEGORY'].isin(['WOMEN'])]
            Deo_Dove_4 = Deo_Dove_3[Deo_Dove_3['BRAND'].isin(['DOVE (UNILEVER HOME & PERSONAL CARE)'])]
            Deo_Dove_4 = Deo_Dove_4.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Personal Care',
                DP_Category='Deodorant',
                DP_Sub_category='Deo Dove',
                DP_Brand='PC Deo Dove',
                DP_Total_Brand='PC Deo Dove')
            #Deo Axe

            Deo_Axe_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Deo_Axe_2 = Deo_Axe_1[Deo_Axe_1['CATEGORY'].isin(['AP & DEO','DEODORANT','BODY SPRAY'])]
            Deo_Axe_3 = Deo_Axe_2[Deo_Axe_2['BRAND'].isin(['AXE (UNILEVER HOME & PERSONAL CARE)'])]
            Deo_Axe_3 = Deo_Axe_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Personal Care',
                DP_Category='Deodorant',
                DP_Sub_category='Axe',
                DP_Brand='PC Axe Deo',
                DP_Total_Brand='PC Axe Deo')

            #Deo Degree

            Deo_Degree_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Deo_Degree_2 = Deo_Degree_1[Deo_Degree_1['BRAND'].isin(['DEGREE (UNILEVER HOME & PERSONAL CARE)',"UNLIMITED BY DEGREE (UNILEVER HOME & PERSONAL CARE)"])]
            Deo_Degree_3 = Deo_Degree_2[Deo_Degree_2['CATEGORY'].isin(['AP & DEO','DEODORANT'])]
            Deo_Degree_3 = Deo_Degree_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Personal Care',
                DP_Category='Deodorant',
                DP_Sub_category='Degree',
                DP_Brand='',
                DP_Total_Brand='PC Degree')

            PC_Filted_Data = pd.concat([Bar_5, Bodywash_5, PW_DMC_3, Deo_DMC_3, Deo_Dove_4, Deo_Axe_3, Deo_Degree_3])     
            download_csv_pc(PC_Filted_Data, label="Download PC_Brands_Data (csv)",filename="Unilever_PC_Brand_Data.csv")

            #Bnw Brands
            #Dove Haircare

            Dove_Haircare_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Dove_Haircare_2 = Dove_Haircare_1[Dove_Haircare_1['BRAND'].isin(['DOVE (UNILEVER HOME & PERSONAL CARE)'])]
            Dove_Haircare_3 = Dove_Haircare_2[Dove_Haircare_2['CATEGORY'].isin(['SHAMPOO','STYLING PRODUCTS','BODY','SHAMPOO AND CONDITIONER COMBO','CONDITIONER','HAIR SPRAY','REMAINING HBL'])]
            Dove_Haircare_3 = Dove_Haircare_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Beauty and Wellbeing',
                DP_Category='Haircare',
                DP_Sub_category='Haircare',
                DP_Brand='BnW HAIR Dove',
                DP_Total_Brand='BnW HAIR Dove')

            #Nexxus

            Nexxus_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Nexxus_2 = Nexxus_1[Nexxus_1['BRAND'].isin(['NEXXUS (NEXXUS PRODUCTS COMPANY)'])]
            Nexxus_3 = Nexxus_2[Nexxus_2['CATEGORY'].isin(['SHAMPOO','STYLING PRODUCTS','SHAMPOO AND CONDITIONER COMBO','CONDITIONER','HAIR SPRAY'])]
            Nexxus_3 = Nexxus_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Beauty and Wellbeing',
                DP_Category='Haircare',
                DP_Sub_category='Haircare',
                DP_Brand='BnW HAIR Nexxus',
                DP_Total_Brand='BnW HAIR Nexxus')

            #Sheamoisture

            sheamoisture_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            sheamoisture_2 = sheamoisture_1[sheamoisture_1['BRAND'].isin(['SHEA MOISTURE (SUNDIAL BRANDS LLC)'])]
            sheamoisture_3 = sheamoisture_2[sheamoisture_2['CATEGORY'].isin(['SHAMPOO','STYLING PRODUCTS','BODY','SHAMPOO AND CONDITIONER COMBO','CONDITIONER','HAIR SPRAY','REMAINING HBL'])]
            sheamoisture_3 = sheamoisture_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Beauty and Wellbeing',
                DP_Category='Haircare',
                DP_Sub_category='Haircare',
                DP_Brand='BnW HAIR Shea Moisture',
                DP_Total_Brand='BnW HAIR Shea Moisture')   

            #Tresemme

            Tresemme_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Tresemme_2 = Tresemme_1[Tresemme_1['BRAND'].isin(['TRESEMME (ALBERTO CULVER COMPANY)'])]
            Tresemme_3 = Tresemme_2[Tresemme_2['CATEGORY'].isin(['SHAMPOO','STYLING PRODUCTS','SHAMPOO AND CONDITIONER COMBO','CONDITIONER','HAIR SPRAY'])]
            Tresemme_3 = Tresemme_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Beauty and Wellbeing',
                DP_Category='Haircare',
                DP_Sub_category='Haircare',
                DP_Brand='BnW HAIR Tresemme',
                DP_Total_Brand='BnW HAIR Tresemme')   
    
            #Vaseline
            
            Vaseline = Nielsen_Raw_Data[Nielsen_Raw_Data['BRAND'].isin(['VASELINE (UNILEVER HOME & PERSONAL CARE)'])]
            Vaseline_1 = Vaseline[Vaseline['CATEGORY'].isin(['BODY','REMAINING HBL'])]
            Vaseline_1 = Vaseline_1.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Beauty and Wellbeing',
                DP_Category='Skincare',
                DP_Sub_category='Skincare',
                DP_Brand='BnW Skin Vaseline',
                DP_Total_Brand='BnW Skin Vaseline')  

            BnW_Filted_Data = pd.concat([Dove_Haircare_3, Nexxus_3, sheamoisture_3, Tresemme_3, Vaseline_1])     
            download_csv_BnW(BnW_Filted_Data, label="Download BnW_Brands_Data (csv)",filename="Unilever_BnW_Brand_Data.csv")
            
            #Brayers

            Breyers_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Breyers_2 = Breyers_1[Breyers_1['BRAND'].isin(['BREYERS (GOOD HUMOR-BREYERS ICE CREAM)'])]
            Breyers_3 = Breyers_2[Breyers_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            Brayers_3 = Breyers_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Icecream',
                DP_Category='Icecream',
                DP_Sub_category='Icecream',
                DP_Brand="NIC ICE Breyer's",
                DP_Total_Brand="NIC ICE Breyer's")  

            #Talenti

            Talenti_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Talenti_2 = Talenti_1[Talenti_1['BRAND'].isin(['TALENTI (TALENTI GELATO)'])]
            Talenti_3 = Talenti_2[Talenti_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            Talenti_3 = Talenti_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Icecream',
                DP_Category='Icecream',
                DP_Sub_category='Icecream',
                DP_Brand="NIC ICE Talenti",
                DP_Total_Brand="NIC ICE Talenti")

            #Klondike

            Klondike_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Klondike_2 = Klondike_1[Klondike_1['BRAND'].isin(['KLONDIKE (GOOD HUMOR-BREYERS ICE CREAM)'])]
            Klondike_3 = Klondike_2[Klondike_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            Klondike_3 = Klondike_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Icecream',
                DP_Category='Icecream',
                DP_Sub_category='Icecream',
                DP_Brand="NIC ICE Klondike",
                DP_Total_Brand="NIC ICE Klondike")
            
            #Yasso

            Yasso_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Yasso_2 = Yasso_1[Yasso_1['BRAND'].isin(['YASSO (YASSO INC)'])]
            Yasso_3 = Yasso_2[Yasso_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            Yasso_3 = Yasso_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Icecream',
                DP_Category='Icecream',
                DP_Sub_category='Icecream',
                DP_Brand="NIC Yasso",
                DP_Total_Brand="NIC Yasso")

            #Hellmanns

            Hellmanns_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Hellmanns_2 = Hellmanns_1[Hellmanns_1['BRAND'].isin(['BEST FOODS (UNILEVER BESTFOODS)',"HELLMANN'S (UNILEVER BESTFOODS)"])]
            Hellmanns_3 = Hellmanns_2[Hellmanns_2['CATEGORY'].isin(['MAYONNAISE'])]
            Hellmanns_3 = Hellmanns_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Nutritions',
                DP_Category='Nutritions',
                DP_Sub_category='Nutritions',
                DP_Brand="NIC Mayo Hellmanns",
                DP_Total_Brand="NIC Mayo Hellmanns")

            #knorr

            Knorr_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Knorr_2 = Knorr_1[Knorr_1['BRAND'].isin(['KNORR (UNILEVER BESTFOODS)'])]
            Knorr_3 = Knorr_2[Knorr_2['CATEGORY'].isin(['BOUILLON','RICE','PASTA','SHELF STABLE MEAL KIT'])]
            Knorr_3 = Knorr_3.assign(
                DP_Organisation='Unilever',
                DP_Business_Unit='Nutritions',
                DP_Category='Nutritions',
                DP_Sub_category='Nutritions',
                DP_Brand="NIC SCKRAID Knorr",
                DP_Total_Brand="NIC SCKRAID Knorr")

            NIC_Filted_Data = pd.concat([Brayers_3, Talenti_3, Klondike_3, Yasso_3, Hellmanns_3,Knorr_3])     
            download_csv_NIC(NIC_Filted_Data, label="Download NIC_Brands_Data (csv)",filename="Unilever_NIC_Brand_Data.csv")


            #NIC ICE Competition

            Breyers_Competition = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Breyers_Competition_2 = Breyers_Competition[~Breyers_Competition['BRAND'].isin(['BREYERS (GOOD HUMOR-BREYERS ICE CREAM)'])]
            Breyers_Competition_3 = Breyers_Competition_2[Breyers_Competition_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            Brayers_Competition_3 = Breyers_Competition_3.assign(
                DP_Organisation= Breyers_Competition_3['BRAND OWNER'],
                DP_Business_Unit='Icecream',
                DP_Category='Icecream',
                DP_Sub_category='Icecream',
                DP_Brand_Name = Breyers_Competition_3['BRAND'],
                DP_Brand_Type = "Competition",
                competition_of ="NIC ICE Breyer's")  
            Talenti_Competition = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Talenti_Competition_2 = Talenti_Competition[~Talenti_Competition['BRAND'].isin(['TALENTI (TALENTI GELATO)'])]
            Talenti_Competition_3 = Talenti_Competition_2[Talenti_Competition_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            Talenti_Competition_3 = Talenti_Competition_3.assign(
                DP_Organisation=Talenti_Competition_3['BRAND OWNER'],
                DP_Business_Unit='Icecream',
                DP_Category='Icecream',
                DP_Sub_category='Icecream',
                DP_Brand_Name=Talenti_Competition_3['BRAND'],
                competition_of="NIC ICE Talenti")
            Klondike_Competition_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Klondike_Competition_2 = Klondike_Competition_1[~Klondike_Competition_1['BRAND'].isin(['KLONDIKE (GOOD HUMOR-BREYERS ICE CREAM)'])]
            Klondike_Competition_3 = Klondike_Competition_2[Klondike_Competition_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            Klondike_Competition_3 = Klondike_Competition_3.assign(
                DP_Organisation=Klondike_Competition_3['BRAND OWNER'],
                DP_Business_Unit='Icecream',
                DP_Category='Icecream',
                DP_Sub_category='Icecream',
                DP_Brand_Name=Klondike_Competition_3['BRAND'],
                competition_of="NIC ICE Klondike")
            Yasso_Competition_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Yasso_Competition_2 = Yasso_Competition_1[~Yasso_Competition_1['BRAND'].isin(['YASSO (YASSO INC)'])]
            Yasso_Competition_3 = Yasso_Competition_2[Yasso_Competition_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            Yasso_Competition_3 = Yasso_Competition_3.assign(
                DP_Organisation=Yasso_Competition_3['BRAND OWNER'],
                DP_Business_Unit='Icecream',
                DP_Category='Icecream',
                DP_Sub_category='Icecream',
                DP_Brand_Name=Yasso_Competition_3['BRAND'],
                competition_of="NIC Yasso")
            
            NIC_Competition_Data = pd.concat([Brayers_Competition_3,Talenti_Competition_3,Klondike_Competition_3,Yasso_Competition_3])     
            download_csv_NIC_Competition(NIC_Competition_Data, label="Download NIC_Ice_Cream_Competition_Data (csv)",filename="Unilever_NIC_ICECREAM_Competition_Data.csv")
            #NIC Nutritions Competition

            Hellmanns_Competition_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Hellmanns_Competition_2 = Hellmanns_Competition_1[~Hellmanns_Competition_1['BRAND'].isin(['BEST FOODS (UNILEVER BESTFOODS)',"HELLMANN'S (UNILEVER BESTFOODS)"])]
            Hellmanns_Competition_3 = Hellmanns_Competition_2[Hellmanns_Competition_2['CATEGORY'].isin(['MAYONNAISE'])]
            Hellmanns_Competition_3 = Hellmanns_Competition_3.assign(
                DP_Organisation=Hellmanns_Competition_3['BRAND OWNER'],
                DP_Business_Unit='Nutritions',
                DP_Category='Nutritions',
                DP_Sub_category='Nutritions',
                DP_Brand_Name =Hellmanns_Competition_3['BRAND'],
                DP_Total_Brand="NIC Mayo Hellmanns")
            Knorr_Competition_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Knorr_Competition_2 = Knorr_Competition_1[~Knorr_Competition_1['BRAND'].isin(['KNORR (UNILEVER BESTFOODS)'])]
            Knorr_Competition_3 = Knorr_Competition_2[Knorr_Competition_2['CATEGORY'].isin(['BOUILLON','RICE','PASTA','SHELF STABLE MEAL KIT'])]
            Knorr_Competition_3 = Knorr_Competition_3.assign(
                DP_Organisation=Knorr_Competition_3['BRAND OWNER'],
                DP_Business_Unit='Nutritions',
                DP_Category='Nutritions',
                DP_Sub_category='Nutritions',
                DP_Brand_Name =Knorr_Competition_3['BRAND'],
                DP_Total_Brand="NIC SCKRAID Knorr")

            NIC_Competition_Data = pd.concat([Hellmanns_Competition_3,Knorr_Competition_3])     
            download_csv_NIC_Competition(NIC_Competition_Data, label="Download NIC_Nutritions_Competition_Data (csv)",filename="Unilever_NIC_NUTRITIONS_Competition_Data.csv")

           
            enable_filters = st.checkbox("Enable Sidebar Filters and Pivot Table")

            if enable_filters:
                filtered_data = sidebar_filters_Unilever(Nielsen_Raw_Data)
                st.write("Filtered Data:")
                st.write(filtered_data)
                download_csv_raw(filtered_data, label="Download Filtered_Raw_Data (CSV)", filename='Filtered_Raw_Data.csv')

                # Generate pivot table from filtered data
                pivot_table = generate_Unilever_pivot_table(filtered_data)
                st.write("Pivot Table:")
                st.write(pivot_table)
                download_csv_raw(pivot_table, label="Download Pivot_Table_Data (CSV)", filename='Pivot_Table_Data.csv')





    if __name__ == "__main__":
        main()
            
    # Add content for Playgourd here
elif selected == "Playground":
    st.subheader(f"You have selected {selected}")

    def initialize_session_state():
        if 'modified_files' not in st.session_state:
            st.session_state.modified_files = {}


    def download_xlsx(df, label, filename):
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def download_csv(df, label, filename):
        csv_file = io.StringIO()
        df.to_csv(csv_file, index=False)
        csv_file.seek(0)
        st.download_button(label=label, data=csv_file, file_name=filename, mime="text/csv")

        
    with st.sidebar:
        initialize_session_state()
        selected = st.selectbox("Main Menu", ['Data Preparation','Data Validation(Metrics)','Data Validation(dimensions)'], index=0)


    if selected == "Data Preparation":
        with st.sidebar:
            initialize_session_state()
            selected = st.selectbox("Main Menu", ['PC DEO AXE','PC DEO DEGREE FEMALE','PC DEO DEGREE MALE','PC DEO DMC','PC PW DMC','PC DEO DOVE','PC PW DOVE BAR','PC PW DOVE BW','BnW HAIR Shea Moisture','BnW HAIR Tresemme','BnW SKIN Vaseline','BnW HAIR Nexxus','BnW HAIR Dove',"NIC ICE Breyer's",'NIC ICE Klondike','NIC ICE Talenti','NIC ICE Yasso',"NIC Mayo Hellmann's","NIC SCKRAID Knorr Bouillon","NIC SCKRAID Knorr Sides"], index=0)
       
        if selected == "PC DEO AXE":
            st.subheader("PC DEO AXE")    
            Axe_PG_Data_Preparation = st.file_uploader("Upload your DEO Axe RROI Excel file", type=["xlsx"], accept_multiple_files=True)
            if Axe_PG_Data_Preparation:
                for Axe_PG_Data_Preparation_df in Axe_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(Axe_PG_Data_Preparation_df)

                        #DEO Axe Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias','Year-Month'])
                        
                        if "Axe" in Axe_PG_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Personal Care"
                            df["Category"] = "Deodorant"
                            df["Sub category"] = "Axe"
                            df["Brand"] = "PC Deo Axe"
                            df["Total Brand"] = "PC Deo Axe"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                coupon_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_filter, 'Platform'] = df.loc[coupon_filter, 'Product Line']
                                df.loc[coupon_filter, 'Product Line'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Product Line']
                                df.loc[Earned_Media_filter, 'Product Line'] = None  

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns:
                                Non_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Non_Media_filter, 'Channel/Daypart'] = df.loc[Non_Media_filter, 'Product Line']
                                df.loc[Non_Media_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                Owned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Owned_Media_filter, 'Platform'] = df.loc[Owned_Media_filter, 'Product Line']
                                df.loc[Owned_Media_filter, 'Product Line'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Shopper', 'Coupon')
                                coupon_Shopper_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_Shopper_filter, 'Platform'] = df.loc[coupon_Shopper_filter, 'Product Line']
                                df.loc[coupon_Shopper_filter, 'Product Line'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Shopper', 'Coupon')
                                coupon_Shopper_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_Shopper_filter, 'Platform'] = df.loc[coupon_Shopper_filter, 'Product Line']
                                df.loc[coupon_Shopper_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Trade Promo"
                                df.loc[trade_promo_filter, 'Channel/Daypart'] = (
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns and 'Daypart' not in df.columns:
                                df['Daypart'] = None
                            if 'Master Channel' in df.columns:
                                Master_Channel_TV_filter = df['Master Channel'] == "TV"
                                df.loc[Master_Channel_TV_filter, 'Daypart'] = df.loc[Master_Channel_TV_filter, 'Channel/Daypart']
                                df.loc[Master_Channel_TV_filter, 'Channel/Daypart'] = "TV"

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "TV"
                                df.loc[Product_line_TV_filter, 'Daypart'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = "TV"
                                df.loc[Product_line_TV_filter, 'Product Line'] = None  

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Digital"
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = "Digital"
                                df.loc[Product_line_TV_filter, 'Product Line'] = None  

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Coupon"
                                df.loc[Product_line_TV_filter, 'Platform'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = "Coupon"
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Commerce & Search"
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = "Commerce & Search"
                                df.loc[Product_line_TV_filter, 'Product Line'] = None  

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                df['Platform'] = df['Platform'].replace('Facebook', 'Facebook page Post')
                                df['Platform'] = df['Platform'].replace('Instagram', 'Instagram page Post')
                                df['Platform'] = df['Platform'].replace('Twitter', 'Twitter page Post')                                         
                                df['Platform'] = df['Platform'].replace('Web Traffic', 'Web_Analytics')
                                df['Master Channel'] = df['Master Channel'].replace('Baseline', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Recipients', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Sessions', ' ')
                                    
                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel/Daypart'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Seasonality"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel/Daypart'] = "Seasonality Monthly"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Master Channel'] == "Coupon"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                        df['Normalized Cost'] = (df['Cost'])
                        df['Normalized Impression'] = (df['Impression'])
                        df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df[['Influencer Say','Color Code','Data Through']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel", "Platform", 
                            "Influencer Say", "Color Code", "Audience", "Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                                                # Display the processed DataFrame
                        st.write(f"Processed DataFrame for: {Axe_PG_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')

                        csv_data = convert_df_to_csv(df)

                        st.download_button(
                            label="Download DEO Axe Playground Processed CSV",
                            data=csv_data,
                            file_name="DEO_Axe_Playground_Processed_Data.csv",
                            mime='text/csv'
                        )
                    except Exception as e:
                        st.error(f"Error processing {Axe_PG_Data_Preparation_df.name}: {e}")
                
        if selected == "PC DEO DEGREE FEMALE":
            st.subheader("PC DEO DEGREE FEMALE")  
            Degree_Female_PG_Data_Preparation = st.file_uploader("Upload your Deo Degree Female RROI file", type=["xlsx"], accept_multiple_files=True)
            if Degree_Female_PG_Data_Preparation:
                for Degree_Female_PG_Data_Preparation_df in Degree_Female_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(Degree_Female_PG_Data_Preparation_df)

                        #DEO Degree Female Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias','Year-Month'])
                        
                        if "DegreeFEMALE" in Degree_Female_PG_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Personal Care"
                            df["Category"] = "Deodorant"
                            df["Sub category"] = "Degree"
                            df["Brand"] = "PC Deo Degree Female"
                            df["Total Brand"] = "PC Deo Degree"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                coupon_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_filter, 'Platform'] = df.loc[coupon_filter, 'Product Line']
                                df.loc[coupon_filter, 'Product Line'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns:
                                Non_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Non_Media_filter, 'Channel/Daypart'] = df.loc[Non_Media_filter, 'Product Line']
                                df.loc[Non_Media_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                Owned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Owned_Media_filter, 'Platform'] = df.loc[Owned_Media_filter, 'Product Line']
                                df.loc[Owned_Media_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Trade Promo"
                                df.loc[trade_promo_filter, 'Channel/Daypart'] = (
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns and 'Daypart' not in df.columns:
                                df['Daypart'] = None
                            if 'Master Channel' in df.columns:
                                Master_Channel_TV_filter = df['Master Channel'] == "TV"
                                df.loc[Master_Channel_TV_filter, 'Daypart'] = df.loc[Master_Channel_TV_filter, 'Channel/Daypart']
                                df.loc[Master_Channel_TV_filter, 'Channel/Daypart'] = "TV"

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Web Traffic"
                                df.loc[Product_line_TV_filter, 'Platform'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Shopper"
                                df.loc[Product_line_TV_filter, 'Platform'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None  

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Others"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None  

                            if 'Platform' in df.columns and 'Master Channel' in df.columns:
                                df['Platform'] = df['Platform'].replace('Facebook', 'Facebook page Post')
                                df['Platform'] = df['Platform'].replace('Instagram', 'Instagram page Post')
                                df['Platform'] = df['Platform'].replace('Twitter', 'Twitter page Post')                                         
                                df['Platform'] = df['Platform'].replace('Web Traffic', 'Web_Analytics')
                                df['Master Channel'] = df['Master Channel'].replace('Baseline', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Sessions', ' ')
                                    
                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel/Daypart'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Seasonality"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel/Daypart'] = "Seasonality Monthly"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Coupon"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Platform'] = df.loc[trade_promo_filter, 'Master Channel']
                                df.loc[trade_promo_filter, 'Master Channel'] = None
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "PW"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                
                        df['Normalized Cost'] = (df['Cost']/2)
                        df['Normalized Impression'] = (df['Impression']/2)
                        df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df[['Influencer Say','Color Code','Data Through']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel", "Platform", 
                            "Influencer Say", "Color Code", "Audience", "Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                        st.write(f"Processed DataFrame for: {Degree_Female_PG_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')

                        csv_data = convert_df_to_csv(df)

                        st.download_button(
                            label="Download DEO DEGREE FEMALE Playground Processed CSV",
                            data=csv_data,
                            file_name="DEO_DEGREE_FEMALE_Playground_Processed_Data.csv",
                            mime='text/csv'
                        )
                    except Exception as e:
                        st.error(f"Error processing {Degree_Female_PG_Data_Preparation_df.name}: {e}")

        if selected == "PC DEO DEGREE MALE":
            st.subheader("PC DEO DEGREE MALE") 
            Degree_Male_PG_Data_Preparation = st.file_uploader("Upload your Deo Degree Male RROI file", type=["xlsx"], accept_multiple_files=True)
            if Degree_Male_PG_Data_Preparation:
                for Degree_Male_PG_Data_Preparation_df in Degree_Male_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(Degree_Male_PG_Data_Preparation_df)

                        #DEO Degree Male Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias','Year-Month'])
                        
                        if "DegreeMALE" in Degree_Male_PG_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Personal Care"
                            df["Category"] = "Deodorant"
                            df["Sub category"] = "Degree"
                            df["Brand"] = "PC Deo Degree Male"
                            df["Total Brand"] = "PC Deo Degree"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                coupon_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_filter, 'Platform'] = df.loc[coupon_filter, 'Product Line']
                                df.loc[coupon_filter, 'Product Line'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns:
                                Non_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Non_Media_filter, 'Channel/Daypart'] = df.loc[Non_Media_filter, 'Product Line']
                                df.loc[Non_Media_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                Owned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Owned_Media_filter, 'Platform'] = df.loc[Owned_Media_filter, 'Product Line']
                                df.loc[Owned_Media_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Trade Promo"
                                df.loc[trade_promo_filter, 'Channel/Daypart'] = (
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns and 'Daypart' not in df.columns:
                                df['Daypart'] = None
                            if 'Master Channel' in df.columns:
                                Master_Channel_TV_filter = df['Master Channel'] == "TV"
                                df.loc[Master_Channel_TV_filter, 'Daypart'] = df.loc[Master_Channel_TV_filter, 'Channel/Daypart']
                                df.loc[Master_Channel_TV_filter, 'Channel/Daypart'] = "TV"

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Web Traffic"
                                df.loc[Product_line_TV_filter, 'Platform'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Shopper"
                                df.loc[Product_line_TV_filter, 'Platform'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None  

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Others"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None  

                            if 'Platform' in df.columns and 'Master Channel' in df.columns:
                                df['Platform'] = df['Platform'].replace('Facebook', 'Facebook page Post')
                                df['Platform'] = df['Platform'].replace('Instagram', 'Instagram page Post')
                                df['Platform'] = df['Platform'].replace('Twitter', 'Twitter page Post')                                         
                                df['Platform'] = df['Platform'].replace('Web Traffic', 'Web_Analytics')
                                df['Master Channel'] = df['Master Channel'].replace('Baseline', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Sessions', ' ')
                                    
                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel/Daypart'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Seasonality"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel/Daypart'] = "Seasonality Monthly"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Coupon"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Platform'] = df.loc[trade_promo_filter, 'Master Channel']
                                df.loc[trade_promo_filter, 'Master Channel'] = None
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "PW"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                
                        df['Normalized Cost'] = (df['Cost']/2)
                        df['Normalized Impression'] = (df['Impression']/2)
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df[['Influencer Say','Color Code','Data Through']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel", "Platform", 
                            "Influencer Say", "Color Code", "Audience", "Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                        st.write(f"Processed DataFrame for: {Degree_Male_PG_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')

                        csv_data = convert_df_to_csv(df)

                        st.download_button(
                            label="DEO DEGREE MALE Download Playground Processed CSV",
                            data=csv_data,
                            file_name="DEO_DEGREE_MALE_Playground_Processed_Data.csv",
                            mime='text/csv'
                        )
                    except Exception as e:
                        st.error(f"Error processing {Degree_Male_PG_Data_Preparation_df.name}: {e}")
       
        if selected == "PC PW DMC":
            st.subheader("PC PW DMC")  
            PW_DMC_PG_Data_Preparation = st.file_uploader("Upload your PW DMC RROI file", type=["xlsx"], accept_multiple_files=True)
            if PW_DMC_PG_Data_Preparation:
                for PW_DMC_Data_Preparation_df in PW_DMC_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(PW_DMC_Data_Preparation_df)

                        #DEO Axe Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias','Year-Month'])
                        
                        if "PW_DMC" in PW_DMC_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Personal Care"
                            df["Category"] = "Skin Cleansing"
                            df["Sub category"] = "PW DMC"
                            df["Brand"] = "PC PW DMC"
                            df["Total Brand"] = "PC PW DMC"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Product Line']
                                df.loc[Earned_Media_filter, 'Product Line'] = None  

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns:
                                Non_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Non_Media_filter, 'Channel/Daypart'] = df.loc[Non_Media_filter, 'Product Line']
                                df.loc[Non_Media_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                Owned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Owned_Media_filter, 'Platform'] = df.loc[Owned_Media_filter, 'Product Line']
                                df.loc[Owned_Media_filter, 'Product Line'] = None


                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                df['Platform'] = df['Platform'].replace('Facebook', 'Facebook page Post')
                                df['Platform'] = df['Platform'].replace('Instagram', 'Instagram page Post')
                                df['Platform'] = df['Platform'].replace('Twitter', 'Twitter page Post')                                         
                                df['Platform'] = df['Platform'].replace('Web Traffic', 'Web_Analytics')
                                df['Master Channel'] = df['Master Channel'].replace('Baseline', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Recipients', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Sessions', ' ')

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Shopper', 'Coupon')
                                coupon_Shopper_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_Shopper_filter, 'Platform'] = df.loc[coupon_Shopper_filter, 'Product Line']
                                df.loc[coupon_Shopper_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Trade Promo"
                                df.loc[trade_promo_filter, 'Channel/Daypart'] = (
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Master Channel'] == "Earned Media"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Master Channel'] = None 
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Master Channel'] == "Paid Media"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Master Channel'] = None 
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Masterbrand"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Halo"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None 


                            if 'Master Channel' in df.columns and 'Daypart' not in df.columns:
                                df['Daypart'] = None
                            if 'Master Channel' in df.columns:
                                Master_Channel_TV_filter = df['Master Channel'] == "TV"
                                df.loc[Master_Channel_TV_filter, 'Daypart'] = df.loc[Master_Channel_TV_filter, 'Channel/Daypart']
                                df.loc[Master_Channel_TV_filter, 'Channel/Daypart'] = "TV" 

                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel/Daypart'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None


                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None 

                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Seasonality"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel/Daypart'] = "Seasonality Monthly"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Master Channel'] == "Coupon"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Master Channel'] = None
                        

                        df['Normalized Cost'] = (df['Cost'])
                        df['Normalized Impression'] = (df['Impression'])
                        df['Daypart'] = df['Daypart'].replace('TV', '')
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df[['Influencer Say','Color Code','Data Through']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel/Daypart", "Platform", 
                            "Influencer Say", "Color Code", "Audience", "Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                                                # Display the processed DataFrame
                        st.write(f"Processed DataFrame for: {PW_DMC_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')

                        csv_data = convert_df_to_csv(df)

                        st.download_button(
                            label="PW DMC Download Playground Processed CSV",
                            data=csv_data,
                            file_name="PW_DMC Playground_Processed_Data.csv",
                            mime='text/csv'
                        )
                    except Exception as e:
                        st.error(f"Error processing {PW_DMC_Data_Preparation_df.name}: {e}")

        if selected == "PC DEO DMC":
            st.subheader("PC DEO DMC")
            Deo_DMC_PG_Data_Preparation = st.file_uploader("Upload your DEO DMC RROI file", type=["xlsx"], accept_multiple_files=True)
            if Deo_DMC_PG_Data_Preparation:
                for Deo_DMC_Data_Preparation_df in Deo_DMC_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(Deo_DMC_Data_Preparation_df)

                        #DEO Axe Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias','Year-Month'])
                        
                        if "DEO_DMC" in Deo_DMC_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Personal Care"
                            df["Category"] = "Deodorant"
                            df["Sub category"] = "DEO DMC"
                            df["Brand"] = "PC DEO DMC"
                            df["Total Brand"] = "PC DEO DMC"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Product Line']
                                df.loc[Earned_Media_filter, 'Product Line'] = None  

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns:
                                Non_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Non_Media_filter, 'Channel/Daypart'] = df.loc[Non_Media_filter, 'Product Line']
                                df.loc[Non_Media_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                Owned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Owned_Media_filter, 'Platform'] = df.loc[Owned_Media_filter, 'Product Line']
                                df.loc[Owned_Media_filter, 'Product Line'] = None


                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                df['Platform'] = df['Platform'].replace('Facebook', 'Facebook page Post')
                                df['Platform'] = df['Platform'].replace('Instagram', 'Instagram page Post')
                                df['Platform'] = df['Platform'].replace('Twitter', 'Twitter page Post')                                         
                                df['Platform'] = df['Platform'].replace('Web Traffic', 'Web_Analytics')
                                df['Master Channel'] = df['Master Channel'].replace('Baseline', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Recipients', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Sessions', ' ')

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Shopper', 'Coupon')
                                coupon_Shopper_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_Shopper_filter, 'Platform'] = df.loc[coupon_Shopper_filter, 'Product Line']
                                df.loc[coupon_Shopper_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Trade Promo"
                                df.loc[trade_promo_filter, 'Channel/Daypart'] = (
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Master Channel'] == "Earned Media"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Master Channel'] = None 
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Master Channel'] == "Paid Media"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Master Channel'] = None 
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Masterbrand"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Halo"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None 


                            if 'Master Channel' in df.columns and 'Daypart' not in df.columns:
                                df['Daypart'] = None
                            if 'Master Channel' in df.columns:
                                Master_Channel_TV_filter = df['Master Channel'] == "TV"
                                df.loc[Master_Channel_TV_filter, 'Daypart'] = df.loc[Master_Channel_TV_filter, 'Channel/Daypart']
                                df.loc[Master_Channel_TV_filter, 'Channel/Daypart'] = "TV" 

                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel/Daypart'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None


                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel/Daypart'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None 

                            if 'Channel/Daypart' in df.columns:
                                Product_line_TV_filter = df['Channel/Daypart'] == "Seasonality"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel/Daypart'] = "Seasonality Monthly"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Master Channel'] == "Coupon"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Master Channel'] = None
                        

                        df['Normalized Cost'] = (df['Cost'])
                        df['Normalized Impression'] = (df['Impression'])
                        df['Daypart'] = df['Daypart'].replace('TV', '')
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df[['Influencer Say','Color Code','Data Through']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel/Daypart", "Platform", 
                            "Influencer Say", "Color Code", "Audience", "Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                                                # Display the processed DataFrame
                        st.write(f"Processed DataFrame for: {Deo_DMC_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')

                        csv_data = convert_df_to_csv(df)

                        st.download_button(
                            label="DEO DMC Download Playground Processed CSV",
                            data=csv_data,
                            file_name="DEO_DMC Playground_Processed_Data.csv",
                            mime='text/csv'
                        )
                    except Exception as e:
                        st.error(f"Error processing {Deo_DMC_Data_Preparation_df.name}: {e}")

        if selected == "PC DEO DOVE":
            st.subheader("PC DEO DOVE")
            Deo_DOVE_PG_Data_Preparation = st.file_uploader("Upload your DEO DOVE RROI file", type=["xlsx"], accept_multiple_files=True)
            if Deo_DOVE_PG_Data_Preparation:
                for Deo_DOVE_Data_Preparation_df in Deo_DOVE_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(Deo_DOVE_Data_Preparation_df)

                        #DEO DOVE Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias','Year-Month'])
                        
                        if "DEO_Dove" in Deo_DOVE_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Personal Care"
                            df["Category"] = "Deodorant"
                            df["Sub category"] = "DEO DOVE"
                            df["Brand"] = "PC DEO DOVE"
                            df["Total Brand"] = "PC DEO DOVE"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel'] = df.loc[Earned_Media_filter, 'Product Line']
                                df.loc[Earned_Media_filter, 'Product Line'] = None  

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel' in df.columns:
                                Non_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Non_Media_filter, 'Channel'] = df.loc[Non_Media_filter, 'Product Line']
                                df.loc[Non_Media_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                Owned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Owned_Media_filter, 'Platform'] = df.loc[Owned_Media_filter, 'Product Line']
                                df.loc[Owned_Media_filter, 'Product Line'] = None


                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                df['Platform'] = df['Platform'].replace('Facebook', 'Facebook page Post')
                                df['Platform'] = df['Platform'].replace('Instagram', 'Instagram page Post')
                                df['Platform'] = df['Platform'].replace('Twitter', 'Twitter page Post')                                         
                                df['Platform'] = df['Platform'].replace('Web Traffic', 'Web_Analytics')
                                df['Master Channel'] = df['Master Channel'].replace('Baseline', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Recipients', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Sessions', ' ')

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Shopper', 'Coupon')
                                coupon_Shopper_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_Shopper_filter, 'Platform'] = df.loc[coupon_Shopper_filter, 'Product Line']
                                df.loc[coupon_Shopper_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Trade Promo"
                                df.loc[trade_promo_filter, 'Channel'] = (
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Haircare F"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "PW F"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Skincleansing"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Cinema"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Print"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "OOH"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "TV"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None 
                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Commerce & Search"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Master Channel'] 
                                df.loc[trade_promo_filter, 'Master Channel'] = "Commerce & Search"
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Digital"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Master Channel'] 
                                df.loc[trade_promo_filter, 'Master Channel'] = "Commerce & Search"
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Channel' in df.columns:
                                Product_line_TV_filter = df['Channel'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None      

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "Influencer Retail")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "Influencer Retail")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Channel' in df.columns:
                                Product_line_TV_filter = df['Channel'] == "Seasonality"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel'] = "Seasonality Monthly"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Master Channel' in df.columns and 'Media Type' in df.columns and 'Daypart' in df.columns:
                                Product_line_TV_filter = (
                                    (df['Master Channel'] == "TV") &
                                    (df['Media Type'] == "Paid Media") &
                                    (df['Channel'] != "TV")
                                )
                                df.loc[Product_line_TV_filter, 'Daypart'] = df.loc[Product_line_TV_filter, 'Channel']
                                df.loc[Product_line_TV_filter, 'Channel'] = "TV"

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Dove"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Superbowl"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None

                        df['Normalized Cost'] = (df['Cost'])
                        df['Normalized Impression'] = (df['Impression'])
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df[['Influencer Say','Color Code','Data Through']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel", "Platform", 
                            "Influencer Say", "Color Code", "Audience", "Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        df = df[df['Daypart'] != 'TV']
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                                                # Display the processed DataFrame
                        st.write(f"Processed DataFrame for: {Deo_DOVE_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')

                        csv_data = convert_df_to_csv(df)

                        st.download_button(
                            label="DEO DOVE Download Playground Processed CSV",
                            data=csv_data,
                            file_name="DEO_DOVE Playground_Processed_Data.csv",
                            mime='text/csv'
                        )
                    except Exception as e:
                        st.error(f"Error processing {Deo_DOVE_Data_Preparation_df.name}: {e}")

        if selected == "PC PW DOVE BAR":
            st.subheader("PC PW DOVE BAR")
            PW_DOVE_BAR_PG_Data_Preparation = st.file_uploader("Upload your PW DOVE BAR RROI file", type=["xlsx"], accept_multiple_files=True)
            if PW_DOVE_BAR_PG_Data_Preparation:
                for PW_DOVE_BAR_Data_Preparation_df in PW_DOVE_BAR_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(PW_DOVE_BAR_Data_Preparation_df)

                        #PW_DOVE_BAR Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias','Year-Month'])
                        
                        if "PW_DoveBAR" in PW_DOVE_BAR_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Personal Care"
                            df["Category"] = "Skin Cleansing"
                            df["Sub category"] = "Bar"
                            df["Brand"] = "PC Dove Bar"
                            df["Total Brand"] = "PC PW Dove"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel'] = df.loc[Earned_Media_filter, 'Product Line']
                                df.loc[Earned_Media_filter, 'Product Line'] = None  

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel' in df.columns:
                                Non_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Non_Media_filter, 'Channel'] = df.loc[Non_Media_filter, 'Product Line']
                                df.loc[Non_Media_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                Owned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Owned_Media_filter, 'Platform'] = df.loc[Owned_Media_filter, 'Product Line']
                                df.loc[Owned_Media_filter, 'Product Line'] = None


                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                df['Platform'] = df['Platform'].replace('Facebook', 'Facebook page Post')
                                df['Platform'] = df['Platform'].replace('Instagram', 'Instagram page Post')
                                df['Platform'] = df['Platform'].replace('Twitter', 'Twitter page Post')                                         
                                df['Platform'] = df['Platform'].replace('Web Traffic', 'Web_Analytics')
                                df['Master Channel'] = df['Master Channel'].replace('Baseline', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Recipients', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Sessions', ' ')

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Shopper', 'Coupon')
                                coupon_Shopper_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_Shopper_filter, 'Platform'] = df.loc[coupon_Shopper_filter, 'Product Line']
                                df.loc[coupon_Shopper_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Trade Promo"
                                df.loc[trade_promo_filter, 'Channel'] = (
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Haircare F"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Deo F"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Print"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "OOH"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "TV"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Commerce & Search"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Master Channel'] 
                                df.loc[trade_promo_filter, 'Master Channel'] = "Commerce & Search"
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Digital"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Master Channel'] 
                                df.loc[trade_promo_filter, 'Master Channel'] = "Commerce & Search"
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns and 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None
                                df.loc[Product_line_TV_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None      

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "Influencer Retail")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "Influencer Retail")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns and 'Master Channel' in df.columns and 'Channel' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Seasonality"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel'] = "Seasonality Monthly"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None
                                df.loc[Product_line_TV_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns and 'Media Type' in df.columns and 'Daypart' in df.columns:
                                Product_line_TV_filter = (
                                    (df['Master Channel'] == "TV") &
                                    (df['Media Type'] == "Paid Media") &
                                    (df['Channel'] != "TV")
                                )
                                df.loc[Product_line_TV_filter, 'Daypart'] = df.loc[Product_line_TV_filter, 'Channel']
                                df.loc[Product_line_TV_filter, 'Channel'] = "TV"

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Dove"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Superbowl"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Channel' in df.columns:
                                Product_line_TV_filter = df['Channel'] == "Seasonality"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel'] = "Seasonality Monthly"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Channel' in df.columns:
                                Product_line_TV_filter = df['Channel'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                        df['Normalized Cost'] = (df['Cost']/2)
                        df['Normalized Impression'] = (df['Impression']/2)
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df[['Influencer Say','Color Code','Data Through']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel", "Platform", 
                            "Influencer Say", "Color Code", "Audience", "Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        df = df[df['Daypart'] != 'TV']
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                                                # Display the processed DataFrame
                        st.write(f"Processed DataFrame for: {PW_DOVE_BAR_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')

                        csv_data = convert_df_to_csv(df)

                        st.download_button(
                            label="PW DOVE BAR Download Playground Processed CSV",
                            data=csv_data,
                            file_name="PW_DOVE_BAR Playground_Processed_Data.csv",
                            mime='text/csv'
                        )
                    except Exception as e:
                        st.error(f"Error processing {PW_DOVE_BAR_Data_Preparation_df.name}: {e}")

        if selected == "PC PW DOVE BW":
            st.subheader("PC PW DOVE BW")
            PW_DOVE_BW_PG_Data_Preparation = st.file_uploader("Upload your PW DOVE BW RROI file", type=["xlsx"], accept_multiple_files=True)
            if PW_DOVE_BW_PG_Data_Preparation:
                for PW_DOVE_BW_Data_Preparation_df in PW_DOVE_BW_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(PW_DOVE_BW_Data_Preparation_df)

                        #PW_DOVE_BW Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias','Year-Month'])
                        
                        if "PW_DoveBW" in PW_DOVE_BW_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Personal Care"
                            df["Category"] = "Skin Cleansing"
                            df["Sub category"] = "BW"
                            df["Brand"] = "PC Dove BW"
                            df["Total Brand"] = "PC PW Dove"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel'] = df.loc[Earned_Media_filter, 'Product Line']
                                df.loc[Earned_Media_filter, 'Product Line'] = None  

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel' in df.columns:
                                Non_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Non_Media_filter, 'Channel'] = df.loc[Non_Media_filter, 'Product Line']
                                df.loc[Non_Media_filter, 'Product Line'] = None 

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                Owned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Owned_Media_filter, 'Platform'] = df.loc[Owned_Media_filter, 'Product Line']
                                df.loc[Owned_Media_filter, 'Product Line'] = None

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                df['Platform'] = df['Platform'].replace('Facebook', 'Facebook page Post')
                                df['Platform'] = df['Platform'].replace('Instagram', 'Instagram page Post')
                                df['Platform'] = df['Platform'].replace('Twitter', 'Twitter page Post')                                         
                                df['Platform'] = df['Platform'].replace('Web Traffic', 'Web_Analytics')
                                df['Master Channel'] = df['Master Channel'].replace('Baseline', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Recipients', ' ')
                                df['Master Channel'] = df['Master Channel'].replace('Sessions', ' ')

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Shopper', 'Coupon')
                                coupon_Shopper_filter = df['Media Type'] == "Coupon"
                                df.loc[coupon_Shopper_filter, 'Platform'] = df.loc[coupon_Shopper_filter, 'Product Line']
                                df.loc[coupon_Shopper_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                trade_promo_filter = df['Media Type'] == "Trade Promo"
                                df.loc[trade_promo_filter, 'Channel'] = (
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Master Channel'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None
                                df.loc[trade_promo_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Haircare F"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Deo F"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None  

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Deo"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Haircare"
                                df.loc[trade_promo_filter, 'Media Type'] = (
                                    df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                    df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Print"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "OOH"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None   

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "TV"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Product Line'] 
                                df.loc[trade_promo_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Commerce & Search"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Master Channel'] 
                                df.loc[trade_promo_filter, 'Master Channel'] = "Commerce & Search"
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Product Line' in df.columns:
                                trade_promo_filter = df['Product Line'] == "Digital"
                                df.loc[trade_promo_filter, 'Channel'] = df.loc[trade_promo_filter, 'Master Channel'] 
                                df.loc[trade_promo_filter, 'Master Channel'] = "Commerce & Search"
                                df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns and 'Product Line' in df.columns:
                                Product_line_TV_filter = df['Product Line'] == "Trends"
                                df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel'] = "Trends Category"
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None
                                df.loc[Product_line_TV_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None 

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "PR")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "Influencer")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None      

                            if 'Master Channel' in df.columns:
                                Product_line_TV_filter = (df['Master Channel'] == "Influencer Retail")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Master Channel']
                                df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Product Line' in df.columns:
                                Product_line_TV_filter = (df['Product Line'] == "Influencer Retail")
                                df.loc[Product_line_TV_filter, 'Channel'] = df.loc[Product_line_TV_filter, 'Product Line']
                                df.loc[Product_line_TV_filter, 'Product Line'] = None 

                            if 'Product Line' in df.columns and 'Master Channel' in df.columns and 'Channel' in df.columns:
                                    Product_line_TV_filter = df['Product Line'] == "Seasonality"
                                    df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel'] = "Seasonality Monthly"
                                    df.loc[Product_line_TV_filter, 'Master Channel'] = None
                                    df.loc[Product_line_TV_filter, 'Product Line'] = None

                            if 'Master Channel' in df.columns and 'Media Type' in df.columns and 'Daypart' in df.columns:
                                    Product_line_TV_filter = (
                                        (df['Master Channel'] == "TV") &
                                        (df['Media Type'] == "Paid Media") &
                                        (df['Channel'] != "TV")
                                    )
                                    df.loc[Product_line_TV_filter, 'Daypart'] = df.loc[Product_line_TV_filter, 'Channel']
                                    df.loc[Product_line_TV_filter, 'Channel'] = "TV"

                            if 'Product Line' in df.columns:
                                    trade_promo_filter = df['Product Line'] == "Dove"
                                    df.loc[trade_promo_filter, 'Media Type'] = (
                                        df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                        df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                    df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Product Line' in df.columns:
                                    trade_promo_filter = df['Product Line'] == "Superbowl"
                                    df.loc[trade_promo_filter, 'Media Type'] = (
                                        df.loc[trade_promo_filter, 'Media Type'].astype(str) + "_" + 
                                        df.loc[trade_promo_filter, 'Product Line'].astype(str))
                                    df.loc[trade_promo_filter, 'Product Line'] = None

                            if 'Channel' in df.columns:
                                    Product_line_TV_filter = df['Channel'] == "Seasonality"
                                    df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Monthly'), 'Channel'] = "Seasonality Monthly"
                                    df.loc[Product_line_TV_filter, 'Master Channel'] = None

                            if 'Channel' in df.columns:
                                    Product_line_TV_filter = df['Channel'] == "Trends"
                                    df.loc[Product_line_TV_filter & (df['Master Channel'] == 'Category'), 'Channel'] = "Trends Category"
                                    df.loc[Product_line_TV_filter, 'Master Channel'] = None    
                        
                        # Convert 'Cost' and 'Impression' columns to numeric, replacing non-numeric values with NaN
                        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
                        df['Impression'] = pd.to_numeric(df['Impression'], errors='coerce')
                        
                        # Handle missing values if necessary (e.g., replace NaN with 0)
                        df['Cost'] = df['Cost'].fillna(0)
                        df['Impression'] = df['Impression'].fillna(0)

                        # Perform the division to calculate normalized values
                        df['Normalized Cost'] = df['Cost'] / 2
                        df['Normalized Impression'] = df['Impression'] / 2
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df[['Influencer Say','Color Code','Data Through']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel", "Platform", 
                            "Influencer Say", "Color Code", "Audience", "Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        df = df[df['Daypart'] != 'TV']
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                                                # Display the processed DataFrame
                        st.write(f"Processed DataFrame for: {PW_DOVE_BW_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')
                        csv_data = convert_df_to_csv(df)
                        st.download_button(
                            label="PW DOVE BW Download Playground Processed CSV",
                            data=csv_data,
                            file_name="PW_DOVE_BW_Playground_Processed_Data.csv",
                            mime='text/csv'
                        )
                    except Exception as e:
                        st.error(f"Error processing {PW_DOVE_BAR_Data_Preparation_df.name}: {e}")

        
        if selected == "BnW HAIR Shea Moisture":
            st.subheader("BnW HAIR Shea Moisture    ")
            BnW_HAIR_Shea_Moisture_PG_Data_Preparation = st.file_uploader("Upload your BnW HAIR Shea Moisture' RROI file", type=["xlsx"], accept_multiple_files=True)
            if BnW_HAIR_Shea_Moisture_PG_Data_Preparation:
                for BnW_HAIR_Shea_Moisture_PG_Data_Preparation_df in BnW_HAIR_Shea_Moisture_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(BnW_HAIR_Shea_Moisture_PG_Data_Preparation_df)

                        #PW_DOVE_BW Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Modified Date','Model Scope Alias'])
                        
                        if "HAIR_SheaMoisture" in BnW_HAIR_Shea_Moisture_PG_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Beauty and Wellbeing"
                            df["Category"] = "Haircare"
                            df["Sub category"] = "Haircare"
                            df["Brand"] = "BnW HAIR Shea Moisture"
                            df["Total Brand"] = "BnW HAIR Shea Moisture"

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None  

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns and 'Audience' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Baseline"
                                df.loc[Earned_Media_filter, 'Product Line'] = None 
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = None
                                df.loc[Earned_Media_filter, 'Platform'] = None
                                df.loc[Earned_Media_filter, 'Audience'] = None

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Coupon"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None    

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Promo', 'Trade Promo')
                                coupon_Shopper_filter = df['Media Type'] == "Trade Promo"
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = None

                        # Convert 'Cost' and 'Impression' columns to numeric, replacing non-numeric values with NaN
                        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
                        df['Impression'] = pd.to_numeric(df['Impression'], errors='coerce')
                        
                        # Handle missing values if necessary (e.g., replace NaN with 0)
                        df['Cost'] = df['Cost'].fillna(0)
                        df['Impression'] = df['Impression'].fillna(0)

                        # Perform the division to calculate normalized values
                        df['Normalized Cost'] = df['Cost']
                        df['Normalized Impression'] = df['Impression']
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df['Platform'] = df['Platform'].replace("Prism", "Shopper")
                        df['Channel/Daypart'] = df['Channel/Daypart'].replace("Percentage Promo", "Percentage Sales")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        df[['Data Through','Daypart']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel/Daypart", "Platform", 
                            "Influencer Say", "Color Code", "Audience","Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                        st.write(f"Processed DataFrame for: {BnW_HAIR_Shea_Moisture_PG_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')
                        csv_data = convert_df_to_csv(df)
                        st.download_button(
                            label="BnW HAIR Shea Moisture Download Playground Processed CSV",
                            data=csv_data,
                            file_name="BnW_HAIR_Shea_Moisture_Processed_Data.csv",
                            mime='text/csv'
                        )

                    except Exception as e:
                        st.error(f"Error processing {BnW_HAIR_Shea_Moisture_PG_Data_Preparation_df.name}: {e}")
        if selected == "BnW HAIR Tresemme":
            st.subheader("BnW HAIR Tresemme")
            BnW_HAIR_Tresemme_PG_Data_Preparation = st.file_uploader("Upload your BnW HAIR Tresemme RROI file", type=["xlsx"], accept_multiple_files=True)
            if BnW_HAIR_Tresemme_PG_Data_Preparation:
                for BnW_HAIR_Tresemme_PG_Data_Preparation_df in BnW_HAIR_Tresemme_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(BnW_HAIR_Tresemme_PG_Data_Preparation_df)

                        #PW_DOVE_BW Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Modified Date','Model Scope Alias'])
                        
                        if "HAIR_Tresemme" in BnW_HAIR_Tresemme_PG_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Beauty and Wellbeing"
                            df["Category"] = "Haircare"
                            df["Sub category"] = "Haircare"
                            df["Brand"] = "BnW HAIR Tresemme"
                            df["Total Brand"] = "BnW HAIR Tresemme"

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None  

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns and 'Audience' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Baseline"
                                df.loc[Earned_Media_filter, 'Product Line'] = None 
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = None
                                df.loc[Earned_Media_filter, 'Platform'] = None
                                df.loc[Earned_Media_filter, 'Audience'] = None

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Coupon"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None    

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Promo', 'Trade Promo')
                                coupon_Shopper_filter = df['Media Type'] == "Trade Promo"
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = None
                            df[['Data Through','Daypart']] = ''
                            if 'Master Channel' in df.columns and 'Daypart' in df.columns and 'Channel/Daypart' in df.columns:
                                coupon_Shopper_filter = df['Master Channel'] == "TV"
                                df.loc[coupon_Shopper_filter, 'Daypart'] = df.loc[coupon_Shopper_filter, 'Channel/Daypart']
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = None    

                        # Convert 'Cost' and 'Impression' columns to numeric, replacing non-numeric values with NaN
                        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
                        df['Impression'] = pd.to_numeric(df['Impression'], errors='coerce')
                        
                        # Handle missing values if necessary (e.g., replace NaN with 0)
                        df['Cost'] = df['Cost'].fillna(0)
                        df['Impression'] = df['Impression'].fillna(0)

                        # Perform the division to calculate normalized values
                        df['Normalized Cost'] = df['Cost']
                        df['Normalized Impression'] = df['Impression']
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df['Platform'] = df['Platform'].replace("Prism", "Shopper")
                        df['Channel/Daypart'] = df['Channel/Daypart'].replace("Percentage Promo", "Percentage Sales")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        # df[['Data Through','Daypart']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel/Daypart", "Platform", 
                            "Influencer Say", "Color Code", "Audience","Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                        st.write(f"Processed DataFrame for: {BnW_HAIR_Tresemme_PG_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')
                        csv_data = convert_df_to_csv(df)
                        st.download_button(
                            label="BnW HAIR Tresemme Download Playground Processed CSV",
                            data=csv_data,
                            file_name="BnW_HAIR_Tresemme_Processed_Data.csv",
                            mime='text/csv'
                        )

                    except Exception as e:
                        st.error(f"Error processing {BnW_HAIR_Tresemme_PG_Data_Preparation_df.name}: {e}")
        
        if selected == "BnW SKIN Vaseline":
            st.subheader("BnW SKIN Vaseline")
            BnW_SKIN_Vaseline_PG_Data_Preparation = st.file_uploader("Upload your BnW SKIN_Vaseline RROI file", type=["xlsx"], accept_multiple_files=True)
            if BnW_SKIN_Vaseline_PG_Data_Preparation:
                for BnW_SKIN_Vaseline_PG_Data_Preparation_df in BnW_SKIN_Vaseline_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(BnW_SKIN_Vaseline_PG_Data_Preparation_df)

                        #PW_DOVE_BW Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Modified Date','Model Scope Alias'])
                        
                        if "SKIN_Vaseline" in BnW_SKIN_Vaseline_PG_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Beauty and Wellbeing"
                            df["Category"] = "Skincare"
                            df["Sub category"] = "Skincare"
                            df["Brand"] = "BnW SKIN Vaseline"
                            df["Total Brand"] = "BnW SKIN Vaseline"

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None  

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns and 'Audience' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Baseline"
                                df.loc[Earned_Media_filter, 'Product Line'] = None 
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = None
                                df.loc[Earned_Media_filter, 'Platform'] = None
                                df.loc[Earned_Media_filter, 'Audience'] = None

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Coupon"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None    

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Promo', 'Trade Promo')
                                coupon_Shopper_filter = df['Media Type'] == "Trade Promo"
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = None

                            df[['Data Through','Daypart']] = ''
                            if 'Master Channel' in df.columns and 'Daypart' in df.columns and 'Channel/Daypart' in df.columns:
                                coupon_Shopper_filter = df['Master Channel'] == "TV"
                                df.loc[coupon_Shopper_filter, 'Daypart'] = df.loc[coupon_Shopper_filter, 'Channel/Daypart']
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = None  

                            if 'Master Channel' in df.columns and 'Channel/Daypart' in df.columns:
                                coupon_Shopper_filter = df['Media Type'] == "Temperature"
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Media Type']
                                df.loc[coupon_Shopper_filter, 'Media Type'] = "Non Media"       


                        # Convert 'Cost' and 'Impression' columns to numeric, replacing non-numeric values with NaN
                        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
                        df['Impression'] = pd.to_numeric(df['Impression'], errors='coerce')
                        
                        # Handle missing values if necessary (e.g., replace NaN with 0)
                        df['Cost'] = df['Cost'].fillna(0)
                        df['Impression'] = df['Impression'].fillna(0)

                        # Perform the division to calculate normalized values
                        df['Normalized Cost'] = df['Cost']
                        df['Normalized Impression'] = df['Impression']
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df['Platform'] = df['Platform'].replace("Prism", "Shopper")
                        df['Channel/Daypart'] = df['Channel/Daypart'].replace("Percentage Promo", "Percentage Sales")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        # df[['Data Through','Daypart']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel/Daypart", "Platform", 
                            "Influencer Say", "Color Code", "Audience","Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                        st.write(f"Processed DataFrame for: {BnW_SKIN_Vaseline_PG_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')
                        csv_data = convert_df_to_csv(df)
                        st.download_button(
                            label="BnW SKIN Vaseline Download Playground Processed CSV",
                            data=csv_data,
                            file_name="BnW_SKIN_Vaseline_Processed_Data.csv",
                            mime='text/csv'
                        )

                    except Exception as e:
                        st.error(f"Error processing {BnW_SKIN_Vaseline_PG_Data_Preparation_df.name}: {e}")

        if selected == "BnW HAIR Nexxus":
            st.subheader("BnW HAIR Nexxus")
            BnW_HAIR_Nexxus_PG_Data_Preparation = st.file_uploader("Upload your BnW HAIR_Nexxus RROI file", type=["xlsx"], accept_multiple_files=True)
            if BnW_HAIR_Nexxus_PG_Data_Preparation:
                for BnW_HAIR_Nexxus_PG_Data_Preparation_df in BnW_HAIR_Nexxus_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(BnW_HAIR_Nexxus_PG_Data_Preparation_df)

                        #PW_DOVE_BW Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Modified Date','Model Scope Alias'])
                        
                        if "HAIR_Nexxus" in BnW_HAIR_Nexxus_PG_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Beauty and Wellbeing"
                            df["Category"] = "Haircare"
                            df["Sub category"] = "Haircare"
                            df["Brand"] = "BnW HAIR Nexxus"
                            df["Total Brand"] = "BnW HAIR Nexxus"

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None  

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns and 'Audience' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Baseline"
                                df.loc[Earned_Media_filter, 'Product Line'] = None 
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = None
                                df.loc[Earned_Media_filter, 'Platform'] = None
                                df.loc[Earned_Media_filter, 'Audience'] = None

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Coupon"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None    

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Promo', 'Trade Promo')
                                coupon_Shopper_filter = df['Media Type'] == "Trade Promo"
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = None

                        df[['Data Through','Daypart']] = ''
                            # if 'Master Channel' in df.columns and 'Daypart' in df.columns and 'Channel/Daypart' in df.columns:
                            #     coupon_Shopper_filter = df['Master Channel'] == "TV"
                            #     df.loc[coupon_Shopper_filter, 'Daypart'] = df.loc[coupon_Shopper_filter, 'Channel/Daypart']
                            #     df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = None  

                            # if 'Master Channel' in df.columns and 'Channel/Daypart' in df.columns:
                            #     coupon_Shopper_filter = df['Media Type'] == "Temperature"
                            #     df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Media Type']
                            #     df.loc[coupon_Shopper_filter, 'Media Type'] = "Non Media"       


                        # Convert 'Cost' and 'Impression' columns to numeric, replacing non-numeric values with NaN
                        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
                        df['Impression'] = pd.to_numeric(df['Impression'], errors='coerce')
                        
                        # Handle missing values if necessary (e.g., replace NaN with 0)
                        df['Cost'] = df['Cost'].fillna(0)
                        df['Impression'] = df['Impression'].fillna(0)

                        # Perform the division to calculate normalized values
                        df['Normalized Cost'] = df['Cost']
                        df['Normalized Impression'] = df['Impression']
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df['Platform'] = df['Platform'].replace("Prism", "Shopper")
                        df['Channel/Daypart'] = df['Channel/Daypart'].replace("Percentage Promo", "Percentage Sales")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        #df[['Data Through','Daypart']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel/Daypart", "Platform", 
                            "Influencer Say", "Color Code", "Audience","Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                        st.write(f"Processed DataFrame for: {BnW_HAIR_Nexxus_PG_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')
                        csv_data = convert_df_to_csv(df)
                        st.download_button(
                            label="BnW HAIR Nexxus Download Playground Processed CSV",
                            data=csv_data,
                            file_name="BnW_HAIR_Nexxus_Processed_Data.csv",
                            mime='text/csv'
                        )

                    except Exception as e:
                        st.error(f"Error processing {BnW_HAIR_Nexxus_PG_Data_Preparation_df.name}: {e}")


        if selected == "BnW HAIR Dove":
            st.subheader("BnW HAIR Dove")
            BnW_HAIR_Dove_PG_Data_Preparation = st.file_uploader("Upload your BnW HAIR_Dove RROI file", type=["xlsx"], accept_multiple_files=True)
            if BnW_HAIR_Dove_PG_Data_Preparation:
                for BnW_HAIR_Dove_PG_Data_Preparation_df in BnW_HAIR_Dove_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(BnW_HAIR_Dove_PG_Data_Preparation_df)

                        #PW_DOVE_BW Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Modified Date','Model Scope Alias'])
                        
                        if "HAIR_Dove" in BnW_HAIR_Dove_PG_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "Beauty and Wellbeing"
                            df["Category"] = "Haircare"
                            df["Sub category"] = "Haircare"
                            df["Brand"] = "BnW HAIR Dove"
                            df["Total Brand"] = "BnW HAIR Dove"

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None  

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns and 'Product Line' in df.columns and 'Channel/Daypart' in df.columns and 'Audience' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Baseline"
                                df.loc[Earned_Media_filter, 'Product Line'] = None 
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = None
                                df.loc[Earned_Media_filter, 'Platform'] = None
                                df.loc[Earned_Media_filter, 'Audience'] = None

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Coupon"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None 

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Non Media"
                                df.loc[Earned_Media_filter, 'Channel/Daypart'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None    

                            if 'Media Type' in df.columns and 'Platform' in df.columns and 'Master Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Owned Media"
                                df.loc[Earned_Media_filter, 'Platform'] = df.loc[Earned_Media_filter, 'Master Channel']
                                df.loc[Earned_Media_filter, 'Master Channel'] = None

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Platform' in df.columns:
                                df['Media Type'] = df['Media Type'].replace('Promo', 'Trade Promo')
                                coupon_Shopper_filter = df['Media Type'] == "Trade Promo"
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = None

                            df[['Data Through','Daypart']] = ''
                            if 'Master Channel' in df.columns and 'Daypart' in df.columns and 'Channel/Daypart' in df.columns:
                                coupon_Shopper_filter = df['Master Channel'] == "TV"
                                df.loc[coupon_Shopper_filter, 'Daypart'] = df.loc[coupon_Shopper_filter, 'Channel/Daypart']
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = None  

                            if 'Master Channel' in df.columns and 'Channel/Daypart' in df.columns:
                                coupon_Shopper_filter = df['Media Type'] == "MasterBrand"
                                coupon_Shopper_filter = df['Master Channel'] == "PR"
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = " "       

                            if 'Master Channel' in df.columns and 'Channel/Daypart' in df.columns:
                                coupon_Shopper_filter = df['Media Type'] == "MasterBrand"
                                coupon_Shopper_filter = df['Master Channel'] == "Influencer"
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = " "  

                            if 'Master Channel' in df.columns and 'Channel/Daypart' in df.columns:
                                coupon_Shopper_filter = (df['Media Type'] == "Halo") & (
                                    df['Master Channel'].isin(["Commerce Display", "Commerce Search", "Digital Search", "Digital Search Visual"]))
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = "Commerce & Search"

                            if 'Master Channel' in df.columns and 'Channel/Daypart' in df.columns:
                                coupon_Shopper_filter = (df['Media Type'] == "Halo") & (
                                    df['Master Channel'].isin(["Digital Audio", "Digital Display", "Digital FEP", "Digital HUM","Digital Social","Digital Video"]))
                                df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Master Channel']
                                df.loc[coupon_Shopper_filter, 'Master Channel'] = "Digital"



                        # Convert 'Cost' and 'Impression' columns to numeric, replacing non-numeric values with NaN
                        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
                        df['Impression'] = pd.to_numeric(df['Impression'], errors='coerce')
                        
                        # Handle missing values if necessary (e.g., replace NaN with 0)
                        df['Cost'] = df['Cost'].fillna(0)
                        df['Impression'] = df['Impression'].fillna(0)

                        # Perform the division to calculate normalized values
                        df['Normalized Cost'] = df['Cost']
                        df['Normalized Impression'] = df['Impression']
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df['Platform'] = df['Platform'].replace("Prism", "Shopper")
                        df['Channel/Daypart'] = df['Channel/Daypart'].replace("Percentage Promo", "Percentage Sales")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        #df[['Data Through','Daypart']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel/Daypart", "Platform", 
                            "Influencer Say", "Color Code", "Audience","Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                        st.write(f"Processed DataFrame for: {BnW_HAIR_Dove_PG_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')
                        csv_data = convert_df_to_csv(df)
                        st.download_button(
                            label="BnW HAIR Dove Download Playground Processed CSV",
                            data=csv_data,
                            file_name="BnW_HAIR_Dove_Processed_Data.csv",
                            mime='text/csv'
                        )

                    except Exception as e:
                        st.error(f"Error processing {BnW_HAIR_Dove_PG_Data_Preparation_df.name}: {e}")
    
        if selected == "NIC Mayo Hellmann's":
            st.subheader("NIC Mayo Hellmann's")
            NIC_Mayo_Hellmann_PG_Data_Preparation = st.file_uploader("Upload your NIC Mayo Hellmann's RROI file", type=["xlsx"], accept_multiple_files=True)
            if NIC_Mayo_Hellmann_PG_Data_Preparation:
                for NIC_Mayo_Hellmann_Data_Preparation_df in NIC_Mayo_Hellmann_PG_Data_Preparation:
                    try:
                        df = pd.read_excel(NIC_Mayo_Hellmann_Data_Preparation_df)

                        #PW_DOVE_BW Playground Preparation
                        if 'Feature ID' in df.columns:
                            df = df.drop(columns=['Feature ID','Model Scope','Input Brand','Input Category','Upload Date','Modified Date','Model Scope Alias'])
                        
                        if "MAYO_Hellmann's" in NIC_Mayo_Hellmann_Data_Preparation_df.name:
                            df["Organisation"] = "Unilever"
                            df["Business Unit"] = "NIC"
                            df["Category"] = "Nutritions"
                            df["Sub category"] = "Nutritions"
                            df["Brand"] = "NIC Mayo Hellmann's"
                            df["Total Brand"] = "NIC Mayo Hellmann's"

                            if 'Media Type' in df.columns and 'Product Line' in df.columns and 'Channel' in df.columns:
                                Earned_Media_filter = df['Media Type'] == "Earned Media"
                                df.loc[Earned_Media_filter, 'Channel'] = df.loc[Earned_Media_filter, 'Product Line']
                                df.loc[Earned_Media_filter, 'Product Line'] = None  
    
                            
                        df[['Data Through','Daypart']] = ''
                            # if 'Master Channel' in df.columns and 'Daypart' in df.columns and 'Channel/Daypart' in df.columns:
                            #     coupon_Shopper_filter = df['Master Channel'] == "TV"
                            #     df.loc[coupon_Shopper_filter, 'Daypart'] = df.loc[coupon_Shopper_filter, 'Channel/Daypart']
                            #     df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = None  

                            # if 'Master Channel' in df.columns and 'Channel/Daypart' in df.columns:
                            #     coupon_Shopper_filter = df['Media Type'] == "Temperature"
                            #     df.loc[coupon_Shopper_filter, 'Channel/Daypart'] = df.loc[coupon_Shopper_filter, 'Media Type']
                            #     df.loc[coupon_Shopper_filter, 'Media Type'] = "Non Media"       


                        # Convert 'Cost' and 'Impression' columns to numeric, replacing non-numeric values with NaN
                        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
                        df['Impression'] = pd.to_numeric(df['Impression'], errors='coerce')
                        
                        # Handle missing values if necessary (e.g., replace NaN with 0)
                        df['Cost'] = df['Cost'].fillna(0)
                        df['Impression'] = df['Impression'].fillna(0)

                        # Perform the division to calculate normalized values
                        df['Normalized Cost'] = df['Cost']
                        df['Normalized Impression'] = df['Impression']
                        df['Platform'] = df['Platform'].replace("NonDigital", "Non-Digital")
                        df['Platform'] = df['Platform'].replace("Prism", "Shopper")
                        df['Channel/Daypart'] = df['Channel/Daypart'].replace("Percentage Promo", "Percentage Sales")
                        #df.rename(columns={"Channel/Daypart": "Channel"}, inplace=True)
                        #df[['Data Through','Daypart']] = ''
                        column_order = [
                            "Organisation", "Business Unit", "Category", "Sub category", "Brand", "Total Brand",
                            "Model", "Media Type", "Product Line", "Master Channel", "Channel/Daypart", "Platform", 
                            "Influencer Say", "Color Code", "Audience","Daypart", "Year", "Month", "Data Through", 
                            "Cost", "Normalized Cost", "Impression", "Normalized Impression", 
                            "Offline Dollar Sales", "Offline Volume", "Offline ROI", 
                            "Online Dollar Sales", "Online Volume", "Online ROI", 
                            "Overall Dollar Sales", "Overall Volume", "Overall ROI"
                        ]
                        df = df[column_order]
                        last_year = df['Year'].iloc[-1]
                        last_month = df['Month'].iloc[-1]
                        df['Data Through'] = pd.to_datetime(f"{last_year}-{last_month}-01") + pd.offsets.MonthEnd(0)
                        df['Data Through'] = df['Data Through'].dt.strftime('%b\'%y')
                        st.write(f"Processed DataFrame for: {NIC_Mayo_Hellmann_Data_Preparation_df.name}")
                        st.dataframe(df)

                        @st.cache_data
                        def convert_df_to_csv(dataframe):
                            return dataframe.to_csv(index=False).encode('utf-8')
                        csv_data = convert_df_to_csv(df)
                        st.download_button(
                            label="NIC Mayo Hellmann's Download Playground Processed CSV",
                            data=csv_data,
                            file_name="NIC_Mayo_Hellmann's_Processed_Data.csv",
                            mime='text/csv'
                        )

                    except Exception as e:
                        st.error(f"Error processing {NIC_Mayo_Hellmann_Data_Preparation_df.name}: {e}")
    # if selected == "Appended the Processed File":

    #     st.subheader("PC PW DOVE BW")
    #     Appended_the_Processed_Data = st.file_uploader("Upload your PW DOVE BW RROI file", type=["xlsx"], accept_multiple_files=True)







    if selected == "Data Validation(Metrics)":
        st.subheader("Data Validation(Metrics)")

        # Upload and process Metrics RROI files
        Metrics_RROI = st.file_uploader("Upload your Processed RROI file", type=["csv"], accept_multiple_files=True)
        Metrics_df = []
        if Metrics_RROI:
            for file in Metrics_RROI:
                Metrics_RROI_df = pd.read_csv(file)
                Metrics_df.append(Metrics_RROI_df)
            st.write("Processed RROI Data")
            st.write(Metrics_RROI_df)
        
        # Upload and process AI RROI files
        AI_RROI_File = st.file_uploader("Upload your AI RROI file", type=["xlsx"], accept_multiple_files=True)
        AI_RROI_check = []
        if AI_RROI_File:
            for file in AI_RROI_File:
                AI_RROI_File_df = pd.read_excel(file)
                AI_RROI_check.append(AI_RROI_File_df)
            st.write("AI RROI Data")
            st.write(AI_RROI_File_df)
        
        # Columns to validate
        columns_to_validate = [
            'Cost', 'Impression', 'Offline Dollar Sales', 'Offline Volume', 
            'Offline ROI', 'Online Dollar Sales', 'Online Volume', 
            'Online ROI', 'Overall Dollar Sales', 'Overall Volume', 'Overall ROI'
        ]
        
        # Perform sum comparison if both files are uploaded
        if Metrics_RROI and AI_RROI_File:
            for column in columns_to_validate:
                try:
                    # Calculate sums for the column
                    Metrics_column_sum = round(sum(df[column].sum() for df in Metrics_df),2)
                    AI_column_sum = round(sum(df[column].sum() for df in AI_RROI_check),2)

                    # Display results for each column
                    st.write(f"Sum of '{column}' in Processed RROI: {Metrics_column_sum}")
                    st.write(f"Sum of '{column}' in AI RROI: {AI_column_sum}")

                    # Check if the sums match
                    if Metrics_column_sum == AI_column_sum:
                        st.success(f"The sums of '{column}' match!")
                    else:
                        st.error(f"The sums of '{column}' do not match!")
                except KeyError:
                    st.warning(f"Column '{column}' not found in one of the uploaded files.")

    
    if selected == "Data Validation(dimensions)":
        st.subheader("Data Validation(dimensions)")

        # Upload and process Mapper RROI files
        Metrics_RROI = st.file_uploader("Upload your mapper RROI file", type=["xlsx"], accept_multiple_files=True)
        Metrics_df = []
        if Metrics_RROI:
            for file in Metrics_RROI:
                Metrics_RROI_df = pd.read_excel(file)
                Metrics_df.append(Metrics_RROI_df)
            st.write("Mapper RROI Data")
            st.write(Metrics_RROI_df)
        
        # Upload and process Processed RROI files
        AI_RROI_File = st.file_uploader("Upload your Processed RROI file", type=["csv"], accept_multiple_files=True)
        AI_RROI_check = []
        if AI_RROI_File:
            for file in AI_RROI_File:
                AI_RROI_File_df = pd.read_csv(file)
                AI_RROI_check.append(AI_RROI_File_df)
            st.write("Processed RROI Data")
            st.write(AI_RROI_File_df)
        
        # Columns to validate
        dimensions_to_validate = [
            'Organisation', 'Business Unit', 'Category', 'Sub category', 
            'Brand', 'Total Brand', 'Media Type', 'Product Line', 
            'Master Channel', 'Channel', 'Platform', 'Influencer Say', 
            'Color Code', 'Audience', 'Daypart'
        ]
        
        # Perform validation if both files are uploaded
        if Metrics_RROI and AI_RROI_File:
            for dimension in dimensions_to_validate:
                try:
                    # Get unique values from both files
                    mapper_values = set(Metrics_RROI_df[dimension].dropna().unique())
                    processed_values = set(AI_RROI_File_df[dimension].dropna().unique())
                    
                    # Check if values match
                    missing_in_processed = mapper_values - processed_values
                    missing_in_mapper = processed_values - mapper_values
                    
                    # Display results
                    st.write(f"**Dimension: {dimension}**")
                    if not missing_in_processed and not missing_in_mapper:
                        st.success(f"All values in '{dimension}' match between the two files.")
                    else:
                        if missing_in_processed:
                            st.warning(f"Values in Mapper but missing in Processed for '{dimension}': {missing_in_processed}")
                        if missing_in_mapper:
                            st.warning(f"Values in Processed but missing in Mapper for '{dimension}': {missing_in_mapper}")
                except KeyError:
                    st.warning(f"Column '{dimension}' not found in one of the uploaded files.")

                  


       
elif selected == "QC":
    # Function to process JSON file to DataFrame
    def process_json_to_excel(json_file_path):
        with open(json_file_path) as file:
            data = json.load(file)
        
        new_data = {}
        for product_line in data:
            for master_channel in data[product_line]:
                new_data = {**new_data, **data[product_line][master_channel]}
        
        rows = []
        for feature, variables in new_data.items():
            if isinstance(variables, list):
                for var in variables:
                    rows.append({'Features': feature, 'Variables': var})
            else:
                rows.append({'Features': feature, 'Variables': variables})
        
        return pd.DataFrame(rows)

    # Function to initialize session state
    def initialize_session_state():
        if 'modified_files' not in st.session_state:
            st.session_state.modified_files = {}

    with st.sidebar:
        initialize_session_state()
        selected = st.selectbox("Main Menu", ['Json to Excel','Preprocessed QC','Attribution check'], index=0)

    st.header("Quality Check")


    if selected == 'Json to Excel':
        st.header("Convert Json files to Excel files")
        uploaded_files = st.file_uploader("Upload JSON file(s)", type="json", accept_multiple_files=True)
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save uploaded file to a temporary location
                with open("temp.json", "wb") as f:
                    f.write(uploaded_file.getvalue())
                # Process JSON file
                df = process_json_to_excel("temp.json")
                
                # Save DataFrame to Excel file
                excel_file = BytesIO()
                df.to_excel(excel_file, index=False)
                excel_file.seek(0)
                
                # Download Excel file
                st.download_button(label=f"Download Excel File ({uploaded_file.name})", data=excel_file, file_name=f'output_{uploaded_file.name}.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

                # Delete temporary JSON file
                os.remove("temp.json")


    if selected == 'Preprocessed QC':
        st.header("Preprocessed QC")
        # Upload files
        uploaded_files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

        # Process files
        if uploaded_files:
            dataframes = []
            for file in uploaded_files:
                if file.type == "text/csv":
                    df = pd.read_csv(file)
                elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    df = pd.read_excel(file)
                else:
                    continue
                # Check if 'Date' column exists
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert 'Date' to datetime, set invalid parsing to NaT
                    dataframes.append(df)
                else:
                    st.warning(f"The file {file.name} does not contain a 'Date' column and will be ignored.")

            if dataframes:
                # Concatenate 'Date' columns
                all_dates = pd.concat([df['Date'].dropna() for df in dataframes])  # Drop NaT values
                common_start_date = all_dates.min().date()
                common_end_date = all_dates.max().date()
                st.write(f"Common date range: {common_start_date} to {common_end_date}")
            else:
                st.warning("No valid dataframes with 'Date' columns were uploaded.")

            
            # Date input
            start_date = st.date_input('Start date', common_start_date)
            end_date = st.date_input('End date', common_end_date)
            
            if start_date and end_date:
                filtered_dataframes = []
                melted_dfs = []
                for df in dataframes:
                    mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
                    filtered_dataframes.append(df.loc[mask])
                
                for i, (file, filtered_df) in enumerate(zip(uploaded_files, filtered_dataframes), start=1):
                    file_name = file.name.lower()
                    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
                    melted_df = pd.melt(filtered_df, id_vars=['Date'], var_name='Variable', value_name='Value')
                    melted_df['Year'] = melted_df['Date'].apply(lambda dt: f"{dt.year:04d}")
                    melted_df['Month'] = melted_df['Date'].apply(lambda dt: calendar.month_abbr[dt.month])
                    
                    # Add additional columns based on filename
                    if 'offline' in file_name:
                        melted_df['Type'] = 'offline'
                    elif 'online' in file_name:
                        melted_df['Type'] = 'online'
                    elif 'cost' in file_name:
                        melted_df['Type'] = 'cost' 
                    melted_dfs.append(melted_df)       

                # Concatenate all melted dataframes
                if melted_dfs:
                    all_melted_df = pd.concat(melted_dfs, ignore_index=True)
                    all_melted_df['Variable'] = (all_melted_df['Variable']
                             .str.replace(r'\|Impressions\|', '|', regex=True)
                             .str.replace(r'\|Cost\|', '|', regex=True)
                             .str.replace(r'\|Media Cost\|', '|', regex=True)
                             .str.replace(r'\|sessions\|', '|', regex=True)
                             .str.replace(r'\|spends\|', '|', regex=True))
                    all_melted_split = all_melted_df['Variable'].str.split('|', expand=True)
                    num_columns = all_melted_split.shape[1]
                    column_names = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']
                    column_names = column_names[:num_columns]
                    all_melted_split.columns = column_names
                    if 'V6' in all_melted_split.columns:
                        all_melted_split['V6'] = all_melted_split['V6'].replace('', np.nan)
                    all_melted_df = pd.concat([all_melted_df, all_melted_split], axis=1)    
                    def to_excel(df):
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            df.to_excel(writer, index=False, sheet_name='Sheet1')
                        processed_data = output.getvalue()
                        return processed_data
                    excel_data = to_excel(all_melted_df)
                    st.download_button(
                        label="Download Excel file",
                        data=excel_data,
                        file_name='all_melted_df.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                else:
                    st.warning("No data found for the selected date range.")
            else:
                st.warning("Please select both start and end dates.")
        else:
            st.warning("Please upload at least one CSV file.")
    if selected == 'Attribution Check':
        st.header("Attribution Check")
    sys.exit()

    # Add content for QC here
elif selected == "Setting":
    st.title(f"You have selected {selected}")
    # Add content for Setting here
elif selected == "More Feature":
    st.title(f"You have selected {selected}")
    # Add content for More Feature Feature here
