import streamlit as st
import pandas as pd
import requests
from io import StringIO
from base64 import b64encode

def process_locations(data):
    # Read the data into a DataFrame
    df = pd.read_csv(StringIO(data), error_bad_lines=False)
    
    # Perform any necessary processing
    # For example, you might want to clean the data or perform some analysis
    
    return df

def main():
    st.title('Location Downloader')
    
    url = st.text_input('Enter URL to CSV file:')
    
    if st.button('Download'):
        if url:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    locations_df = process_locations(response.text)
                    
                    # Display the processed data
                    st.write('Processed locations data:')
                    st.write(locations_df)
                    
                    # Allow users to download the processed data
                    st.markdown(get_csv_download_link(locations_df), unsafe_allow_html=True)
                else:
                    st.error(f'Failed to fetch data from URL. Status code: {response.status_code}')
            except Exception as e:
                st.error(f'Error fetching data from URL: {str(e)}')
        else:
            st.warning('Please enter a URL.')

def get_csv_download_link(df):
    # Generate a link to download the dataframe as CSV
    csv = df.to_csv(index=False)
    href = f'<a href="data:file/csv;base64,{b64encode(csv.encode()).decode()}" download="processed_locations.csv">Download processed data</a>'
    return href

if __name__ == '__main__':
    main()
