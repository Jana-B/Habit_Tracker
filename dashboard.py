import streamlit as st
import pandas as pd
import altair as alt
from db import get_habit_collection
from datetime import datetime, timedelta

def get_habit_data(user):
    habits = get_habit_collection()
    user_habits = habits.find({"user": user})
    
    habit_data = {}
    for habit in user_habits:
        habit_data[habit['name']] = {'entries': habit['entries'], 'color': habit['color']}
    
    return habit_data

def create_chart(habit_name, habit_data):
    df = pd.DataFrame(habit_data['entries'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = df['value'].astype(int)  # Ensure integer values
    
    max_value = df['value'].max()
    y_axis = alt.Y('value:Q', 
                   title=habit_name, 
                   scale=alt.Scale(domain=(0, max_value + 1)),  # Set y-axis range
                   axis=alt.Axis(tickMinStep=1))  # Ensure integer ticks
    
    chart = alt.Chart(df).mark_line(color=habit_data['color']).encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%d-%m')),
        y=y_axis,
        tooltip=['date:T', alt.Tooltip('value:Q', title='Value', format='d')]  # 'd' format for integer
    ).properties(width=600, height=300)
    
    return chart

def display_dashboard(user):
    st.title("Your Dashboard")
    
    habit_data = get_habit_data(user)
    
    if not habit_data:
        st.write("No habits to display.")
        return
    
    for habit_name, data in habit_data.items():
        if data['entries']:
            st.altair_chart(create_chart(habit_name, data))