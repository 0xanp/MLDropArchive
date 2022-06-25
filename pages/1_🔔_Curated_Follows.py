import streamlit as st
from twitter_auth import bearer_token
import tweepy
st.set_page_config(page_title="Curated Follows Feed", page_icon="🔔", layout="wide")
st.markdown("# Curated Follows Feed Demo")
st.sidebar.header("Some filtering")
st.write(
    """This is placeholder page for the curated follows feed"""
)
# ----- ESTABLISH A TWEEPY CLIENT 
# client = tweepy.Client(bearer_token=bearer_token)
# Curated list of usernames we want to track

# curated_lists = ['0xAnP','itsjvon']