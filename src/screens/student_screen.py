import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.componets.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance,get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject
from src.componets.dialog_enroll import enroll_dialog
from src.componets.subject_card import subject_card
def student_dashboard():
    st.markdown("""
                <h1 style='
                color:black;
                text-align:center;
                font-size:40px;
                font-weight:700;
                '>
                DASHBOARD HERE
                </h1>
                """, unsafe_allow_html=True)
    student_data=st.session_state.student_data
    student_id=student_data['student_id']
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
            f'<h1 class="welcome-text" style="font-size:24px;">Welcome, {student_data["name"]} 👋</h1>',
            unsafe_allow_html=True
)
        if st.button("Log out",type='secondary',key='loginbackbtn'):
            st.session_state['is_logged_in']=False
            del st.session_state.student_data
            st.rerun()
    st.space()
    c1,c2=st.columns(2)
    with c1:
        st.markdown(
            "<h2 style='color:black;'>Your Enrolled subjects</h2>",
            unsafe_allow_html=True
            )
            # st.header('Your Enrolled subjects')
    with c2:
        if st.button('Enroll in subject',type='primary',width='stretch'):
            enroll_dialog()
    st.divider()
    with st.spinner('Loading your enrolled subjects'):
        subjects=get_student_subjects(student_id)
        logs=get_student_attendance(student_id)
        stats_map={}
        for log in logs:
            sid=log['subject_id']
            if sid not in stats_map:
                stats_map[sid]={"total":0,"attended":0}
            stats_map[sid]['total']+=1
            if log.get('is_present'):
                stats_map[sid]['attended']+=1
        # cols= st.columns([1,1], gap="large")
    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sid=sub_node['subject_id']
        stats=stats_map.get(sid,{"total":0,"attended":0})
        def unenroll_button(sid=sid, i=i):
            if st.button(
                "unenroll from this course",
                type="tertiary",
                key=f"unenroll_{sid}_{i}",
                icon=":material/delete_forever:",
                use_container_width=True
                ):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"unenrolled from {sub['name']} successfully")
                st.rerun()

            # with cols[i%2]:
        subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=[
                ('📊','Total',stats['total']),
                ('✅','Attended',stats['attended']),
                    ],
                    footer_callback=unenroll_button
                    )
