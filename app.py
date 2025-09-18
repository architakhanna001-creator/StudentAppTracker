import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO

FILENAME = "applications.csv"

# Ensure CSV file exists
if not os.path.exists(FILENAME):
    df = pd.DataFrame(columns=["ID", "Name", "Course", "Email", "Status"])
    df.to_csv(FILENAME, index=False)

def load_data():
    df = pd.read_csv(FILENAME)
    df["ID"] = df["ID"].astype(str)  # force all IDs as strings
    return df

def save_data(df):
    df["ID"] = df["ID"].astype(str)  # keep IDs as strings before saving
    df.to_csv(FILENAME, index=False)


st.set_page_config(page_title="🎓 Student Enrollment & Application Tracker", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 Student Application Tracker</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Manage, Track & Report Student Applications</h4>", unsafe_allow_html=True)
st.markdown("---")


def convert_df_to_excel(df):
    output = BytesIO()
    try:
        # Try using xlsxwriter first
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Applications")
    except ImportError:
        # Fallback to openpyxl if xlsxwriter is not installed
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Applications")
    return output.getvalue()


menu = ["Add Application", "View Applications", "Update Status", "Update Record", "Reports"]
choice = st.sidebar.selectbox("Menu", menu)


df = load_data()

if choice == "Add Application":
    st.subheader("➕ Add New Student Application")
    id = st.text_input("Student ID")
    name = st.text_input("Name")
    course = st.text_input("Course")
    email = st.text_input("Email")
    status = "Submitted"

    if st.button("Add Application"):
        new_entry = pd.DataFrame([[str(id), name, course, email, status]],
                                 columns=df.columns)
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        st.success(f"✅ Application for {name} added successfully!")

elif choice == "View Applications":
    st.subheader("📋 All Applications")

    # --- Search ---
    search_term = st.text_input("🔍 Search by Name or Email")

    # --- Filters ---
    courses = ["All"] + sorted(df["Course"].dropna().unique().tolist())
    statuses = ["All"] + sorted(df["Status"].dropna().unique().tolist())

    selected_course = st.selectbox("🎓 Filter by Course", courses)
    selected_status = st.selectbox("📌 Filter by Status", statuses)

    # --- Apply filters ---
    filtered_df = df.copy()

    if search_term:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(search_term, case=False, na=False) |
            filtered_df["Email"].str.contains(search_term, case=False, na=False)
        ]

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["Status"] == selected_status]

    # --- Show results ---
    st.dataframe(filtered_df)

    st.info(f"Showing {len(filtered_df)} record(s)")
    # --- Export to Excel ---
    excel_data = convert_df_to_excel(filtered_df)
    st.download_button(
        label="📥 Download Results as Excel",
        data=excel_data,
        file_name="applications.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)



elif choice == "Update Status":
    st.subheader("✏️ Update Application Status")
    student_id = st.text_input("Enter Student ID")
    new_status = st.selectbox("New Status", ["Submitted", "Under Review", "Accepted", "Rejected"])

    if st.button("Update"):
        if any(df["ID"].astype(str) == str(student_id)):
            df.loc[df["ID"].astype(str) == str(student_id), "Status"] = new_status
            save_data(df)
            st.success("✅ Status updated successfully!")
        else:
            st.error("❌ Student ID not found.")


elif choice == "Reports":
    st.subheader("📊 Summary Report")
    st.write(f"Total Applications: {len(df)}")
    st.write(df["Status"].value_counts())

    # Status Distribution Pie Chart
    status_counts = df['Status'].value_counts()

    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%',
           colors=['#4CAF50', '#F44336', '#FFC107'], startangle=90)
    ax.set_title("Application Status Distribution")

    st.pyplot(fig)


elif choice == "Update Record":
    st.subheader("📝 Update Student Record")
    
    # Dropdown instead of text input (safer)
    student_id = st.selectbox("Select Student ID", df["ID"].astype(str).unique())

    if student_id:
        # Get current details
        record = df[df["ID"] == student_id].iloc[0]

        new_id = st.text_input("Student ID", record["ID"])
        new_name = st.text_input("Name", record["Name"])
        new_course = st.text_input("Course", record["Course"])
        new_email = st.text_input("Email", record["Email"])
        new_status = st.selectbox("Status", ["Submitted", "Under Review", "Accepted", "Rejected"], 
                                  index=["Submitted", "Under Review", "Accepted", "Rejected"].index(record["Status"]))

        if st.button("Update Record"):
            df.loc[df["ID"] == student_id, ["ID", "Name", "Course", "Email", "Status"]] = [new_id, new_name, new_course, new_email, new_status]
            save_data(df)
            st.success(f"✅ Record for {new_name} updated successfully!")
