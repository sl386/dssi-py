import streamlit as st
from src.inference import get_prediction

# Initialise session state variable
if 'input_features' not in st.session_state:
    st.session_state['input_features'] = {}

def app_sidebar():
    st.sidebar.header('Diabetes Prediction')

    # Input fields for diabetes-related variables
    pregnancies = st.sidebar.slider('Number of Pregnancies', 0, 20, 0, 1)
    glucose = st.sidebar.slider('Glucose Level', 0, 200, 100, 1)
    blood_pressure = st.sidebar.slider('Blood Pressure', 0, 200, 80, 1)
    skin_thickness = st.sidebar.slider('Skin Thickness (mm)', 0, 100, 20, 1)
    insulin = st.sidebar.slider('Insulin Level', 0, 900, 100, 1)
    bmi = st.sidebar.slider('BMI (kg/m^2)', 10.0, 70.0, 25.0, 0.1)
    diabetes_pedigree = st.sidebar.slider('Diabetes Pedigree Function', 0.0, 2.5, 0.5, 0.01)
    age = st.sidebar.slider('Age', 18, 100, 30, 1)

    def get_input_features():
        input_features = {
            'Pregnancies': pregnancies,
            'Glucose': glucose,
            'BloodPressure': blood_pressure,
            'SkinThickness': skin_thickness,
            'Insulin': insulin,
            'BMI': bmi,
            'DiabetesPedigreeFunction': diabetes_pedigree, 
            'Age': age
        }
        return input_features

    # Buttons for prediction and reset
    sdb_col1, sdb_col2 = st.sidebar.columns(2)
    with sdb_col1:
        predict_button = st.sidebar.button("Predict Diabetes Outcome", key="predict")
    with sdb_col2:
        reset_button = st.sidebar.button("Reset", key="clear")

    if predict_button:
        st.session_state['input_features'] = get_input_features()

    if reset_button:
        st.session_state['input_features'] = {}

    return None

def app_body():
    title = title = title = '<p style="font-family:arial, sans-serif; color:#31333F; font-size: 40px; text-align:center;"><b>Diabetes Prediction with Random Forest</b></p>'
    st.markdown(title, unsafe_allow_html=True)
    default_msg = '**System assessment says:** {}'
    if st.session_state['input_features']:
        assessment = get_prediction(pregnancies=st.session_state['input_features']['Pregnancies'],
                                    glucose=st.session_state['input_features']['Glucose'],
                                    blood_pressure=st.session_state['input_features']['BloodPressure'],
                                    skin_thickness=st.session_state['input_features']['SkinThickness'],
                                    insulin=st.session_state['input_features']['Insulin'],
                                    bmi=st.session_state['input_features']['BMI'],
                                    diabetes_pedigree=st.session_state['input_features']['DiabetesPedigreeFunction'],
                                    age=st.session_state['input_features']['Age'])
        # Display result based on assessment value
        if assessment.lower() == "positive":
            result_text = '<p style="font-family:arial, sans-serif; color:#FF4B4B; font-size: 20pt; text-align:center;"><b>!!! High likelihood of diabetes !!!</b></p>'
            st.markdown(result_text, unsafe_allow_html=True)
        if assessment.lower() == "negative":
            result_text = '<p style="font-family:arial, sans-serif; color:#31333F; font-size: 20pt; text-align:center;"><b>Low likelihood of diabetes</b></p>'
            st.markdown(result_text, unsafe_allow_html=True)
    return None

def main():
    app_sidebar()
    app_body()
    return None

if __name__ == "__main__":
    main()