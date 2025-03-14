import streamlit as st
from utils.data_manager import DataManager

def show_profile():
    if 'user_email' not in st.session_state:
        st.warning("Please login to access the profile")
        return

    st.title("Profile & Metrics")
    data_manager = DataManager()

    # Create tabs for different sections
    metrics_tab, history_tab, feedback_tab = st.tabs([
        "Update Metrics", "History", "Feedback"
    ])

    with metrics_tab:
        with st.form("metrics_form"):
            st.subheader("Update Your Metrics")

            col1, col2 = st.columns(2)

            with col1:
                age = st.number_input("Age", min_value=1, max_value=120)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0)
                height = st.number_input("Height (cm)", min_value=50.0, max_value=300.0)
                heart_rate = st.number_input("Resting Heart Rate (bpm)", min_value=40, max_value=200)

            with col2:
                activity_level = st.select_slider(
                    "Activity Level",
                    options=["Sedentary", "Light", "Moderate", "Very Active", "Extremely Active"]
                )
                sleep_hours = st.slider("Sleep Hours", 0.0, 24.0, 8.0, 0.5)
                stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
                exercise_minutes = st.number_input("Daily Exercise Minutes", min_value=0, max_value=300)

            submitted = st.form_submit_button("Save Metrics")

            if submitted:
                metrics = {
                    'age': age,
                    'gender': gender,
                    'weight': weight,
                    'height': height,
                    'activity_level': activity_level,
                    'sleep_hours': sleep_hours,
                    'stress_level': stress_level,
                    'heart_rate': heart_rate,
                    'exercise_minutes': exercise_minutes
                }
                data_manager.save_metrics(st.session_state.user_email, metrics)
                st.success("Metrics updated successfully!")

    with history_tab:
        st.subheader("Your Fitness History")
        user_metrics = data_manager.get_user_metrics(st.session_state.user_email)
        if not user_metrics.empty:
            st.line_chart(user_metrics.set_index('date')[['weight', 'sleep_hours', 'stress_level']])
            st.dataframe(user_metrics)
        else:
            st.info("No historical data available yet.")

    with feedback_tab:
        st.subheader("Provide Feedback")
        feedback_text = st.text_area("Share your thoughts or suggestions:")
        if st.button("Submit Feedback"):
            data_manager.save_feedback(st.session_state.user_email, feedback_text)
            st.success("Thank you for your feedback!")

    # Display current metrics and recommendations
    latest_metrics = data_manager.get_latest_metrics(st.session_state.user_email)
    if latest_metrics is not None:
        st.subheader("Current Stats & Recommendations")

        # Create three columns for different metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Age", int(latest_metrics['age']))
            st.metric("Weight", f"{latest_metrics['weight']} kg")
            st.metric("Height", f"{latest_metrics['height']} cm")

        with col2:
            bmi = data_manager.calculate_bmi(latest_metrics['weight'], latest_metrics['height'])
            bmi_category, bmi_suggestion = data_manager.get_bmi_category(bmi)
            st.metric("BMI", f"{bmi:.1f}")
            st.metric("BMI Category", bmi_category)

        with col3:
            st.metric("Activity Level", latest_metrics['activity_level'])
            st.metric("Daily Exercise", f"{latest_metrics['exercise_minutes']} minutes")
            st.metric("Calories Burned", f"{latest_metrics['calories_burned']:.0f} kcal")

        # Exercise recommendations
        st.subheader("Personalized Recommendations")
        exercise_plan = data_manager.get_exercise_suggestions(
            latest_metrics['age'], 
            bmi_category,
            latest_metrics['activity_level']
        )

        st.write("🏃‍♂️ Recommended Exercises:", ", ".join(exercise_plan['exercises']))
        st.write("⏱️ Suggested Duration:", exercise_plan['duration'])
        st.write("📅 Recommended Frequency:", exercise_plan['frequency'])
        st.write("💡 Health Tip:", bmi_suggestion)