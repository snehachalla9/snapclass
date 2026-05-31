import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.componets.dialog_auto_enroll import auto_enroll_dialog
def main():
    st.set_page_config(
        page_title='SnapClass-Making Attendance faster using AI',
        page_icon='assets/download.png'
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # Get QR join code
    join_code = st.query_params.get('join-code')

    # Auto switch to student
    if join_code and st.session_state.login_type != 'student':
        st.session_state.login_type = 'student'
        st.rerun()

    # Screens
    match st.session_state['login_type']:

        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case None:
            home_screen()

    # Open enrollment dialog
    if join_code and st.session_state.login_type == 'student':
        auto_enroll_dialog(join_code)


main()