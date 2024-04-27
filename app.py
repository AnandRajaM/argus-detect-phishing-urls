import streamlit as st
import time
import tensorflow
from tensorflow.keras.models import load_model
from concurrent.futures import ThreadPoolExecutor 
import feature_extraction as fe
import url_trust_index as uti
import numpy as np
import joblib

loaded_svm_model = joblib.load('./phising-urls/svm_phishing_model.pkl')
loaded_decision_tree_model = joblib.load('./phising-urls/decision_tree_phishing_model.pkl')
loaded_random_forest_model = joblib.load('./phising-urls/random_forest_phishing_model.pkl')
loaded_xgboost_model = joblib.load('./phising-urls/XGBoost_phishing_model.pkl')
loaded_logistic_regression_model = joblib.load('./phising-urls/linear_regression_phishing_model.pkl')

loaded_model = load_model('./phising-urls/phishing_model.h5')

st.title('Phishing URL Checker')

with st.sidebar:
    st.header('Preffered Models:')
    st.write('1. Neural Network')
    st.write('2. XGBoost')

url = st.text_input('Enter URL to check 😀 :')
option = st.selectbox(
    'Choose Your Model',
    ('Neural Network','SVM', 'Decision Tree', 'Random Forest', 'XGBoost', 'Linear Regression'))


if st.button('Check'):
    start_time = time.time()  # Record the start time
    progress_text = st.empty()  # Placeholder for displaying elapsed time
    uti_text = st.empty()

    with st.spinner('Checking the URL...'):
        if not url:
            st.warning('Please enter a URL to check')
            exit()
        if not url.startswith('http') or not url.startswith('https'):
            st.warning('Please enter a valid URL with http or https protocol included! (Complete Address)')
            exit()
            
        try:
            with ThreadPoolExecutor() as executor:
                extracted_parameters = executor.submit(fe.extract_url, url)
                uti = executor.submit(uti.calculate_uti, url)
            extracted_parameters = extracted_parameters.result()
            uti = uti.result()
            print(uti)
        except:
            st.error('Error in Extraction of features due to Exception')
            exit()

        input_data = np.expand_dims(extracted_parameters, axis=0)
        if option == 'SVM':
            prediction = loaded_svm_model.predict([extracted_parameters])
        if option == 'Decision Tree':  
            prediction = loaded_decision_tree_model.predict([extracted_parameters])
        if option == 'Random Forest':
            prediction = loaded_random_forest_model.predict([extracted_parameters])
        if option == 'XGBoost':
            prediction = loaded_xgboost_model.predict([extracted_parameters])
        if option == 'Linear Regression':
            prediction = loaded_logistic_regression_model.predict([extracted_parameters])
        
        if option == 'Neural Network':
            prediction_neural = loaded_model.predict(input_data)
            prediction_neural = (prediction_neural >= 0.5).astype(int)
            print(prediction_neural)
            if prediction_neural[0][0] == 0:
                st.success('The URL is Legitimate')
                st.balloons()
            else:
                st.error('The URL is Phishing')
        try:
            if prediction[0] == 0:
                st.success('The URL is Legitimate')
                st.balloons()
            else:
                st.error('The URL is Phishing')
        except:
            pass
        
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time
        progress_text.write(f":rainbow[Time taken to check the URL: {elapsed_time:.2f} seconds]")
        if uti >= 7:
            uti_text.write('URL Trust Index: :green[{}]'.format(uti))
        elif uti >= 5.5 and uti < 7:
            uti_text.write('URL Trust Index: :yellow[{}]'.format(uti))
        else:
            uti_text.write('URL Trust Index: :red[{}]'.format(uti))


st.header('What is Phishing URL?')
st.write(":red[Phishing] is a type of social engineering attack often used to steal user data, including login credentials and credit card numbers. It occurs when an attacker, masquerading as a trusted entity, dupes a victim into opening an email, instant message, or text message. The recipient is then tricked into clicking a malicious link, which can lead to the installation of malware, the freezing of the system as part of a ransomware attack or the revealing of sensitive information. The attacker may also use social engineering to manipulate the victim into providing personal information, such as passwords and credit card numbers.")


def stream_data():
    st.write("Phishing websites are deceptive platforms designed to trick users into divulging sensitive information. They often mimic legitimate websites or use targeted messaging to lure victims. Here are key aspects to consider:")
    st.write("- **Spoofed Websites:** Phishing sites mimic real ones, often with slight URL variations.")
    st.write("- **Deceptive Messages:** They start with emails or messages pretending to be from trusted sources.")
    st.write("- **Targeted Attacks:** Some are personalized (spear phishing) for higher success.")
    st.write("- **Credential Theft:** They aim to steal login details for unauthorized access or fraud.")
    st.write("- **Data Collection:** Phishing sites also gather sensitive info like credit card numbers.")
    st.write("- **Malware Distribution:** Clicking links or attachments can install malware.")
    st.write("- **Redirects and Pop-ups:** Tactics to trap users and prevent easy escape.")
    st.write("- **Social Engineering:** Manipulating emotions or urgency to trick users.")
    st.write("- **Evolution:** Phishing techniques adapt to tech and user awareness.")
    st.write("- **Preventative Measures:** Caution, security software, and training help thwart attacks.")
    st.write('[Learn more on Wikipedia](https://en.wikipedia.org/wiki/Phishing)')


# Button to trigger displaying more information
if st.button("Learn More"):
    stream_data()