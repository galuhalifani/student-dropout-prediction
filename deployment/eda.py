import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
from ucimlrepo import fetch_ucirepo

plt.rcParams.update({
    "axes.labelpad": 20,
    "axes.labelsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14
})
def transform_data():
    def load_data():
        data = fetch_ucirepo(id=697)
        df = data.data.original
        return df

    def renameColumns(df):
        old_columns_names = df.columns
        new_column_names = [
            "marital_status",
            "application_mode",
            "application_order",
            "course",
            "course_time",
            "education_level",
            "previous_grade",
            "nationality",
            "mother_education",
            "father_education",
            "mother_occupation",
            "father_occupation",
            "admission_grade",
            "is_displaced",
            "has_special_needs",
            "is_debtor",
            "is_tuition_paid",
            "gender",
            "is_scholarship_holder",
            "age_at_enrollment",
            "is_international",
            "s1_credited",
            "s1_enrolled",
            "s1_evaluated",
            "s1_approved",
            "s1_grade",
            "s1_not_evaluated",
            "s2_credited",
            "s2_enrolled",
            "s2_evaluated",
            "s2_approved",
            "s2_grade",
            "s2_not_evaluated",
            "unemployment_rate",
            "inflation_rate",
            "gdp",
            "status"
        ]

        col_rename_mapping = dict(zip(old_columns_names, new_column_names))

        df_renamed = df.rename(columns=col_rename_mapping)
        return df_renamed

    def unencode(df):
        gender_dict = {
            0: "female",
            1: "male"
        }

        marital_status_dict = {
            1: "single",
            2: "married",
            3: "widower",
            4: "divorced",
            5: "facto union",
            6: "legally separated"
        }

        course_time_dict = {
            0: "evening",
            1: "daytime"
        }

        application_mode_dict = {
            1: "1st phase - general contingent",
            2: "Ordinance No. 612/93",
            5: "1st phase - special contingent (Azores Island)",
            7: "Holders of other higher courses",
            10: "Ordinance No. 854-B/99",
            15: "International student (bachelor)",
            16: "1st phase - special contingent (Madeira Island)",
            17: "2nd phase - general contingent",
            18: "3rd phase - general contingent",
            26: "Ordinance No. 533-A/99, item b2) (Different Plan)",
            27: "Ordinance No. 533-A/99, item b3 (Other Institution)",
            39: "Over 23 years old",
            42: "Transfer",
            43: "Change of course",
            44: "Technological specialization diploma holders",
            51: "Change of institution/course",
            53: "Short cycle diploma holders",
            57: "Change of institution/course (International)"
        }

        course_dict = {
            33: "Biofuel Production Technologies",
            171: "Animation and Multimedia Design",
            8014: "Social Service (evening attendance)",
            9003: "Agronomy",
            9070: "Communication Design",
            9085: "Veterinary Nursing",
            9119: "Informatics Engineering",
            9130: "Equinculture",
            9147: "Management",
            9238: "Social Service",
            9254: "Tourism",
            9500: "Nursing",
            9556: "Oral Hygiene",
            9670: "Advertising and Marketing Management",
            9773: "Journalism and Communication",
            9853: "Basic Education",
            9991: "Management (evening attendance)"
        }

        nationality_dict = {
            1: "Portuguese", 2: "German", 6: "Spanish", 11: "Italian",
            13: "Dutch", 14: "English", 17: "Lithuanian", 21: "Angolan",
            22: "Cape Verdean", 24: "Guinean", 25: "Mozambican", 26: "Santomean",
            32: "Turkish", 41: "Brazilian", 62: "Romanian", 100: "Moldova (Republic of)",
            101: "Mexican", 103: "Ukrainian", 105: "Russian", 108: "Cuban",
            109: "Colombian"
        }

        education_qualification_dict = {
            1: "Secondary",
            2: "Bachelors degree",
            3: "Higher education (diploma)",
            4: "Masters degree",
            5: "Doctorate degree",
            6: "Higher education (diploma)",
            9: "12th grade - not completed",
            10: "11th grade - not completed",
            11: "7th grade",
            12: "11th-grade",
            13: "2nd-year complementary high school",
            14: "10th grade",
            15: "10th grade - not completed",
            18: "General commerce course",
            19: "Basic 3rd cycle (9th-11th)",
            20: "Complementary high school",
            22: "Technical/professional course",
            25: "Incomplete high school",
            26: "7th grade",
            27: "Basic 2nd cycle (6th-8th)",
            29: "9th grade - not completed",
            30: "8th grade",
            31: "Administration & commerce course",
            33: "Supplementary accounting & admin",
            34: "Unknown",
            35: "Illiterate",
            36: "Can read, no formal schooling",
            37: "Basic 1st cycle (4th-5th)",
            38: "Basic 2nd cycle (6th-8th)",
            39: "Technological specialization",
            40: "Higher education (diploma)",
            41: "Specialized higher studies",
            42: "Professional higher technical course",
            43: "Masters degree",
            44: "Doctorate degree"
        }

        parent_occupation_dict = {
            0: "Student",
            1: "Govt & executive leaders",
            2: "Specialists (science, law, etc.)",
            3: "Technicians & associate professionals",
            4: "Admin staff",
            5: "Personal services & sales",
            6: "Farmers & agriculture",
            7: "Skilled industry workers",
            8: "Machine operators",
            9: "Unskilled workers",
            10: "Military professions",
            90: "Other",
            99: "Other",
            101: "Military officers",
            102: "Military sergeants",
            103: "Military professions",
            112: "Admin & commercial managers",
            114: "Hotel & service managers",
            121: "Scientists & engineers",
            122: "Healthcare professionals",
            123: "Teachers",
            124: "Finance & admin specialists",
            131: "Science & engineering technicians",
            132: "Health technicians",
            134: "Legal, sports & culture techs",
            135: "IT technicians",
            141: "Secretaries & office workers",
            143: "Accounting & financial clerks",
            144: "Other admin support",
            151: "Personal service workers",
            152: "Sellers",
            153: "Care & welfare workers",
            154: "Security & protection services",
            161: "Commercial farmers",
            163: "Subsistence farmers & fishermen",
            171: "Construction workers (non-electricians)",
            172: "Metalworkers",
            174: "Electricians & electronics workers",
            175: "Food, textile, & wood industry workers",
            181: "Machine operators",
            182: "Assembly workers",
            183: "Drivers & transport operators",
            192: "Unskilled farm & fishery workers",
            193: "Unskilled industry & transport workers",
            194: "Kitchen assistants",
            195: "Street vendors (non-food)"
        }

        df["gender"] = df["gender"].replace(gender_dict)
        df["marital_status"] = df["marital_status"].replace(marital_status_dict)
        df["course_time"] = df["course_time"].replace(course_time_dict)
        df["application_mode"] = df["application_mode"].replace(application_mode_dict)
        df["course"] = df["course"].replace(course_dict)
        df["nationality"] = df["nationality"].replace(nationality_dict)
        df["education_level"] = df["education_level"].replace(education_qualification_dict)
        df["mother_education"] = df["mother_education"].replace(education_qualification_dict)
        df["father_education"] = df["father_education"].replace(education_qualification_dict)
        df["mother_occupation"] = df["mother_occupation"].replace(parent_occupation_dict)
        df["father_occupation"] = df["father_occupation"].replace(parent_occupation_dict)

        return df

    def convert_grades(df):
        df['s1_grade'] = df['s1_grade'] / 20 * 100
        df['s2_grade'] = df['s2_grade'] / 20 * 100
        df['admission_grade'] = df['admission_grade'] / 200 * 100
        df['previous_grade'] = df['previous_grade'] / 200 * 100
        return df

    def remove_zero_score_grads(df):
        df["avg_grade"] = (df["s1_grade"] + df["s2_grade"]) / 2
        df = df[~((df['avg_grade'] == 0) & (df['status'] == 'Graduate'))]
        return df
    
    df = load_data()
    df_renamed = renameColumns(df)
    df_unencoded = unencode(df_renamed)
    df_converted = convert_grades(df_unencoded)
    df_cleaned = remove_zero_score_grads(df_converted)

    return pd.DataFrame(df_cleaned)

