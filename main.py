from tensorflow.keras.models import load_model
import feature_extraction as fe
import numpy as np

try:
    extracted_parameters = fe.extract_url("https://www.apple.com")
except:
    print("Error in Extraction of features due to above exception ^^")
    exit()

loaded_model = load_model('./phising-urls/phishing_model.h5')

input_data = np.expand_dims(extracted_parameters, axis=0)

prediction = loaded_model.predict(input_data)
prediction = (prediction >= 0.5).astype(int)
print(prediction)
if prediction[0][0] == 0:
    print("Legitimate URL")
else:
    print("Phishing URL")


