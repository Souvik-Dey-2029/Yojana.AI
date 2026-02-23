import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_model():
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), "schemes_dataset.csv")
    df = pd.read_csv(data_path)

    # Features and Targets
    X = df.drop(columns=[
        'pm_kisan', 'swami_vivekananda_scholarship', 'mudra_loan', 
        'kanyashree', 'ews_scholarship', 'skill_india', 
        'startup_india_seed', 'pm_awas_yojana'
    ])
    y = df[[
        'pm_kisan', 'swami_vivekananda_scholarship', 'mudra_loan', 
        'kanyashree', 'ews_scholarship', 'skill_india', 
        'startup_india_seed', 'pm_awas_yojana'
    ]]

    # Encode categorical features
    encoders = {}
    X_encoded = X.copy()
    for column in ['gender', 'state', 'occupation', 'education', 'category']:
        le = LabelEncoder()
        X_encoded[column] = le.fit_transform(X[column])
        encoders[column] = le

    # Initialize and train the model
    # We use MultiOutputClassifier because one user can be eligible for multiple schemes
    base_clf = DecisionTreeClassifier(random_state=42)
    model = MultiOutputClassifier(base_clf)
    model.fit(X_encoded, y)

    # Save the model and encoders
    save_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    joblib.dump({'model': model, 'encoders': encoders, 'feature_names': X.columns.tolist()}, save_path)
    print(f"Model trained and saved to {save_path}")

if __name__ == "__main__":
    train_model()
