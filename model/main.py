# Import essential libraries for data handling, modeling, and evaluation
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report  # <- added missing import
import pickle as pickle

# Function to create, train, and evaluate a logistic regression model
def create_model(data):
    # Separate features (X) and target (y)
    X = data.drop(['diagnosis'], axis=1)
    y = data['diagnosis']

    # Standardize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train the logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions and evaluate performance
    y_pred = model.predict(X_test)
    print('Accuracy of our model:', accuracy_score(y_test, y_pred))
    print("Classification report:\n", classification_report(y_test, y_pred))

    return model, scaler

# Function to load and clean the dataset
def get_clean_data():
    # Load the CSV file into a DataFrame
    data = pd.read_csv('data\data.csv')

    # Remove unnecessary columns
    data = data.drop(['Unnamed: 32', 'id'], axis=1)

    # Encode the diagnosis column: M = 1 (malignant), B = 0 (benign)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

    return data

# Main execution function
def main():
    # Load and clean the data
    data = get_clean_data()

    # Train model and scale features
    model, scaler = create_model(data)

    # Save the trained model to a file
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Save the fitted scaler to a file
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

# Entry point of the script
if __name__ == '__main__':
    main()
