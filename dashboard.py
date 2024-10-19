import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def show_dashboard(user):
    st.header("Dashboard")
    habits = user['habits']
    
    if not habits:
        st.write("No habits to show.")
        return
    
    # Prepare habit data for visualization
    data = []
    for habit in habits:
        habit_data = {
            "Habit": habit['name'],
            "Color": habit['color'],
            "Count": habit['count'],
            "Date": datetime.now().date()
        }
        data.append(habit_data)

    df = pd.DataFrame(data)

    # Show habit data as bar chart
    st.subheader("Today's Progress")
    fig, ax = plt.subplots()
    df.plot(kind='bar', x='Habit', y='Count', color=df['Color'], ax=ax)
    st.pyplot(fig)

    st.subheader("Habit Trends")
    # Additional charts can be added here to show historical data, weekly/monthly trends