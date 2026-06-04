import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.componets.header import header_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subject,get_attendance_for_teacher
from src.componets.dialog_create_subject import create_subject_dialog
from src.componets.subject_card import subject_card
from src.componets.dialog_share_subject import share_subject_dialog
from src.componets.dialog_add_photo import add_photos_dialog
import numpy as np
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance
from datetime import datetime
import pandas as pd
from src.componets.dialog_attendance_results import attendance_result_dialog
from src.componets.dialog_voice_attendance import voice_attendance_dialog
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()


    # c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    # with c1:
    #     header_dashboard()
    # with c2:
    #     st.button("go back home",type='secondary',key='loginbackbtn')
    # st.markdown("""
    #             <style>
    #             h2{
    #             color:black !important;
    #             text-align:center !important;
    #             font-size:30px !important;
    #             font-weight:600 !important;
    #             }
    #             </style>
    #             """, unsafe_allow_html=True)
    # st.header('Register Your teacher Profile')
    # st.markdown(
    # "<h1>Register Your Teacher Profile</h1>",
    # unsafe_allow_html=True)
def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
            f'<h1 class="welcome-text" style="font-size:24px;">Welcome, {teacher_data["name"]} 👋</h1>',
            unsafe_allow_html=True
)
        # st.markdown(
        # f'<h1 class="welcome-text">Welcome, {teacher_data["name"]} 👋</h1>',
        # unsafe_allow_html=True)
    
        if st.button("Log out",type='secondary',key='loginbackbtn'):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()
    st.space()
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab='Take_attendance'
    tab1,tab2,tab3=st.columns(3)
    with tab1:
        type1="primary" if st.session_state.current_teacher_tab=='Take_attendance' else "tertiary"
        if st.button('Take_attendance',type=type1,width='stretch',icon=':material/how_to_reg:'):
            st.session_state.current_teacher_tab='Take_attendance'
            st.rerun()
    with tab2:
        type2="primary" if st.session_state.current_teacher_tab=='Manage_subjects' else "tertiary"
        if st.button('Manage_subjects',type=type2,width='stretch',icon=':material/how_to_reg:'):
            st.session_state.current_teacher_tab='Manage_subjects'
            st.rerun()
    with tab3:
        type3="primary" if st.session_state.current_teacher_tab=='Attendance Records' else "tertiary"
        if st.button('Attendance Records',type=type3,width='stretch',icon=':material/how_to_reg:'):
            st.session_state.current_teacher_tab='Attendance Records'
            st.rerun()
    st.divider()
    if st.session_state.current_teacher_tab=="Take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab=='Manage_subjects':
        teacher_tab_Manage_subjects()
    if st.session_state.current_teacher_tab=='Attendance Records':
        teacher_tab_Attendance_Records()
def teacher_tab_take_attendance():
    teacher_id=st.session_state.teacher_data['teacher_id']
    st.markdown("""
                <h2 style="
                color:black;
                font-size:32px;
                font-weight:700;
                ">
                Take AI Attendance
                </h2>
                """, 
                unsafe_allow_html=True)
    # st.header('Take AI attendance')
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images=[]
    subjects=get_teacher_subject(teacher_id)
    if not subjects:
        st.warning("you havent created any subjects yet! please create one to begin")
        return
    subject_options={f"{s['name']}-{s['subject_code']}":s["subject_id"] for s in subjects}
    col1,col2=st.columns([3,1],vertical_alignment='bottom')
    with col1:
        st.markdown("### <span style='color:black'>Select Subject</span>", unsafe_allow_html=True)
        selected_subject_label = st.selectbox(
    "",
    options=list(subject_options.keys())
)
    #     selected_subject_label=st.selectbox('select subject',options=list(subject_options.keys()))
    with col2:
        if st.button('➕Add photos',type='primary',icon=':material/photo_prints:',width='stretch'):
            add_photos_dialog()
    selected_subject_id=subject_options[selected_subject_label]
    st.divider()
    if st.session_state.attendance_images:
        st.markdown(
            "<h2 style='color:black;'>Added photos</h2>",
            unsafe_allow_html=True
            )
        # st.header('Added photos')
        gallery_cols=st.columns(4)
        for idx,img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx%4]:
                st.image(img,width='stretch')
                st.markdown(
                    f"<p style='color:black;'>photo{idx+1}</p>",
                    unsafe_allow_html=True
                    )
        has_photos=bool(st.session_state.attendance_images)
        c1,c2,c3=st.columns(3)
        with c1:
            if st.button('clear all photos',width='stretch',type='tertiary',icon=':material/delete:'):
                st.session_state.attendance_images=[]
                st.rerun()
        with c2:
            # has_photos=bool(st.session_state.attendance_images)
            if st.button('run face analysis',width='stretch',type='tertiary',icon=':material/analytics:',disabled=not has_photos):
                with st.spinner('Deep scanning classroom photos '):
                    all_detected_ids={}
                    for idx,img in enumerate(st.session_state.attendance_images):
                        img_np=np.array(img.convert("RGB"))
                        detected,_,_=predict_attendance(img_np)
                        if detected:
                            for sid in detected.keys():
                                student_id=int(sid)
                                all_detected_ids.setdefault(student_id,[]).append(f"photo{idx+1}")
                    enrolled_res=supabase.table('subject_students').select("*,students(*)").eq('subject_id',selected_subject_id).execute()
                    enrolled_students=enrolled_res.data
                    if not enrolled_students:
                        st.warning('No students enrolled in this course')
                    else:
                        results,attendance_to_log=[],[]
                        current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                        for node in enrolled_students:
                            student=node['students']
                            sources=all_detected_ids.get(int(student['student_id']),[])
                            is_present=len(sources)>0
                            results.append({
                                "Name":student['name'],
                                "ID":student['student_id'],
                                "source":",".join(sources) if is_present else "_",
                                "status":"✅present" if is_present else "❌absent"
                            })
                            attendance_to_log.append({
                                'student_id':student['student_id'],
                                'subject_id':selected_subject_id,
                                'timestamp':current_timestamp,
                                'is_present':bool(is_present)
                            })
                            attendance_result_dialog(pd.DataFrame(results),attendance_to_log)
        with c3:
            if st.button('use voice attendance',type='primary',width='stretch',icon=':material/mic:'):
                voice_attendance_dialog(selected_subject_id)

        

            







