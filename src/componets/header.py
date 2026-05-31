import streamlit as st
import base64

def header_home():

    logo_path = "/home/rgukt-basar/Downloads/images.png"

    with open(logo_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
        <div style="
            display:flex;
            justify-content:center;
            margin-top:20px;
            margin-bottom:30px;
        ">
            <img src="data:image/png;base64,{encoded}"
                 style="height:220px;">
            <h1 style='text-align:center;color:#E0E3FF'>SNAP<br/>CLASS<h1/>


        </div>
    """, unsafe_allow_html=True)
import streamlit as st

def header_dashboard():
    logo_path = "/home/rgukt-basar/Downloads/images.png"

    with open(logo_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
        <div style="
            display:flex;
            justify-content:center;
            margin-top:-10px;
            margin-bottom:10px;
        ">
            <img src="data:image/png;base64,{encoded}"
                 style="height:100px;">
            <h4 style='text-align:center;color:#4A6CFF'>SNAP<br/>CLASS<h4/>


        </div>
    """, unsafe_allow_html=True)