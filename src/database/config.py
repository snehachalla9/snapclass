import streamlit as st
st.write("URL exists:", "SUPABASE_URL" in st.secrets)
st.write("KEY exists:", "SUPABASE_KEY" in st.secrets)
from supabase import create_client,Client
supabase:Client=create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
