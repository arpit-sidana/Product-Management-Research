import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_company_info(company_name):
    """
    Get company information using Clearbit API
    """
    # You'll need to sign up for a Clearbit API key
    api_key = os.getenv('CLEARBIT_API_KEY')
    headers = {'Authorization': f'Bearer {api_key}'}
    
    try:
        response = requests.get(
            f'https://company.clearbit.com/v2/companies/find?name={company_name}',
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

# Set up the Streamlit page
st.set_page_config(page_title="Company Info Finder", page_icon="🏢")
st.title("Company Information Finder")

# Create the search box
company_name = st.text_input("Enter company name:", placeholder="e.g., Microsoft")

if company_name:
    with st.spinner('Fetching company information...'):
        company_data = get_company_info(company_name)
        
        if company_data:
            # Display company information
            st.subheader("Company Details")
            
            # Basic company info
            st.write(f"**Name:** {company_data.get('name', 'N/A')}")
            st.write(f"**Domain:** {company_data.get('domain', 'N/A')}")
            st.write(f"**Employee Count:** {company_data.get('metrics', {}).get('employeeCount', 'N/A')}")
            
            # Additional details
            st.write(f"**Industry:** {company_data.get('category', {}).get('industry', 'N/A')}")
            st.write(f"**Description:** {company_data.get('description', 'N/A')}")
            
            # Show company logo if available
            if company_data.get('logo'):
                st.image(company_data['logo'], width=100)
        else:
            st.error("Could not find company information")