def student_screen():
    style_background_dashboard()
    style_base_layout()
    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("go back home",type='secondary',key='loginbackbtn'):
            st.session_state['login_type']=None
            st.rerun()
    st.markdown("""
                <style>
                h2{
                color:black !important;
                text-align:center !important;
                font-size:30px !important;
                font-weight:600 !important;
                caret-color:black !important;
                }
                </style>
                """, unsafe_allow_html=True)
    # st.header('Login Using Password')
    st.header('Login Using Face Id',text_alignment='center')
    st.space()
    st.space()
    st.markdown("""
                <style>
                /* Input box */
                .stTextInput input{
                 background:white !important;
                color:black !important;
                border-radius:10px !important;
                border:none !important;
                padding:12px !important;
                }
                /* Placeholder */
                .stTextInput input::placeholder{
                color:gray !important;
                opacity:1 !important;
                }
                /* Label */
                .stTextInput label{
                color:black !important;
                font-weight:600 !important;
                }
                </style>
                """, unsafe_allow_html=True)
    # st.header('student screen')
    show_registration=False
    photo_source=st.camera_input("position your camera")
    if photo_source:
        img=np.array(Image.open(photo_source))
        with st.spinner('AI is scanning'):
            detected,all_ids,num_faces=predict_attendance(img)
            if num_faces==0:
                st.warning('Face not found')
            elif num_faces>1:
                st.markdown(
                    """
                    <div style="
                    background-color:black;
                    color:white;
                    padding:10px;
                    border-radius:10px;
                    font-size:18px;
                    text-align:center;
                    ">
                    Multiple Faces Detected
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                # st.warning('Multiple Faces detected')
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s['student_id']==student_id),None)
                    if student:
                        st.success(
                            f"Face recognized : {student['name']}")
                        st.session_state.face_verified = True
                        st.session_state.temp_student = student
                    # if student:
                    #     st.session_state.is_logged_in=True
                    #     st.session_state.user_role='student'
                    #     st.session_state.student_data=student
                    #     st.toast(f"Welcome Back {student['name']}")
                       
                    #     import time
                    #     time.sleep(1)
                    #     st.rerun()
                else:
                    st.info('Face not recoginsed You might me new student')
                    show_registration=True
    if st.session_state.get("face_verified"):
        st.divider()
        st.header("Voice Verification")
        st.markdown("""
                    <style>

/* Audio input label */
[data-testid="stAudioInput"] label {
    color: black !important;
    font-weight: 600 !important;
    font-size: 18px !important;
}

/* Audio input container */
[data-testid="stAudioInput"] {
    color: black !important;
}

/* Microphone button text/icons */
[data-testid="stAudioInput"] button {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)
        voice_login_audio = st.audio_input(
            "Speak for verification"
            )
        if voice_login_audio is not None:
            with st.spinner("Checking your voice..."):
                audio_bytes = voice_login_audio.read()
                voice_emb = get_voice_embedding(audio_bytes)
                st.markdown(
    f"""
    <p style="
    color:black;
    font-size:16px;
    font-weight:600;
    ">
    Voice embedding generated:
    {voice_emb is not None}
    </p>
    """,
    unsafe_allow_html=True
)
                # st.write(
                #     "Voice embedding generated:",
                #     voice_emb is not None
                #     )
                if voice_emb is not None:
                    student = st.session_state.temp_student
                    stored_emb = student.get("voice_embedding")
                    if stored_emb is None:
                        st.error(
                            "No voice enrolled for this student"
                            )
                    else:
                        try:
                            emb1 = np.array(voice_emb)
                            emb2 = np.array(stored_emb)
                            similarity = np.dot(emb1, emb2) / (
                                np.linalg.norm(emb1) *
                                np.linalg.norm(emb2)
                                )
                            st.write(
                                f"Similarity : {similarity:.2f}")
                            if similarity > 0.75:
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = student
                                st.success(
                                    f"Welcome {student['name']}"
                                    )
                                import time
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Voice not matched")
                        except Exception as e:
                            st.error(f"Comparison Error: {e}")
                else:
                    st.error(
                        "Could not generate voice embedding")
    
    if show_registration:
            with st.container(border=True):
                st.header('Register new Profile')
                new_name=st.text_input("Enter Your name",placeholder='sneha challa')
                st.markdown(
                    "<h3 style='color:black;'>Optional: Voice Enrollment</h3>",
                    unsafe_allow_html=True)
                # st.subheader('Optional:voice enrollment')
                st.info("enroll your voice for only attendance")
                audio_data=None
                try:
                    st.markdown(
                        """
                        <p style="
                        color:black;
                        font-size:16px;
                        font-weight:600;
                        ">
                        Record your voice like: I am present, My name is Sneha
                        </p>
                        """,
                        unsafe_allow_html=True
                        )
                    audio_data = st.audio_input("")
                    # audio_data=st.audio_input('Record you vice like I am present,Mu name is sneha')
                except Exception as e:
                    st.error('Audio data failed')
                if st.button('Create  Account',type='primary'):
                    if new_name:
                        with st.spinner('Creating Profile..'):
                            img=np.array(Image.open(photo_source))
                            encodings=get_face_embeddings(img)
                            if encodings:
                                face_emb=encodings[0].tolist()
                                voice_emb=None
                                if audio_data is not None:
                                     audio_bytes = audio_data.read()
                                     st.write("Audio bytes:", len(audio_bytes))
                                     voice_emb = get_voice_embedding(audio_bytes)
                                     st.write("Voice embedding generated:", voice_emb is not None)
                                else:
                                    voice_emb = None
                                # if audio_data is not None:
                                #       audio_bytes = audio_data.read()
                                #       voice_emb = get_voice_embedding(audio_bytes)
                                #       st.write(voice_emb)
                                # if audio_data:
                                #     voice_emb=get_voice_embedding(audio_data.read())
                                response_data=create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)
                                if response_data:
                                    train_classifier()
                                    st.session_state.is_logged_in=True
                                    st.session_state.user_role='student'
                                    st.session_state.student_data=response_data
                                    st.toast(f"Welcome Back {response_data[0]['name']}")
                                   
                                    import time
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error('couldnt capture you face')
                                    


                    else:
                        st.warning('Please enter your name')



