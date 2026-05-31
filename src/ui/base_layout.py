import streamlit as st

def style_background_home():
    st.markdown("""
                <style>

.stApp{
    background:#5865F2;
}

/* Style only teacher and student cards */
div[data-testid="stColumn"]:nth-of-type(2),
div[data-testid="stColumn"]:nth-of-type(3){

    background-color:#E0E3FF !important;

    padding:2.5rem !important;

    border-radius:5rem !important;
}

</style>
""", unsafe_allow_html=True)

def style_background_dashboard():

    st.markdown("""
    <style>

    .stApp{
        background:#CFE8FF !important;
    }

    [data-testid="stAppViewContainer"]{
        background:#CFE8FF !important;
    }

    h1{
        color:#2D2D44 !important;
        text-align:center !important;
    }

    </style>
    """, unsafe_allow_html=True)
def style_base_layout():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@300;400;500;600&display=swap');

    /* Full App Background */
    .stApp{
        background:#5865F2;
    }

    /* Move content downward */
    .block-container{
        padding-top:8rem !important;
    }

    /* Heading */
    h1{
        font-family:'Climate Crisis', sans-serif !important;

        font-size:2 rem !important;

        text-align:center !important;

        color:#1e1e1e !important;

        margin-bottom:5rem !important;

        text-shadow:3px 3px 0px rgba(0,0,0,0.2);
    }

    /* Text Font */
    h3,h4,p{
        font-family:'Outfit',sans-serif !important;
    }

    /* Center Buttons */
    div.stButton{
        display:flex;
        justify-content:center;
    }

    /* ALL Buttons */
    div.stButton > button{

        background:#EB459E !important;
        color:white !important;

        width:170px !important;
        height:45px !important;

        border:none !important;

        border-radius:1.5rem !important;

        font-size:15px !important;
        font-weight:500 !important;

        transition:transform 0.25s ease-in-out !important;
    }

    /* Hover Effect */
    div.stButton > button:hover{
        transform:scale(1.05);
    }

    </style>
    """, unsafe_allow_html=True)