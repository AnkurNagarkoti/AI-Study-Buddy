import streamlit as st
import pandas as pd
from frontend.api_client import get_quiz_history
import datetime

def dashboard_page():
    st.title("📊 Progress Dashboard")
    
    history = get_quiz_history()
    
    if not history:
        st.info("No quiz history found. Take a quiz to see your progress!")
        return

    # Convert to DataFrame
    try:
        df = pd.DataFrame(history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return
    
    # Filters
    st.subheader("Performance Analytics")
    col1, col2 = st.columns([1, 3])
    with col1:
        time_filter = st.selectbox("Time Range", ["Last 7 Days", "Last 30 Days", "All Time"])
    
    if time_filter == "Last 7 Days":
        cutoff = datetime.date.today() - datetime.timedelta(days=7)
        df_filtered = df[df['date'] >= cutoff]
    elif time_filter == "Last 30 Days":
        cutoff = datetime.date.today() - datetime.timedelta(days=30)
        df_filtered = df[df['date'] >= cutoff]
    else:
        df_filtered = df
        
    if df_filtered.empty:
        st.warning("No data for the selected time range.")
    else:
        # Metrics
        c1, c2, c3 = st.columns(3)
        avg_score = df_filtered['score'].mean()
        total_quizzes = len(df_filtered)
        best_topic = df_filtered.groupby('topic')['score'].mean().idxmax() if not df_filtered.empty else "N/A"
        
        c1.metric("Average Score", f"{avg_score:.1f}")
        c2.metric("Total Quizzes", total_quizzes)
        c3.metric("Best Topic", best_topic)
        
        # Charts
        st.subheader("Score Trend")
        st.line_chart(df_filtered.set_index('timestamp')['score'])
    
    # Recent History Cards
    st.subheader("Recent History")
    
    # Sort by timestamp desc
    history_sorted = sorted(history, key=lambda x: x['timestamp'], reverse=True)
    
    for i, item in enumerate(history_sorted):
        # Create a card-like container
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            
            # Format timestamp
            try:
                dt = pd.to_datetime(item['timestamp'])
                date_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = item['timestamp']
            
            with c1:
                st.markdown(f"### 📝 {item['topic']}")
                st.caption(f"Completed on {date_str}")
                
            with c2:
                st.metric("Score", f"{item['score']}/{item['total_questions']}")
            
            with c3:
                # Calculate percentage
                if item['total_questions'] > 0:
                    pct = (item['score'] / item['total_questions']) * 100
                    if pct >= 80:
                        st.success(f"{pct:.0f}%")
                    elif pct >= 50:
                        st.warning(f"{pct:.0f}%")
                    else:
                        st.error(f"{pct:.0f}%")
                else:
                    st.write("N/A")