def format_label(label):
        """Converts snake_case labels to readable format, e.g., 'marital_status' -> 'Marital Status'."""
        if(label == 's1_grade'):
            return 'Semester 1 Grade'
        if(label == 's2_grade'):
            return 'Semester 2 Grade'
        if(label == 'avg_grade'):
            return 'Average Grade'
        return label.replace("_", " ").title()

def create_option_selector(title, options):
    """Creates a select box with formatted option labels while keeping the original values."""
    formatted_options = {format_label(opt): opt for opt in options}
    selected_label = st.selectbox(title, list(formatted_options.keys()))
    return formatted_options[selected_label]

def create_bar_plot(df, column):
    fig, ax = plt.subplots(figsize=(5, 2))
    status_counts = df[column].value_counts()
    percentages = status_counts / status_counts.sum() * 100
    labels = [f"{label} ({percent:.1f}%)" for label, percent in zip(status_counts.index, percentages)]
    
    status_counts.plot(kind="pie", ax=ax, legend=True, startangle=90, cmap="Set2", labels=None, autopct='%1.1f%%')
    ax.legend(labels=labels, loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_title(f"{format_label(column)} Distribution")
    ax.set_ylabel("")
    st.pyplot(fig, bbox_inches='tight') 

def create_histogram(df, column):
    fig, ax = plt.subplots(figsize=(10, 3))
    sns.histplot(df[column], bins=20, kde=True, ax=ax)
    ax.set_title(f"Distribution of {format_label(column)}")
    ax.set_xlabel(format_label(column))
    ax.set_ylabel("Count")
    st.pyplot(fig)

def topCoursesByEnrollmentOrGrade(dfa):
    filter1,filter2 = st.columns(2)
    with filter1:
        number_filter = int(
            st.number_input('Select # courses', 
                            min_value=5, 
                            max_value=int(dfa['course'].nunique()), 
                            step=1, 
                            value=5, 
                            help='Select top x courses',
                            key='top_courses'),
        )
    with filter2:
        option = st.selectbox('Select parameter : ', ('Enrollment', 'Grade'))

    if option == 'Enrollment':
        top_courses = dfa["course"].value_counts().nlargest(number_filter)
        x_values = top_courses.values
        y_values = top_courses.index
        xlabel = "Number of Students"
    else:
        top_courses = (
            dfa.groupby("course")["avg_grade"]
            .mean()
            .nlargest(number_filter)
        )
        x_values = top_courses.values
        y_values = top_courses.index
        xlabel = "Average Grade"

    fig_width = 8
    fig_height = number_filter * 0.8
    fig = plt.figure(figsize=(fig_width, fig_height))
    sns.barplot(x=x_values, y=y_values)
    plt.title(f"\nTop {number_filter} Courses by {option}\n", fontsize=24)
    plt.xlabel(xlabel,fontsize=16)
    plt.ylabel("Course", fontsize=16, labelpad=20)
    plt.yticks(fontsize=14) 
    plt.xticks(fontsize=14) 
    st.pyplot(fig)

def courseDropoutRate(dfa, option):
    dfa_course_agg = dfa.groupby(option).agg(
        dropout_rate=("status", lambda x: (x == "Dropout").mean() * 100),
        graduation_rate=("status", lambda x: (x == "Graduate").mean() * 100),
        enrollment_rate=("status", lambda x: (x == "Enrolled").mean() * 100),
    ).reset_index().sort_values(by="dropout_rate", ascending=False)

    fig_width = 10
    fig_height = min(len(dfa_course_agg), 10)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    ax.barh(dfa_course_agg[option], dfa_course_agg["dropout_rate"], label="Dropout Rate", color='maroon')
    ax.barh(dfa_course_agg[option], dfa_course_agg["graduation_rate"], 
        left=dfa_course_agg["dropout_rate"], 
        label="Graduation Rate", color="green")
    ax.barh(dfa_course_agg[option], dfa_course_agg["enrollment_rate"], 
        left=dfa_course_agg["dropout_rate"] + dfa_course_agg["graduation_rate"],
        label="Enrolled Rate", color="lightblue")

    ax.set_xlabel("Percentage (%)")
    ax.set_ylabel(option)
    ax.set_title(f"Dropout rates by {option}")
    ax.legend()

    if (option == ('is_tuition_paid' or 'is_scholarship_holder')):
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["No", "Yes"]) 

    ax.set_xlim(0, 100)
    ax.invert_yaxis() 
    st.pyplot(fig)

