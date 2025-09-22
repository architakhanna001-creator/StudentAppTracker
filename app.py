import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Application Tracker",
    page_icon="🎓",
    layout="wide"
)

# ---------------- TITLE & DESCRIPTION ----------------
st.title("🎓 Student Application Tracker")
st.markdown(
    """
    Manage student applications with ease!  
    ✅ Add, update, and search student records  
    ✅ Export data to Excel  
    ✅ Visualize application statistics  

    ---
    """
)

# ---------------- DATA STORAGE ----------------
if "students" not in st.session_state:
    st.session_state.students = []

# ---------------- FUNCTIONS ----------------
def convert_df_to_excel(df):
    output = BytesIO()
    try:
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Students")
    except ImportError:
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Students")
    return output.getvalue()

def show_pie_chart(df):
    fig, ax = plt.subplots(figsize=(4, 4))
    df["Status"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax, startangle=90)
    ax.set_ylabel("")
    ax.set_title("📊 Application Status Distribution")
    st.pyplot(fig)

# ---------------- SIDEBAR MENU ----------------
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🏠 Home", "➕ Add Student", "✏️ Update Student", "🔍 View Students", "📊 Statistics"]
)

# ---------------- HOME ----------------
if menu == "🏠 Home":
    st.subheader("Welcome 👋")
    st.info("Use the sidebar to navigate between features.")

# ---------------- ADD STUDENT ----------------
elif menu == "➕ Add Student":
    st.subheader("➕ Add New Student Record")
    with st.form("add_student_form"):
        name = st.text_input("Name")
        roll_no = st.text_input("Roll No")
        status = st.selectbox("Application Status", ["Applied", "Shortlisted", "Rejected", "Enrolled"])
        submit = st.form_submit_button("Add Student")
        if submit:
            st.session_state.students.append({"Name": name, "Roll No": roll_no, "Status": status})
            st.success(f"✅ Student {name} added successfully!")

# ---------------- UPDATE STUDENT ----------------
elif menu == "✏️ Update Student":
    st.subheader("✏️ Update Existing Record")
    roll_no = st.text_input("Enter Roll No to Update")
    new_status = st.selectbox("New Status", ["Applied", "Shortlisted", "Rejected", "Enrolled"])
    if st.button("Update"):
        updated = False
        for student in st.session_state.students:
            if student["Roll No"] == roll_no:
                student["Status"] = new_status
                updated = True
                st.success(f"✅ Record for Roll No {roll_no} updated!")
                break
        if not updated:
            st.error("⚠️ Roll No not found.")

# ---------------- VIEW STUDENTS ----------------
elif menu == "🔍 View Students":
    st.subheader("📋 Student Records")
    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)
        st.dataframe(df, use_container_width=True)

        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="📥 Download Excel",
            data=excel_data,
            file_name="students.xlsx",
            mime="application/vnd.ms-excel",
        )
    else:
        st.warning("No student records found.")

# ---------------- STATISTICS ----------------
elif menu == "📊 Statistics":
    st.subheader("📊 Application Insights")
    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)
        show_pie_chart(df)
    else:
        st.warning("No data available for statistics.")
