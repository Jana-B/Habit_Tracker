import streamlit as st
from models import Habit
from database import db
import matplotlib.pyplot as plt

def dashboard_tab(user_id):
    if "habits" not in st.session_state:
        habit = Habit(db, user_id)
        st.session_state.habits = habit.get_user_habits()

    habits = st.session_state.habits

    st.subheader("Habit Dashboard")

    # Display habit stats and graphs
    for h in habits:
        st.write(f"**{h['name']}** - Today's Count: {h['count']}")
        
        # Plot historical habit data (per day)
        if len(h['history']) > 0:
            dates = [entry['date'] for entry in h['history']]
            counts = [entry['count'] for entry in h['history']]
            st.line_chart({"dates": dates, "counts": counts})

    # Show a pie chart for a quick summary
    fig, ax = plt.subplots()
    colors = [h['color'] for h in habits]
    counts = [h['count'] for h in habits]
    labels = [h['name'] for h in habits]
    ax.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%')
    st.pyplot(fig)