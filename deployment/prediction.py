import streamlit as st
import pandas as pd
import pickle
import json
import numpy as np
import dill

with open("reverse_mapping.txt", "r") as reverse_mapping_file:
    reverse_mapping = json.load(reverse_mapping_file)
    reverse_mapping = {int(k): v for k, v in reverse_mapping.items()}

with open("best_model.pkl", "rb") as best_model_file:
    best_model = dill.load(best_model_file)

marital_status_options = ['single', 'married', 'divorced', 'legally separated', 'facto union', 'widower']
course_options = ['Nursing', 'Social Service',
                'Journalism and Communication', 'Veterinary Nursing', 'Communication Design',
                'Animation and Multimedia Design', 'Management', 'Equinculture',
                'Oral Hygiene', 'Basic Education', 'Agronomy',
                'Advertising and Marketing Management', 'Informatics Engineering', 'Tourism',
                'Biofuel Production Technologies']
course_time_options = ['daytime', 'evening']
education_level_options = ['Illiterate',  'Informal Education', 'Primary', 'Secondary - not completed', 'Secondary',
                           'Diploma', 'Bachelors degree', 'Masters degree', 'Doctorate degree', 'Others', ]
gender_options = ['female', 'male']

def update_approved():
    """Ensure s2_approved does not exceed s2_evaluated"""
    st.session_state.s2_approved = min(st.session_state.s2_approved, st.session_state.s2_evaluated)

def update_credited():
    """Ensure s2_credited does not exceed s2_approved"""
    st.session_state.s2_credited = min(st.session_state.s2_credited, st.session_state.s2_approved)

def convertBoolean(value):
    return 1 if value else 0

