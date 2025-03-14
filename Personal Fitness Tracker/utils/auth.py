import streamlit as st
import pandas as pd
import hashlib
import os
from pathlib import Path

class AuthManager:
    def __init__(self):
        self.users_file = "data/users.csv"
        self._init_users_file()

    def _init_users_file(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.users_file):
            pd.DataFrame(columns=['email', 'password', 'name']).to_csv(self.users_file, index=False)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, email, password, name):
        users_df = pd.read_csv(self.users_file)
        if email in users_df['email'].values:
            return False, "Email already registered"
        
        hashed_password = self._hash_password(password)
        new_user = pd.DataFrame([[email, hashed_password, name]], 
                               columns=['email', 'password', 'name'])
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(self.users_file, index=False)
        return True, "Registration successful"

    def login_user(self, email, password):
        users_df = pd.read_csv(self.users_file)
        user = users_df[users_df['email'] == email]
        if user.empty:
            return False, "Email not found"
        
        hashed_password = self._hash_password(password)
        if user['password'].iloc[0] == hashed_password:
            return True, user['name'].iloc[0]
        return False, "Incorrect password"