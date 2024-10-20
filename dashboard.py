import streamlit as st
import pandas as pd
import altair as alt
from db import get_habit_collection
from datetime import datetime, timedelta

def get_habit_data(userId):
    habits = get_habit_collection()
    user_habits = habits.find({"userId": userId})
    
    habit_data = {}
    for habit in user_habits:
        habit_data[habit['name']] = habit['entries']
    
    return habit_data

def create_chart(habit_name, habit_entries, color):
    df = pd.DataFrame(habit_entries)
    df['date'] = pd.to_datetime(df['date'])
    
    chart = alt.Chart(df).mark_line(color=color).encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%d-%m')),
        y=alt.Y('value:Q', title=habit_name),
        tooltip=['date:T', 'value:Q']
    ).properties(width=600, height=300)
    
    return chart

def display_dashboard(userId):
    st.title("Your Dashboard")
    
    habit_data = get_habit_data(userId)
    
    if not habit_data:
        st.write("No habits to display.")
        return
    
    for habit_name, entries in habit_data.items():
        if entries:
            st.altair_chart(create_chart(habit_name, entries, color="#FF5733"))  # Default color example