def run():    
    col1, col3 = st.columns([2,2])

    with col1:
        st.title('Predict Status')
        st.markdown(
        "<p style='font-size:12px;'>"
            "To predict student's academic status (Dropout or Graduate), fill in the below form with the relevant student's information."
        "</p>", 
        unsafe_allow_html=True)
        st.image("student.jpg", use_container_width=True)
        st.markdown('---')
        st.subheader('Student Personal Information')
        name = st.text_input("Student Name", placeholder='Enter student name', help="Optional")
        marital_status = st.selectbox("Marital Status", marital_status_options)
        gender = st.radio("Gender", gender_options)
        education_level = st.selectbox("Education Level", education_level_options, index=6)
        age_at_enrollment = st.number_input("Age at Enrollment", min_value=16, max_value=60, step=1)
        st.markdown('---')

        st.subheader('Financial Information')
        is_displaced = st.checkbox("Student is Displaced from Home")
        is_scholarship_holder = st.checkbox("Student is a Scholarship Holder")
        is_debtor = st.checkbox("Student has Debt/Loans")
        is_tuition_paid = st.radio("Has Tuition Been Paid?", ['Yes', 'No'])
        st.markdown('---')

        st.subheader('Student Enrollment Information')
        course = st.selectbox("Course", course_options)
        course_time = st.radio("Course Time", course_time_options)
        admission_grade = st.number_input("Admission Grade", min_value=0.0, max_value=100.0, value=75.0, step=10.0)
        application_order = st.number_input("Application Order", min_value=0, max_value=9, step=1, help="0 - first choice; 9 last choice")
        st.markdown('---')
        
        st.subheader('Student Academic Performance')
        st.markdown("### Semester Grades")
        s1_grade = st.number_input("Semester 1 Grade", min_value=0.0, max_value=100.0, step=10.0)
        s2_grade = st.number_input("Semester 2 Grade", min_value=0.0, max_value=100.0, step=10.0)

        st.markdown("### Semester 2 Modules")
        s2_not_evaluated = st.number_input(
            "No. of Modules Not Evaluated",
            min_value=0,
            step=1,
            key="s2_not_evaluated"
        )

        if "s2_evaluated" not in st.session_state:
            st.session_state.s2_evaluated = 8
        s2_evaluated = st.number_input(
            "No. of Modules Evaluated",
            min_value=0,
            step=1,
            key="s2_evaluated",
            on_change=update_approved
        )

        if "s2_approved" not in st.session_state:
            st.session_state.s2_approved = min(st.session_state.s2_evaluated, 4)
        s2_approved = st.number_input(
            "No. of Modules Passed",
            min_value=0,
            max_value=st.session_state.get("s2_evaluated", 8),
            step=1,
            key="s2_approved",
            on_change=update_credited
        )

        if "s2_credited" not in st.session_state:
            st.session_state.s2_credited = min(st.session_state.s2_approved, 0)

        s2_credited = st.number_input(
            "No. of Modules Credited",
            min_value=0,
            max_value=st.session_state.get("s2_approved", 4),
            step=1,
            key="s2_credited",
        )
        st.markdown('---')

        st.subheader('Other Information: Macroeconomics')
        gdp = st.slider('GDP at enrollment (-4 = Recession, 0 = Stable, 4 = Economic Boom)', min_value=-4, max_value=4, value=0, step=1, help="Use this slider to select the GDP status at the time of student enrollment.")
        st.markdown('---')

        df_inf = {
            'marital_status': marital_status,
            'application_order': application_order,
            'course': course,
            'course_time': course_time,
            'education_level': education_level,
            'admission_grade': admission_grade,
            'is_displaced': int(convertBoolean(is_displaced)),
            'is_debtor': int(convertBoolean(is_debtor)),
            'is_tuition_paid': int(convertBoolean(is_tuition_paid)),
            'gender': gender,
            'is_scholarship_holder': int(convertBoolean(is_scholarship_holder)),
            'age_at_enrollment': age_at_enrollment,
            's1_grade': s1_grade,
            's2_credited': s2_credited,
            's2_evaluated': s2_evaluated,
            's2_approved': s2_approved,
            's2_grade': s2_grade,
            's2_not_evaluated': s2_not_evaluated,
            'gdp': float(gdp)
        }

    profile_data = {
    "Student Name": name if name else "Anonymous",
    "Marital Status": marital_status,
    "Gender": gender,
    "Education Level": education_level,
    "Age at Enrollment": age_at_enrollment,
    "Course": course,
    "Course Time": course_time,
    "Scholarship Holder": 'Yes' if is_scholarship_holder else 'No',
    "Tuition Paid": is_tuition_paid,
    "Semester 1 Grade": s1_grade,
    "Semester 2 Grade": s2_grade,
    "Modules Evaluated": s2_evaluated,
    "Modules Passed": s2_approved,
    "Modules Credited": s2_credited,
    "GDP at enrollment": gdp,
    "Application Order": application_order,
    "Admission Grade": admission_grade,
    "Displaced": 'Yes' if is_displaced else 'No',
    "Debtor": 'Yes' if is_debtor else 'No'
    }
    
    df_summary = pd.DataFrame(profile_data.items(), columns=["Attribute", "Value"])

    html_style = '''
        <style>
        div:has( >.element-container div.floating) {
            display: flex;
            flex-direction: column;
            position: fixed;
            max-height: 400px;
            overflow-y: auto;
            padding: 15px;
            margin-left: 3rem;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
        }

        div.floating {
            height: 100%;
        }
        </style>
    '''
    st.markdown(html_style, unsafe_allow_html=True)
    with col3:
        # Summarize the student profile
        st.markdown('<div class="floating"></div>', unsafe_allow_html=True)
        st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color: green !important;
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
        submitted = st.button('Predict Student Status')
        if submitted:
            df_inf = pd.DataFrame([df_inf])
            pred = best_model.predict(df_inf)
            prediction = reverse_mapping.get(pred[0], "Unknown")
            st.subheader(f":red[{prediction}]") if prediction == "Dropout" else st.subheader(f":green[{prediction}]")
            st.markdown('\n')

        st.subheader("Student Summary")
        with st.expander("See summary", expanded=False):
            st.table(df_summary)
if __name__ == '__main__':
    run()