def gradeByStatus(dfa, option):
    fig = plt.figure(figsize=(12, 5))
    sns.boxplot(data=dfa, x="status", y=option, order=["Dropout", "Enrolled", "Graduate"])
    plt.title("Range of Grades by Student Status")
    plt.xlabel("Student Status")
    plt.ylabel(f"{option}")
    st.pyplot(fig)

def admissionGradeVsSemesterGrade(dfa):
    fig = plt.figure(figsize=(10,3))
    bins = [0, 50, 70, 100]
    labels = ['0-50', '50-70', '70-100']
    dfa["avg_admission_grade_bin"] = pd.cut(dfa["admission_grade"], bins=bins, labels=labels, include_lowest=True)
    admission_grade_grouped = dfa.groupby("avg_admission_grade_bin", observed=False)["avg_grade"].mean()
    admission_grade_grouped.plot(kind="bar", color="red", alpha=0.7)
    plt.title("Avg Admission Grade by Average Grade")
    plt.ylabel("Avg Grade")
    plt.xlabel("Admission Grade")
    st.pyplot(fig)

df = pd.read_csv('./student_data_analysis.csv')
def run():

    html_style = '''
        <style>
        .block-container {
            padding-left: 5rem;
            padding-right: 15rem;
            margin-left: 15rem !important;
            margin-right: 15rem !important;
            margin-top: -3rem!important;
        }
        </style>
    '''
    st.markdown(html_style, unsafe_allow_html=True)
    st.title('Student Dropout Analysis')
    st.image("student2.jpg", use_container_width=True)
    with st.expander("Dataset Information", expanded=False):
        st.markdown(
        "<p style='font-size:12px;'>"
            "Dataset is retrived from UCI Machine Learning Repository that contains 4,000 records of students from several higher education institutions in Portugal. The dataset includes information known at the time of student enrollment: academic path, demographics, and social-economic factors. "
            "<br><br> See sidebar for data source reference and credits."
        "</p>", 
        unsafe_allow_html=True)
    st.markdown('---')
    
    st.header('Student Distributions')
    st.subheader('Demographic')

    demographic_col = create_option_selector('Select parameter:', ['status', 'marital_status', 'age_at_enrollment', 'gender', 'course', 'is_international', 'is_tuition_paid', 'is_scholarship_holder'])
    if demographic_col == 'age_at_enrollment':
        create_histogram(df, demographic_col)
    else:
        create_bar_plot(df, demographic_col)

    st.subheader('Grade Distribution')
    grade_col = create_option_selector('Select parameter:', ['s1_grade', 's2_grade', 'avg_grade', 'admission_grade', 'previous_grade'])
    create_histogram(df, grade_col)

    st.header('Top Courses by Enrollment & Grade')
    topCoursesByEnrollmentOrGrade(df)

    st.header('Dropout Rates by Courses')
    dropout_col = create_option_selector('Select parameter:', ['course', 'gender', 'course_time', 'marital_status', 'is_tuition_paid', 'is_scholarship_holder'])
    courseDropoutRate(df, dropout_col)

    st.header('Grade by Status')
    grade_status_col = create_option_selector('Select parameter:', ['avg_grade', 's1_grade', 's2_grade', 'previous_grade', 'admission_grade'])
    gradeByStatus(df, grade_status_col)

    st.header('Admission Grade and Semester Grade')
    admissionGradeVsSemesterGrade(df)

    st.markdown('---')
    st.header('Explore Dataset (Pre-Processed)')
    st.dataframe(df)

if __name__ == '__main__':
    run()