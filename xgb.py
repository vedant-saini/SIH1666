import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
df = pd.read_csv('student_career_guidance_randomized.csv')

# Check for missing values
missing_values = df.isnull().sum()
print(f"Missing values in each column:\n{missing_values}")

# One-hot encode the 'Interest' and 'Strength' columns
encoder = OneHotEncoder(sparse_output=False)
encoded_data = encoder.fit_transform(df[['Interest', 'Strength']])
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(['Interest', 'Strength']))

# Label encode the 'Career Path' column
label_encoder = LabelEncoder()
df['Career Path'] = label_encoder.fit_transform(df['Career Path'])

# Combine the encoded features with the Academic Performance and Career Path
final_df = pd.concat([encoded_df, df[['Academic Performance', 'Career Path']]], axis=1)

# Standardize the 'Academic Performance' column
scaler = StandardScaler()
final_df['Academic Performance'] = scaler.fit_transform(final_df[['Academic Performance']])

# Separate features (X) and target (y)
X = final_df.drop(columns=['Career Path'])
y = final_df['Career Path']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

# Define the XGBoost model
xgb = XGBClassifier(random_state=42)

# Define the hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

# Set up the grid search
grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Get the best parameters and the corresponding score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print(f"Best Parameters: {best_params}")
print(f"Best Cross-Validation Score: {best_score}")

# Train the XGBoost model with the best parameters
best_xgb = XGBClassifier(**best_params, random_state=42)
best_xgb.fit(X_train, y_train)

# Predict on the test set
y_pred = best_xgb.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy with Best Hyperparameters: {accuracy}')

# Define the career_map for labels
career_map = {0: 'Software Engineer', 1: 'Graphic Designer', 2: 'Business Analyst', 3: 'Data Scientist', 4: 'Teacher'}

# Generate a classification report
print('Classification Report with Best Hyperparameters:')
print(classification_report(y_test, y_pred, target_names=career_map.values()))
