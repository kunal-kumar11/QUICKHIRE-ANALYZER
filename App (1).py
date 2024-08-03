# Required Libraries
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
from io import StringIO

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['cv']
collection = db['user_data']

# Function to insert data into MongoDB
def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    data = {
        'name': name,
        'email': email,
        'resume_score': res_score,
        'timestamp': timestamp,
        'no_of_pages': no_of_pages,
        'predicted_field': reco_field,
        'user_level': cand_level,
        'actual_skills': skills,
        'recommended_skills': recommended_skills,
        'recommended_courses': courses
    }
    collection.insert_one(data)

# Function to generate a download link for a DataFrame
def get_table_download_link(df, filename, link_text):
    csv = df.to_csv(index=False)
    buffer = StringIO()
    buffer.write(csv)
    buffer.seek(0)
    href = f'<a href="data:file/csv;base64,{buffer.getvalue().encode().decode()}" download="{filename}">{link_text}</a>'
    return href

# Streamlit Application
def main():
    st.title("CV Analysis System")

    menu = ["User", "Admin"]
    choice = st.sidebar.selectbox("Select Activity", menu)

    if choice == 'User':
        st.subheader("User Side")
        
        # User Inputs
        name = st.text_input("Name")
        email = st.text_input("Email")
        res_score = st.number_input("Resume Score", min_value=0, max_value=100, value=0)
        timestamp = st.date_input("Timestamp")
        no_of_pages = st.number_input("Number of Pages", min_value=1, value=1)
        reco_field = st.text_input("Recommended Field")
        cand_level = st.selectbox("Candidate Level", ["Beginner", "Intermediate", "Advanced"])
        skills = st.text_area("Actual Skills")
        recommended_skills = st.text_area("Recommended Skills")
        courses = st.text_area("Recommended Courses")
        
        if st.button("Submit"):
            insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses)
            st.success("Data submitted successfully!")

    elif choice == 'Admin':
        st.subheader("Admin Side")
        
        # Admin Login
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        
        if st.button('Login'):
            if ad_user == 'briit' and ad_password == 'briit123':
                st.success("Welcome Dr Briit!")

                # Fetch data from MongoDB
                data = list(collection.find())
                df = pd.DataFrame(data)

                st.header("**User's Data**")
                st.dataframe(df)

                # Provide download link
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)

                # Admin Side Data Visualization
                st.subheader("**Pie-Chart for Predicted Field Recommendation**")
                field_counts = df['predicted_field'].value_counts()
                fig = px.pie(df, names=field_counts.index, values=field_counts.values, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)

                st.subheader("**Pie-Chart for User's Experienced Level**")
                level_counts = df['user_level'].value_counts()
                fig = px.pie(df, names=level_counts.index, values=level_counts.values, title="Pie-Chart📈 for User's Experienced Level")
                st.plotly_chart(fig)

            else:
                st.error("Wrong ID & Password Provided")

if __name__ == '__main__':
    main()
