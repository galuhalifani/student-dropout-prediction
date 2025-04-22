import streamlit as st
import eda
import prediction

st.set_page_config(
    page_title = 'Student Dropout Prediction App',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

st.sidebar.markdown("## Welcome to the Dropout Prediction App 🎓")
st.sidebar.markdown(
    "<p style='font-size:12px;'>Use this app to analyze student dropout data and make predictions.</p>", 
    unsafe_allow_html=True
)
page = st.sidebar.selectbox('📊 **Navigate using below drop-down:** ', ('Data Insights', 'Predict Student Status'))
st.sidebar.markdown("---")
st.sidebar.write('Created by ***Galuh Alifani***')
st.sidebar.expander("See Source & Credits", expanded=False).markdown('- Data Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)\n - M.V.Martins, D. Tolledo, J. Machado, L. M.T. Baptista, V.Realinho. (2021) "Early prediction of student’s performance in higher education: a case study" Trends and Applications in Information Systems and Technologies, vol.1, in Advances in Intelligent Systems and Computing series. Springer. DOI: 10.1007/978-3-030-72657-7_16')

if page == 'Data Insights':
    eda.run()
else:
    prediction.run()