import streamlit as st
import plotly.graph_objects as go
from utils.data_manager import DataManager

def show_dashboard():
    if 'user_email' not in st.session_state:
        st.warning("Please login to access the dashboard")
        return

    st.title("🏃‍♂️ Fitness Dashboard")
    data_manager = DataManager()
    user_metrics = data_manager.get_user_metrics(st.session_state.user_email)

    if user_metrics.empty:
        st.info("No data available. Please add your metrics in the Profile section.")
        return

    # Custom color scheme
    custom_colors = ['#FF4B4B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692']

    # First row - Summary Cards
    latest_metrics = data_manager.get_latest_metrics(st.session_state.user_email)

    if latest_metrics is not None:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        # Fix: Initialize delta before using it
        delta = "N/A"

        if len(user_metrics) >= 2:
            previous_weight = user_metrics['weight'].iloc[-2]
            delta = f"{latest_metrics['weight'] - previous_weight:.1f} kg"

        with col1:
            st.metric("Weight", f"{latest_metrics['weight']} kg", delta=delta)

        with col2:
            st.metric("Height", f"{latest_metrics['height']} cm")

        with col3:
            bmi_value = data_manager.calculate_bmi(latest_metrics['weight'], latest_metrics['height'])
            st.metric("BMI", f"{bmi_value:.2f}")

        with col4:
            st.metric("Exercise", f"{latest_metrics['exercise_minutes']} mins")

    # Progress Charts
    st.subheader("📊 Fitness Progress")

    # Weight and BMI Trends
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Weight Progress", "BMI Trend"])

        with tab1:
            fig_weight = go.Figure()
            fig_weight.add_trace(go.Scatter(
                x=user_metrics['date'],
                y=user_metrics['weight'],
                mode='lines+markers',
                name='Weight',
                line=dict(color=custom_colors[0], width=3),
                marker=dict(size=8)
            ))
            fig_weight.update_layout(
                title='Weight Progress Over Time',
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig_weight, use_container_width=True)

        with tab2:
            user_metrics['bmi'] = user_metrics.apply(
                lambda row: data_manager.calculate_bmi(row['weight'], row['height']),
                axis=1
            )
            fig_bmi = go.Figure()
            fig_bmi.add_trace(go.Scatter(
                x=user_metrics['date'],
                y=user_metrics['bmi'],
                mode='lines+markers',
                name='BMI',
                line=dict(color=custom_colors[1], width=3),
                marker=dict(size=8)
            ))
            fig_bmi.update_layout(
                title='BMI Trend Over Time',
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig_bmi, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Activity and Health Metrics
    st.subheader("💪 Activity & Health")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_exercise = go.Figure()
        fig_exercise.add_trace(go.Bar(
            x=user_metrics['date'],
            y=user_metrics['exercise_minutes'],
            name='Exercise Duration',
            marker_color=custom_colors[2]
        ))
        fig_exercise.update_layout(
            title='Daily Exercise Minutes',
            template='plotly_dark',
            height=300
        )
        st.plotly_chart(fig_exercise, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_calories = go.Figure()
        fig_calories.add_trace(go.Bar(
            x=user_metrics['date'],
            y=user_metrics['calories_burned'],
            name='Calories Burned',
            marker_color=custom_colors[3]
        ))
        fig_calories.update_layout(
            title='Daily Calories Burned',
            template='plotly_dark',
            height=300
        )
        st.plotly_chart(fig_calories, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Health Metrics
    st.subheader("❤️ Health Metrics")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_sleep = go.Figure()
        fig_sleep.add_trace(go.Scatter(
            x=user_metrics['date'],
            y=user_metrics['sleep_hours'],
            mode='lines+markers',
            name='Sleep Hours',
            line=dict(color=custom_colors[4], width=3),
            marker=dict(size=8)
        ))
        fig_sleep.update_layout(
            title='Sleep Pattern',
            template='plotly_dark',
            height=300
        )
        st.plotly_chart(fig_sleep, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_stress = go.Figure()
        fig_stress.add_trace(go.Scatter(
            x=user_metrics['date'],
            y=user_metrics['stress_level'],
            mode='lines+markers',
            name='Stress Level',
            line=dict(color=custom_colors[5], width=3),
            marker=dict(size=8)
        ))
        fig_stress.update_layout(
            title='Stress Level Trend',
            template='plotly_dark',
            height=300
        )
        st.plotly_chart(fig_stress, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