def teacher_tab_Manage_subjects():
    st.markdown("""
    <style>

    .stButton > button {
        color: black !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        border-radius: 12px !important;
    }

    .stButton > button p {
        white-space: nowrap !important;
    }

    </style>
    """, unsafe_allow_html=True)
    teacher_id=st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown("""
                    <h1 style="
                    font-size:48px;
                    font-weight:800;
                    line-height:0.9;
                    color:#1e293b;
                    ">
                    Manage<br>Subjects
                    </h1>
                    """, unsafe_allow_html=True)
    with col2:
        if st.button(
            'Create New Subject',
            width='stretch',
            type='primary'
            ):
            create_subject_dialog(teacher_id)
    # col1,col2=st.columns(2)
    # with col1:
    #     st.header('Manage Subjects',width='stretch')
    # with col2:
    #     if st.button('Create New Subjects',width='stretch'):
    #         create_subject_dialog(teacher_id)
    #List all subjects
    subjects=get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                ("👥","students",sub['total_students']),
                ("🏫","classes",sub['total_classes'])
            ]
            def sharebtn(sub=sub):
                if st.button(f"share code:{sub['subject_code']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                    share_subject_dialog(sub['name'],sub['subject_code'])
                    st.space()
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=sharebtn
                )
    else:
        st.markdown("""
                    <div style="
                    background:#FFF3CD;
                    color:black;
                    padding:14px;
                    border-radius:10px;
                    font-weight:600;
                    border:1px solid #FFE69C;
                    ">
                    No subjects found, create subjects
                    </div>
                    """, unsafe_allow_html=True)
        
        # st.warning('No subjects found,create subjects')
def teacher_tab_Attendance_Records():
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
    st.header('Attendance Records')
    teacher_id=st.session_state.teacher_data['teacher_id']
    records=get_attendance_for_teacher(teacher_id)
    if not records:
        return
    data=[]
    for r in records:
        ts=r.get('timestamp')
        data.append({
            "ts_group":ts.split(".")[0] if ts else None,
            "Time":datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject":r['subjects']['name'],
            "Subject_code":r['subjects']['subject_code'],
            "is_present":bool(r.get('is_present',False))
        })
    df=pd.DataFrame(data)
    summary=(
        df.groupby(['ts_group','Time','Subject','Subject_code'])
        .agg(
            Present_Count=('is_present','sum'),
            Total_count=('is_present','count')
        ).reset_index()
    )
    summary['Attendance_Stats']=(
        "✅"+summary['Present_Count'].astype(str)+"/"+summary['Total_count'].astype(str)+'Students'
    )
    display_df=(summary.sort_values(by='ts_group',ascending=False)
                [['Time','Subject','Subject_code','Attendance_Stats']])
    st.dataframe(display_df,width='stretch',hide_index=True)

    # st.header('Login Using Password')
    # st.markdown("""
    # <style>
    # .welcome-text{
    #     color:black;
    #     text-align:center;
    #     font-size:50px;
    #     font-weight:700;
    #     margin-top:100px;
    # }
    # </style>
    # """, unsafe_allow_html=True)
    # st.header(f"""Welcome,{teacher_data['name']}""")
def login_teacher(username,password):
    if not username or not password:
        return False
    teacher=teacher_login(username,password)
    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False

def teacher_screen_login():
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
    st.header('Login Using Password')
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
    teacher_username=st.text_input("Enter Username",placeholder='ananyaroy')
    teacher_pass=st.text_input("Enter password",type='password',placeholder='Enter Password')
    st.divider()
    btn1,btn2=st.columns(2)
    with btn1:
        if st.button('Login',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("welcome back!",icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("invalid usename or password")
    with btn2:
        if st.button('Register',type='primary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type='register'


def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False,"All Fields are required"
    if check_teacher_exists(teacher_username):
        return False,"Username allready taken"
    if teacher_pass.strip()!=teacher_pass_confirm.strip():
        return False,"Password not matches"
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"successfully created! Login Now"
    except Exception as e:
        return False,"unexpected error!"


def teacher_screen_register():
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
    st.header('Register Your teacher Profile')
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
    teacher_username=st.text_input("Enter Username",placeholder='ananyaroy')
    teacher_name=st.text_input("Enter name",placeholder='ananyaroy')
    teacher_pass=st.text_input("Enter password",type='password',placeholder='Enter Password')
    teacher_pass_confirm=st.text_input("confirm your  password",type='password',placeholder='Enter Password')
    st.divider()
    btn1,btn2=st.columns(2)
    with btn1:
        if st.button('Register',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            success,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type='login'
                st.rerun()
            else:
                st.error(message)

    with btn2:
        if st.button('Login',type='primary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type='login'
