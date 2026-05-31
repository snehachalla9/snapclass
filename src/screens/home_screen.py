import streamlit as st
from src.componets.header import header_home
from src.ui.base_layout import style_base_layout,style_background_home,style_background_dashboard
def home_screen():
    # st.header('home screen')
    header_home()
    style_base_layout()
    style_background_home()
    # col1,col2=st.columns(2)
    space1, col1, col2, space2 = st.columns([1,1,1,1],vertical_alignment="center")
    with col1:
        st.image("assets/teacher.png", width=180)
        # st.image("/home/rgukt-basar/Pictures/Screenshots/teacher.png",width=180)
        if st.button('teacher portal',key="teacher_btn",type='primary'):
            st.session_state['login_type']='teacher'
            st.rerun()
    with col2:
        st.image("assets/student.png", width=180)
        # st.image("/home/rgukt-basar/Pictures/Screenshots/student.png",width=180)
        if st.button('student portal',key="student_btn",type='primary'):
            st.session_state['login_type']='student'
            st.rerun()

