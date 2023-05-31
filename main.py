import streamlit as st
import pandas as pd


def load_excel_data(file_path):
    # Load the Excel file into a DataFrame
    excel_data = pd.read_excel(file_path, sheet_name=None)
    return excel_data


def filter_unpaid_students(data, selected_sheet, selected_month):
    # Select the specified sheet
    sheet_data = data[selected_sheet]

    # Select the necessary columns for processing
    required_columns = ['NOM', 'PRENOMS', selected_month]
    filtered_data = sheet_data[required_columns].copy()

    # Replace None values with "Impayé" in the selected month
    filtered_data[selected_month] = filtered_data[selected_month].fillna("Impayé")

    # Filter students who haven't paid this month
    unpaid_students = filtered_data[filtered_data[selected_month] == "Impayé"]

    # Create a new column to expand the table
    filtered_data['AUTRE_COLONNE'] = None

    return unpaid_students, filtered_data


import pandas as pd

def display_student_unpaid_months(data, student_name, month):
    # Filter the data for the selected student
    student_data = data[(data['NOM'] + ' ' + data['PRENOMS']) == student_name]

    # Replace None values with "Impayé" in the specified month
    student_data[month] = student_data[month].fillna("Impayé")

    # Check if the student has paid for the specified month
    has_paid = student_data[month].values[0] != "Impayé"

    # Create a DataFrame to display the student's information and payment status
    student_info = pd.DataFrame(columns=['Nom', 'Prénoms', 'Statut paiement'])
    if not student_data.empty:
        if has_paid:
            student_info.loc[0] = [student_data['NOM'].values[0], student_data['PRENOMS'].values[0], "Payé"]
        else:
            student_info.loc[0] = [student_data['NOM'].values[0], student_data['PRENOMS'].values[0], "Impayé"]

    return student_info


# Create a sidebar for page selection
def main():
    page = st.sidebar.selectbox("Veuillez sélectionner une page", ["Analyse globale", "Analyse par étudiant"])

    if page == "Analyse globale":
        st.image('logo.jpeg')
        st.markdown("<h1 style='text-align: center; color: black;'>Mon tableau de bord d'analyse automatisée</h1>",
                unsafe_allow_html=True)
        # Home page content
        uploaded_file = st.file_uploader("Veuillez sélectionner le bon fichier Excel", type=["xls", "xlsx"])
        if uploaded_file:
            # Load the Excel data into a DataFrame
            excel_data = load_excel_data(uploaded_file)

            # List the sheets in the Excel file
            sheet_names = list(excel_data.keys())

            st.title("Mon tableau de bord d'analyse automatisée")
            st.write("Veuillez sélectionner ce que vous voulez faire.")

            # Store the uploaded file and data in a session state
            st.session_state.uploaded_file = uploaded_file
            st.session_state.excel_data = excel_data
            st.session_state.sheet_names = sheet_names

            # Select the sheet for filtering unpaid students
            st.session_state.selected_sheet = st.selectbox("Veuillez sélectionner uune classe", sheet_names)
            selected_month = st.selectbox("Veuillez sélectionner un mois",
                                        ['FEVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN', "JUILlET","AOÛT","SEPTEMBRE","OCTOBRE"])
            unpaid_students, filtered_data = filter_unpaid_students(excel_data, st.session_state.selected_sheet,
                                                                    selected_month)
            st.table(unpaid_students)

    elif page == "Analyse par étudiant":
        # Unpaid Months page content
        st.title("Analyse par étudiant")
        students_data = st.session_state.excel_data[st.session_state.selected_sheet]
        student_names = students_data['NOM'] + ' ' + students_data['PRENOMS']
        selected_student = st.selectbox("Veuillez sélectionner un étudiant", student_names)

        if selected_student:
            # Access the uploaded file and data from the session state
            excel_data = st.session_state.excel_data
            selected_month = st.selectbox("Veuillez sélectionner un mois",
                                        ['FEVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN',"JUILLET","AOÛT"])

            # Filter unpaid students
            unpaid_students, filtered_data = filter_unpaid_students(excel_data, st.session_state.selected_sheet,
                                                                    selected_month)
                                                                    


            # Display the student's payment status
            student_info = display_student_unpaid_months(filtered_data, selected_student, selected_month)
            st.table(student_info)

# Run the app
if __name__ == "__main__":
    main()
