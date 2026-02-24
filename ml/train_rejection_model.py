import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model():
    print("🚀 Starting Rejection Model Training...")
    
    # Load dataset
    data_path = 'ml/rejection_dataset.csv'
    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found.")
        return
        
    df = pd.read_csv(data_path)
    
    # Features and Target
    X = df.drop('approved', axis=1)
    y = df['approved']
    
    # Train Model (Random Forest for robust probability scores)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save Model
    model_path = 'ml/rejection_model.joblib'
    joblib.dump(model, model_path)
    
    print(f"✅ Model trained and saved to {model_path}")
    print(f"Features mapped: {list(X.columns)}")

if __name__ == "__main__":
    train_model()
