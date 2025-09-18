import csv
import os

FILENAME = "applications.csv"

# Create the CSV file if it doesn't exist
if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Course", "Email", "Status"])

def add_application():
    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")
    course = input("Enter Course: ")
    email = input("Enter Email: ")
    status = "Submitted"  # default

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([student_id, name, course, email, status])
    print(f"✅ Application for {name} added successfully!\n")

from tabulate import tabulate  # add at the top with imports

def view_applications():
    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("⚠️ No applications found.\n")
        return

    headers = rows[0]      # first row is header
    data = rows[1:]        # rest are student records

    print("\n===== All Applications =====")
    print(tabulate(data, headers=headers, tablefmt="grid"))
    print()


def update_status():
    student_id = input("Enter Student ID to update: ")
    new_status = input("Enter new status (Submitted/Under Review/Accepted/Rejected): ")

    rows = []
    updated = False

    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    for row in rows:
        if row[0] == student_id:
            row[4] = new_status
            updated = True

    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    if updated:
        print("✅ Status updated successfully!\n")
    else:
        print("❌ Student ID not found.\n")

def search_applications():
    choice = input("Search by (1) Course or (2) Status? Enter 1 or 2: ")

    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    headers = rows[0]
    data = rows[1:]

    results = []

    if choice == "1":
        course = input("Enter course to search: ")
        results = [row for row in data if row[2].lower() == course.lower()]
    elif choice == "2":
        status = input("Enter status to search (Submitted/Under Review/Accepted/Rejected): ")
        results = [row for row in data if row[4].lower() == status.lower()]
    else:
        print("❌ Invalid choice.")
        return

    if results:
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print("⚠️ No matching records found.")
    print()

def summary_report():
    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("⚠️ No applications found.\n")
        return

    data = rows[1:]
    total = len(data)
    status_counts = {"Submitted": 0, "Under Review": 0, "Accepted": 0, "Rejected": 0}

    for row in data:
        status = row[4]
        if status in status_counts:
            status_counts[status] += 1

    print("\n===== Summary Report =====")
    print(f"Total Applications: {total}")
    for key, val in status_counts.items():
        print(f"{key}: {val}")
    print()


def menu():
    while True:
        print("===== Student Enrollment & Application Tracker =====")
        print("1. Add Application")
        print("2. View Applications")
        print("3. Update Application Status")
        print("4. Search Applications")
        print("5. Summary Report")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            update_status()
        elif choice == "4":
            search_applications()
        elif choice == "5":
            summary_report()
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.\n")
menu()