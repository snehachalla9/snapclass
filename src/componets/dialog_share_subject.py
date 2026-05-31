import streamlit as st
import segno
import io
@st.dialog("share class link")
def share_subject_dialog(subject_name,subject_code):
    app_domain= "https://snapclass-main.streamlit.app"
    join_url=f"{app_domain}/?join-code={subject_code}"
    st.header("saan to join")
    qr=segno.make(join_url)
    out=io.BytesIO()
    qr.save(out,kind='png',scale=10,border=1)
    col1,col2=st.columns(2)
    with col1:
        st.markdown('### copy link')
        st.text_input('join url',join_url)
        st.text_input('subject code',subject_code)
        st.info('copy this link to share on whatsapp or email')
    with col2:
        st.markdown('###scan to join')
        st.image(out.getvalue(),caption='QRCODE for classs joining')      


