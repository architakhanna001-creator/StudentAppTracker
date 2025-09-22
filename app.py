import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os

DATA_FILE = "students.csv"

# Load existing records
if "students" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.students = pd.read_csv(DATA_FILE).to_dict(orient="records")
    else:
        st.session_state.students = []

def save_students():
    df = pd.DataFrame(st.session_state.students)
    df.to_csv(DATA_FILE, index=False)


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
    ["🏠 Home", "➕ Add Student Record", "✏️ Update Student Record", "🔍 View Student Applications", "📊 Statistics/Reports"]
)

# ---------------- HOME ----------------
if menu == "🏠 Home":
    st.subheader("Welcome 👋")
    st.info("Use the sidebar to navigate between features.")

# ---------------- ADD STUDENT RECORD ----------------
elif menu == "➕ Add Student Record":
    st.subheader("➕ Add New Student Record")
    with st.form("add_student_form"):
        name = st.text_input("Name")
        roll_no = st.text_input("Roll No")
        email = st.text_input("Email")
        course = st.text_input("Course")
        status = st.selectbox("Application Status", ["Applied", "Shortlisted", "Rejected", "Enrolled"])
        
        submit = st.form_submit_button("Add Student")
        if submit:
            st.session_state.students.append({
                "Name": name,
                "Roll No": roll_no,
                "Email": email,
                "Course": course,
                "Status": status
            })
            save_students()
            st.success(f"✅ Student {name} added successfully!")


# ---------------- UPDATE STUDENT RECORD ----------------
elif menu == "✏️ Update Student Record":
    st.subheader("✏️ Update Existing Record")

    roll_no = st.text_input("Enter Roll No of the student to update")
    if roll_no:
        # Find the student record
        student_index = next((i for i, s in enumerate(st.session_state.students) if s["Roll No"] == roll_no), None)

        if student_index is not None:
            student = st.session_state.students[student_index]

            with st.form("update_student_form"):
                # Pre-fill existing values
                name = st.text_input("Name", value=student.get("Name", ""))
                email = st.text_input("Email", value=student.get("Email", ""))
                course = st.text_input("Course", value=student.get("Course", ""))
                status = st.selectbox("Application Status", ["Applied", "Shortlisted", "Rejected", "Enrolled"], index=["Applied", "Shortlisted", "Rejected", "Enrolled"].index(student.get("Status", "Applied")))

                submit = st.form_submit_button("Update Student")
                if submit:
                    # Update the student record
                    st.session_state.students[student_index] = {
                        "Name": name,
                        "Roll No": roll_no,
                        "Email": email,
                        "Course": course,
                        "Status": status
                    }
                    save_students()
                    st.success(f"✅ Student record for Roll No {roll_no} updated successfully!")
        else:
            st.error("⚠️ Roll No not found.")


# ---------------- VIEW STUDENT APPLICATIONS ----------------
elif menu == "🔍 View Student Applications":
    st.subheader("📋 All Applications")

    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)

        # --- Search ---
        search_term = st.text_input("🔍 Search by Name or Email")

        # --- Filters ---
        courses = ["All"] + sorted(df["Course"].dropna().unique().tolist()) if "Course" in df else ["All"]
        statuses = ["All"] + sorted(df["Status"].dropna().unique().tolist())

        selected_course = st.selectbox("🎓 Filter by Course", courses)
        selected_status = st.selectbox("📌 Filter by Status", statuses)

        # --- Apply filters ---
        filtered_df = df.copy()

        if search_term:
            if "Email" in df:
                filtered_df = filtered_df[
                    filtered_df["Name"].str.contains(search_term, case=False, na=False) |
                    filtered_df["Email"].str.contains(search_term, case=False, na=False)
                ]
            else:
                filtered_df = filtered_df[
                    filtered_df["Name"].str.contains(search_term, case=False, na=False)
                ]

        if selected_course != "All" and "Course" in df:
            filtered_df = filtered_df[filtered_df["Course"] == selected_course]

        if selected_status != "All":
            filtered_df = filtered_df[filtered_df["Status"] == selected_status]

        # --- Show results ---
        st.dataframe(filtered_df, use_container_width=True)
        st.info(f"Showing {len(filtered_df)} record(s)")

        # --- Export to Excel ---
        excel_data = convert_df_to_excel(filtered_df)
        st.download_button(
            label="📥 Download Results as Excel",
            data=excel_data,
            file_name="applications.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ No student records found.")


# ---------------- STATISTICS/REPORTS ----------------
elif menu == "📊 Statistics/Reports":
    st.subheader("📊 Application Insights")
    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)
        show_pie_chart(df)
    else:
        st.warning("No data available for statistics.")
