from tensorflow.keras.models import load_model
import feature_extraction as fe
import numpy as np


extracted_parameters = fe.extract_parameters('https://www.google.com')

loaded_model = load_model("my_model.h5")

prediction = loaded_model.predict(np.array([list(extracted_parameters.values())]))
prediction = (prediction >= 0.5).astype(int)
print(prediction)
if prediction[0][0] == 0:
    print("Phishing URL")
else:
    print("Legitimate URL")
