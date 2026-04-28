
import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(
    page_title="Saraswati Shishu Mandir, Dudhana",
    page_icon="🏫",
    layout="wide"
)

# -------------------- DATA STORAGE --------------------
DATA_FILE = "students_data.csv"

COLUMNS = [
    "Admission No", "Student Name", "Age", "Gender", "Date of Birth",
    "Class", "Section", "Aadhaar Number", "Blood Group",
    "Previous School", "Admission Date", "Father Name",
    "Father Occupation", "Father Mobile", "Mother Name",
    "Mother Occupation", "Mother Mobile", "Full Address",
    "Village", "Annual Fee", "Transport Required", "Principal Name", "Paid Fee", "Remaining Fee", "Last Payment Date", "Payment Mode", "Installment Amount"
]

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    # Add any missing columns automatically for older CSV files
    for col in COLUMNS:
        if col not in df.columns:
            if col in ['Paid Fee', 'Remaining Fee', 'Installment Amount', 'Annual Fee']:
                df[col] = 0
            elif col == 'Principal Name':
                df[col] = 'Mahesh Jaiswal'
            else:
                df[col] = ''
    df = df[COLUMNS]
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.DataFrame(columns=COLUMNS)
    df.to_csv(DATA_FILE, index=False)

# -------------------- STYLING --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff7ed 0%, #fffbeb 100%);
}
.hero {
    padding: 2.5rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #7c3aed, #ea580c);
    color: white;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    margin-bottom: 1.5rem;
}
.info-card {
    background: white;
    padding: 1.5rem;
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border: 1px solid #fed7aa;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class='hero'>
    <h1>🏫 Saraswati Shishu Mandir, Dudhana</h1>
    <h3>ज्ञान • संस्कार • प्रगति</h3>
    <p>Student Management & Admission Portal</p>
    <p><strong>Principal:</strong> Mahesh Jaiswal</p>
</div>
""", unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------
k1, k2, k3 = st.columns(3)
k1.metric("👨‍🎓 Total Students", len(df))
k2.metric("🏫 Classes", "Nursery - 8")
k3.metric("📍 Location", "Dudhana")

# -------------------- SEARCH STUDENT --------------------
st.markdown('---')
st.header('🔍 Search Student Record')

search_name = st.text_input('Enter Student Name')

if search_name:
    result = df[df['Student Name'].str.contains(search_name, case=False, na=False)]
    if not result.empty:
        st.success(f"{len(result)} record(s) found")
        st.dataframe(result, width='stretch')
    else:
        st.warning('No student record found.')

# -------------------- ADMISSION FORM --------------------
st.markdown('---')
st.header('📝 New Student Admission Form')

with st.form('admission_form', clear_on_submit=True):
    admission_no = st.text_input('🎫 Admission Number')

    st.subheader('Student Information')
    c1, c2 = st.columns(2)

    with c1:
        student_name = st.text_input('👦 Student Name')
        age = st.number_input('🎂 Age', min_value=3, max_value=18, step=1)
        gender = st.selectbox('⚧ Gender', ['Male', 'Female', 'Other'])
        student_class = st.selectbox('🏫 Class', ['Nursery'] + [str(i) for i in range(1, 9)])
        section = st.selectbox('📘 Section', ['A', 'B', 'C'])

    with c2:
        dob = st.date_input('📅 Date of Birth', value=date(2016, 1, 1), min_value=date(2000, 1, 1), max_value=date.today())
        aadhaar = st.text_input('🆔 Aadhaar Number')
        blood_group = st.selectbox('🩸 Blood Group', ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
        previous_school = st.text_input('🏛️ Previous School')
        admission_date = st.date_input('📌 Admission Date', value=date.today())

    st.subheader('Parent Information')
    c3, c4 = st.columns(2)

    with c3:
        father_name = st.text_input('👨 Father Name')
        father_occupation = st.text_input('💼 Father Occupation')
        father_mobile = st.text_input('📞 Father Mobile Number')

    with c4:
        mother_name = st.text_input('👩 Mother Name')
        mother_occupation = st.text_input('💼 Mother Occupation')
        mother_mobile = st.text_input('📞 Mother Mobile Number')

    st.subheader('Address & Fee Details')
    address = st.text_area('🏠 Full Address')
    village = st.text_input('🌍 Village/Area', value='Dudhana')
    annual_fee = st.number_input('💰 Annual Fee (₹)', min_value=0, step=500)
    paid_fee = st.number_input('💵 Paid Fee (₹)', min_value=0, step=500)
    payment_date = st.date_input('📅 Fee Payment Date', value=date.today())
    payment_mode = st.selectbox('💳 Payment Mode', ['Cash', 'Online', 'Cheque'])
    installment_amount = st.number_input('📌 Installment Amount (₹)', min_value=0, step=500)
    transport_required = st.radio('🚌 Transport Required?', ['Yes', 'No'])
    remaining_fee = annual_fee - paid_fee

    submitted = st.form_submit_button('✅ Save Student Record')

if submitted:
    new_record = pd.DataFrame([{
        'Admission No': admission_no,
        'Student Name': student_name,
        'Age': age,
        'Gender': gender,
        'Date of Birth': dob,
        'Class': student_class,
        'Section': section,
        'Aadhaar Number': aadhaar,
        'Blood Group': blood_group,
        'Previous School': previous_school,
        'Admission Date': admission_date,
        'Father Name': father_name,
        'Father Occupation': father_occupation,
        'Father Mobile': father_mobile,
        'Mother Name': mother_name,
        'Mother Occupation': mother_occupation,
        'Mother Mobile': mother_mobile,
        'Full Address': address,
        'Village': village,
        'Annual Fee': annual_fee,
        'Transport Required': transport_required,
        'Principal Name': 'Mahesh Jaiswal',
        'Paid Fee': paid_fee,
        'Remaining Fee': remaining_fee,
        'Last Payment Date': payment_date,
        'Payment Mode': payment_mode,
        'Installment Amount': installment_amount
    }])

    df = pd.concat([df, new_record], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    st.success(f'✅ Student record for {student_name} saved successfully!')

# -------------------- FEE SUMMARY --------------------
st.markdown('---')
st.header('💰 Fee Management Dashboard')

if not df.empty:
    total_fee = pd.to_numeric(df['Annual Fee'], errors='coerce').fillna(0).sum()
    total_paid = pd.to_numeric(df['Paid Fee'], errors='coerce').fillna(0).sum()
    total_pending = pd.to_numeric(df['Remaining Fee'], errors='coerce').fillna(0).sum()

    f1, f2, f3 = st.columns(3)
    f1.metric('📘 Total Fees', f'₹{total_fee:,.0f}')
    f2.metric('✅ Total Collected', f'₹{total_paid:,.0f}')
    f3.metric('⏳ Pending Fees', f'₹{total_pending:,.0f}')

    due_students = df[pd.to_numeric(df['Remaining Fee'], errors='coerce').fillna(0) > 0]
    if not due_students.empty:
        st.subheader('📌 Students With Pending Fees')
        st.dataframe(
            due_students[['Admission No', 'Student Name', 'Class', 'Annual Fee', 'Paid Fee', 'Remaining Fee', 'Last Payment Date', 'Payment Mode']],
            width='stretch'
        )

# -------------------- DELETE / UPDATE STUDENT RECORD --------------------
st.markdown('---')
st.header('🛠️ Manage Student Records')

if not df.empty:
    selected_admission = st.selectbox(
        'Select Admission Number',
        options=df['Admission No'].astype(str).unique()
    )

    selected_student = df[df['Admission No'].astype(str) == selected_admission].iloc[0]

    st.subheader('📋 Selected Student Details')
    st.dataframe(selected_student.to_frame().T, width='stretch')

    col1, col2 = st.columns(2)

    with col1:
        if st.button('🔵 Update Student Record', use_container_width=True):
            st.info('Edit functionality can be added here for the selected student.')

    with col2:
        if st.button('🗑️ Delete Student Record', type='primary', use_container_width=True):
            df = df[df['Admission No'].astype(str) != selected_admission]
            df.to_csv(DATA_FILE, index=False)
            st.success(f'Student record with Admission No {selected_admission} deleted successfully!')
            st.rerun()
st.markdown('---')
st.header('📚 Complete Student Database')
st.dataframe(df, width='stretch')

# -------------------- DOWNLOAD --------------------
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label='📥 Download Student Records (CSV)',
    data=csv,
    file_name='students_data.csv',
    mime='text/csv'
)

# -------------------- FOOTER --------------------
st.markdown('---')
st.markdown("""
<div style='text-align:center;'>
    <h4>🌸 Saraswati Shishu Mandir, Dudhana</h4>
    <p>Empowering Young Minds for a Brighter Future</p>
</div>
""", unsafe_allow_html=True)




ssh-keygen -t ed25519 -C "your_email@example.com"