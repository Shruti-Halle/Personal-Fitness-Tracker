import pandas as pd
import os
from datetime import datetime

class DataManager:
    def __init__(self):
        self.fitness_file = "data/fitness_data.csv"
        self._init_fitness_file()

    def _init_fitness_file(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.fitness_file):
            columns = ['email', 'date', 'age', 'gender', 'weight', 'height', 
                      'activity_level', 'sleep_hours', 'stress_level', 
                      'heart_rate', 'calories_burned', 'exercise_minutes']
            pd.DataFrame(columns=columns).to_csv(self.fitness_file, index=False)

    def calculate_bmi(self, weight, height):
        # Ensure numeric types
        try:
            weight = float(weight)
            height = float(height)
            height_m = height / 100  # Convert cm to m
            bmi = weight / (height_m * height_m)
            return round(bmi, 2)
        except (ValueError, TypeError):
            return 0.0

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight", "Consider increasing caloric intake and strength training."
        elif bmi < 24.9:
            return "Normal weight", "Maintain your current healthy lifestyle."
        elif bmi < 29.9:
            return "Overweight", "Focus on cardio exercises and balanced diet."
        else:
            return "Obese", "Consult a healthcare provider and start with low-impact exercises."

    def get_exercise_suggestions(self, age, bmi_category, activity_level):
        suggestions = {
            "Underweight": {
                "exercises": ["Bodyweight squats", "Push-ups", "Resistance band training"],
                "duration": "30-45 minutes",
                "frequency": "3-4 times per week"
            },
            "Normal weight": {
                "exercises": ["Running", "Cycling", "Full body workouts"],
                "duration": "45-60 minutes",
                "frequency": "4-5 times per week"
            },
            "Overweight": {
                "exercises": ["Brisk walking", "Swimming", "Stationary cycling"],
                "duration": "30-45 minutes",
                "frequency": "5-6 times per week"
            },
            "Obese": {
                "exercises": ["Walking", "Water aerobics", "Light yoga"],
                "duration": "20-30 minutes",
                "frequency": "Start with 3 times per week"
            }
        }
        return suggestions.get(bmi_category, suggestions["Normal weight"])

    def calculate_calories_burned(self, weight, exercise_minutes, activity_level):
        try:
            weight = float(weight)
            exercise_minutes = float(exercise_minutes)
            # Rough estimation of calories burned based on activity level
            calories_per_minute = {
                "Sedentary": 3,
                "Light": 4,
                "Moderate": 6,
                "Very Active": 8,
                "Extremely Active": 10
            }
            rate = calories_per_minute.get(activity_level, 5)
            return round(rate * exercise_minutes * (weight / 60), 2)
        except (ValueError, TypeError):
            return 0.0

    def save_metrics(self, email, metrics):
        fitness_df = pd.read_csv(self.fitness_file)
        metrics['email'] = email
        metrics['date'] = datetime.now().strftime('%Y-%m-%d')

        # Ensure numeric types
        for field in ['age', 'weight', 'height', 'sleep_hours', 'stress_level', 'heart_rate', 'exercise_minutes']:
            if field in metrics:
                metrics[field] = float(metrics[field])

        # Calculate calories burned
        metrics['calories_burned'] = self.calculate_calories_burned(
            metrics['weight'], 
            metrics.get('exercise_minutes', 30),
            metrics['activity_level']
        )

        new_entry = pd.DataFrame([metrics])
        fitness_df = pd.concat([fitness_df, new_entry], ignore_index=True)
        fitness_df.to_csv(self.fitness_file, index=False)

    def get_user_metrics(self, email):
        fitness_df = pd.read_csv(self.fitness_file)
        user_metrics = fitness_df[fitness_df['email'] == email].sort_values('date')

        # Convert numeric columns
        numeric_columns = ['age', 'weight', 'height', 'sleep_hours', 'stress_level', 
                         'heart_rate', 'exercise_minutes', 'calories_burned']
        for col in numeric_columns:
            if col in user_metrics.columns:
                user_metrics[col] = pd.to_numeric(user_metrics[col], errors='coerce')

        return user_metrics

    def get_latest_metrics(self, email):
        user_metrics = self.get_user_metrics(email)
        if user_metrics.empty:
            return None
        return user_metrics.iloc[-1]

    def save_feedback(self, email, feedback_text):
        feedback_file = "data/feedback.csv"
        if not os.path.exists(feedback_file):
            pd.DataFrame(columns=['email', 'date', 'feedback']).to_csv(feedback_file, index=False)

        feedback_df = pd.read_csv(feedback_file)
        new_feedback = pd.DataFrame([[email, datetime.now().strftime('%Y-%m-%d'), feedback_text]], 
                                  columns=['email', 'date', 'feedback'])
        feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
        feedback_df.to_csv(feedback_file, index=False)