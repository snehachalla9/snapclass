import streamlit as st
from src.database.db import create_subject

@st.dialog("create new subject")
def create_subject_dialog(teacher_id):
    st.write('Enter the details of new subject')
    sub_id=st.text_input('subject code',placeholder='cs1234')
    sub_name=st.text_input('subject name',placeholder='machine learning')
    section=st.text_input('section',placeholder='ECE c4')
    if st.button("create subject now",type='primary',width='stretch'):
        if sub_id  and sub_name and section:
            try:
                create_subject(sub_id,sub_name,section,teacher_id)
                st.toast('subject created successfully')
                st.rerun()
            except Exception as e:
                st.error(f"Error:{str(e)}")
        else:
            st.warning('please fill all required details')        

