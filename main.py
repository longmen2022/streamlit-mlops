# -----------------------------
# Imports
# -----------------------------

import streamlit as st                      # Streamlit for building the web interface
import pickle                               # Used to load saved machine learning models
import pandas as pd                         # For data manipulation and analysis
import plotly.graph_objects as go           # For rendering interactive radar charts
import numpy as np                          # For numerical operations like reshaping arrays

# -----------------------------
# Load and Clean Dataset
# -----------------------------

def get_clean_data():
    """
    Load and clean the breast cancer dataset from a CSV file.
    Returns a cleaned pandas DataFrame.
    """
    data = pd.read_csv(r'C:\Users\men_l\Downloads\StreamLit-Python-Predict-Cancer\data\data.csv')  # Load dataset
    data = data.drop(['Unnamed: 32', 'id'], axis=1)  # Drop irrelevant columns
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})  # Map diagnosis labels to numeric
    return data  # Return cleaned data

# -----------------------------
# Sidebar Input Sliders
# -----------------------------

def add_sidebar():
    """
    Build the sidebar with sliders for feature input.
    Returns a dictionary with feature names and user-provided values.
    """
    st.sidebar.header("Cell Nuclei Measures")  # Sidebar section title
    data = get_clean_data()  # Load cleaned dataset

    # Label and dataset column mapping
    slider_labels = [
        ("Radius (mean)", "radius_mean"), ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"), ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"), ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"), ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"), ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"), ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"), ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"), ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"), ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"), ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"), ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"), ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"), ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"), ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"), ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}  # Dictionary to store slider values

    for label, key in slider_labels:
        # Create a slider with min=0.0, max as column max, and default as column mean
        input_dict[key] = st.sidebar.slider(
            label=label,
            min_value=0.0,
            max_value=float(data[key].max()),
            value=float(data[key].mean())
        )

    return input_dict  # Return dictionary of input values

# -----------------------------
# Scale Input Values (0 to 1)
# -----------------------------

def get_scaled_values(input_dict):
    """
    Normalize inputs using min-max scaling based on dataset stats.
    """
    data = get_clean_data()  # Get full dataset
    X = data.drop(['diagnosis'], axis=1)  # Drop target column
    scaled_dict = {}  # Dictionary to store scaled inputs

    for key, value in input_dict.items():
        min_val = X[key].min()  # Get min value for feature
        max_val = X[key].max()  # Get max value for feature
        scaled_value = (value - min_val) / (max_val - min_val)  # Min-max scaling
        scaled_dict[key] = scaled_value  # Store scaled value

    return scaled_dict  # Return scaled input dictionary

# -----------------------------
# Create Radar Chart
# -----------------------------

def get_radar_chart(input_data):
    """
    Generate radar chart showing mean, standard error, and worst values.
    """
    input_data = get_scaled_values(input_data)  # Scale inputs for chart plotting

    categories = ['Radius', 'Texture', 'Perimeter', 'Area',
                  'Smoothness', 'Compactness', 'Concavity',
                  'Concave Points', 'Symmetry', 'Fractal Dimension']  # Radar axes

    fig = go.Figure()  # Initialize radar chart

    # Plot mean values
    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
            input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
            input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
            input_data['fractal_dimension_mean']
        ],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))

    # Plot standard error values
    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'],
            input_data['area_se'], input_data['smoothness_se'], input_data['compactness_se'],
            input_data['concavity_se'], input_data['concave points_se'], input_data['symmetry_se'],
            input_data['fractal_dimension_se']
        ],
        theta=categories,
        fill='toself',
        name='Standard Error'
    ))

    # Plot worst values
    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
            input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
            input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
            input_data['fractal_dimension_worst']
        ],
        theta=categories,
        fill='toself',
        name='Worst Value'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),  # Set axis range for normalization
        showlegend=True  # Show legend
    )

    return fig  # Return radar chart object

# -----------------------------
# Prediction Section
# -----------------------------

def add_predictions(input_data):
    """
    Load model and scaler, transform input, and display prediction.
    """
    model = pickle.load(open(r"C:\Users\men_l\Downloads\StreamLit-Python-Predict-Cancer\model\model.pkl", "rb"))  # Load classifier
    scaler = pickle.load(open(r"C:\Users\men_l\Downloads\StreamLit-Python-Predict-Cancer\model\scaler.pkl", "rb"))  # Load scaler

    input_array = np.array(list(input_data.values())).reshape(1, -1)  # Convert dictionary to 2D array
    input_array_scaled = scaler.transform(input_array)  # Scale the input for prediction

    prediction = model.predict(input_array_scaled)  # Get binary prediction
    st.subheader("Cell cluster prediction")
    st.write("The cell cluster is: ")

    if prediction[0] == 0:
        st.write("<span class='diagnosis benign'>Benign</span>", unsafe_allow_html=True)  # Display benign prediction
    else:
        st.write("<span class='diagnosis malignant'>Malignant</span>", unsafe_allow_html=True)  # Display malignant prediction

    # Show probability for each class
    st.write("Probability of being benign: ", model.predict_proba(input_array_scaled)[0][0])
    st.write("Probability of being malignant: ", model.predict_proba(input_array_scaled)[0][1])
    st.write("This app can assist medical professionals in making a diagnosis, but should not be used as a substitute for a professional diagnosis.")
    

# -----------------------------
# Streamlit App Layout
# -----------------------------

def main():
    """
    Build main page layout and call chart and prediction logic.
    """
    st.set_page_config(
        page_title="Breast Cancer Predictor",       # Browser tab title
        page_icon=":female-doctor:",                # Icon shown on tab
        layout="wide",                              # Use wide layout
        initial_sidebar_state="expanded"            # Sidebar expanded by default
    )

    with open(r"C:\Users\men_l\Downloads\StreamLit-Python-Predict-Cancer\assets\style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    input_data = add_sidebar()  # Get sidebar inputs

    with st.container():  # Main app container
        st.title("Breast Cancer Predictor")  # Display page title
        st.write("Please connect this app to your cytology lab to help diagnose breast cancer form your tissue sample. This app predicts using a machine learning model whether a breast mass is benign or malignant based on the measurements it receives from your cytosis lab. You can also update the measurements by hand using the sliders in the sidebar. "
                 "It's meant to support—but not replace—medical evaluation.")

    col1, col2 = st.columns([4, 1])  # Create two columns with different widths

    with col1:
        radar_chart = get_radar_chart(input_data)  # Generate radar chart
        st.plotly_chart(radar_chart)  # Display chart in left column

    with col2:
        add_predictions(input_data)  # Display prediction results in right column

# -----------------------------
# Entry Point
# -----------------------------


if __name__ == '__main__':
    main()  # Launch the Streamlit app
