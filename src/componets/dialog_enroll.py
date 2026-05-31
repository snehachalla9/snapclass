import streamlit as st
from src.database.db import create_subject,enroll_student_to_subject
from src.database.config import supabase
@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code=st.text_input('Subject_code',placeholder='Eg cs123')
    join_code=join_code.lower()
    if st.button('Enroll_now',type='primary',width='stretch'):
        if join_code:
            res=supabase.table('subjects').select('subject_id,name,subject_code').ilike('subject_code',join_code.strip()).execute()
            # st.write(res.data)
            if res.data:
                subject=res.data[0]
                student_id=st.session_state.student_data['student_id']
                check=supabase.table('subject_students').select('*').eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
                if check.data:
                    st.warning('You ar already enrolled')
                else:
                    response=enroll_student_to_subject(student_id,subject['subject_id'])
                    st.write(response)
                    if response:
                        st.success("successfully  enrolled!")
                    else:
                        st.error("Enrollment failed!..")
                    import time
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning('please enter a subject code')





