import streamlit as st
import pandas as pd

# Title of the app
st.title('Action Identifier')

# File uploader for CSV and Excel files
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Determine file type and read accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            df = df.drop_duplicates(subset=[col for col in df.columns if col != 'Cumulative count'])
        # Display the original dataframe
        st.write("Original Data:")
        st.dataframe(df)
        if 'Feature ID' in df.columns:
            # Split the 'Feature ID' column
            df['Feature Number'] = df['Feature ID'].str.split('_').str[1].astype(int)

        # Check if required columns exist
        if 'Key' in df.columns and 'Feature Number' in df.columns:
            # Group by 'Key' and count occurrences
            key_counts = df['Key'].value_counts().to_dict()
            
            # Function to classify based on Feature Number and Key count
            def classify_action(row):
                key = row['Key']
                # Get the count of occurrences for the current Key
                count = key_counts[key]
                
                if count > 1:
                    # Get the maximum Feature Number for the current Key
                    max_feature_number = df[df['Key'] == key]['Feature Number'].max()
                    # Return "High" if the current Feature Number is the maximum, otherwise "Low"
                    return "High" if row['Feature Number'] == max_feature_number else "Low"
                else:
                    return "High"  # Single occurrence case

            # Apply classification to each row
            df['Action'] = df.apply(classify_action, axis=1)
            
            # Display the updated dataframe with Action Classification
            st.write("Data with Action Identifier:")
            st.dataframe(df)
        else:
            st.warning("'Key' or 'Feature Number' column not found in the uploaded file.")
        
        # Convert dataframe to CSV for download
        csv = df.to_csv(index=False)

        # Create a download button
        st.download_button(
            label="Download Processed Data as CSV",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv'
        )
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
