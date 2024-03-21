import streamlit as st
import boto3

MAP_EMOJI_URL = "https://em-content.zobj.net/source/apple/391/bucket_1faa3.png"

# Set page title and favicon.
st.set_page_config(
    page_title="S3 to HTTPS Links Converter", 
    page_icon=MAP_EMOJI_URL,
    layout="centered"
)
st.markdown("<br>", unsafe_allow_html=True)
st.image(MAP_EMOJI_URL, width=80)
st.markdown("""
    # S3 to HTTPS Links Converter
    [![Follow](https://img.shields.io/twitter/follow/mykolakozyr?style=social)](https://www.twitter.com/mykolakozyr)
    [![Follow](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/mykolakozyr/)
    
    ## Details

    This is an app to transform S3 URI to HTTPS URL. Working with S3 URIs could be annoying for us, ordinary people, while engineers keep using them like they have no idea it does not just open in the browser. 
    The app is designed with anger and annoyment, but also with love to people.

    ---
    """)

# Access secrets
aws_access_key_id = st.secrets["aws_access_key_id"]
aws_secret_access_key = st.secrets["aws_secret_access_key"]


# Setup AWS session
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Function to retrieve the HTTPS URL
def s3_to_https(uri, session):
    # Split the URI to extract bucket name and object path
    parts = uri.split("://")[1].split("/", 1)
    bucket_name = parts[0]
    object_name = parts[1] if len(parts) > 1 else ""

    # Create an S3 client
    s3 = session.client('s3')

    # Retrieve the bucket's region
    bucket_location = s3.get_bucket_location(Bucket=bucket_name)
    region = bucket_location['LocationConstraint']
    if region is None:
        region = 'us-east-1'

    # Construct the HTTPS URL based on the region
    if region == 'us-east-1':
        https_url = f'https://{bucket_name}.s3.amazonaws.com/{object_name}'
    else:
        https_url = f'https://{bucket_name}.s3-{region}.amazonaws.com/{object_name}'

    return https_url

# Text input for the S3 URL
s3 = st.text_input('Please insert your S3 URI and press Enter.')
if s3:
	#Validating the if the URL starts with S3
	if s3.startswith('s3://'):
		https= s3_to_https(s3, session)
		st.success("✅ The HTTPS URL: " + https)
	else:
		st.error("Please make sure you inserted the valid S3 URI. It should start with `s3://`.")
