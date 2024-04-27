
# Phishing Website Detection Project 


## Introduction
Phishing websites are deceptive websites designed to trick users into revealing sensitive information such as login credentials, financial details, or personal information. These websites often impersonate legitimate entities, like banks, social media platforms, or online stores, to deceive users into disclosing their confidential data.

## Dataset
The models in this repository are trained on a diverse dataset consisting of features extracted from known phishing and legitimate websites. By analyzing various attributes such as URL structure, content, and metadata, these models learn to distinguish between phishing and legitimate websites effectively.

Dataset can be found [here](https://www.kaggle.com/datasets/eswarchandt/phishing-website-detector/)

## Models

Models implemented in the project:

Support Vector Machine (SVM)
Random Forest
Decision Tree
XGBoost
Linear Regression
Neural Networks


## Screenshots
![App Screenshot](https://github.com/AnandRajaM/phishing-urls/blob/main/images/landing.png)
![App Screenshot](https://github.com/AnandRajaM/phishing-urls/blob/main/images/prediction.png)



## Usage

#### 1. Clone the Repository:
``` 
git clone https://github.com/your_username/phishing-website-detection.git
```

#### 2. Install Dependencies:

```
pip install -r requirements.txt
```

#### 3. Run app.py
```
streamlit run app.py
```

#### 4. Done! Now Input a URL , Choose your model , and let the models do its magic! ✨


## URL Trust Index

In addition to the machine learning models, we've introduced a new feature called the URL Trust Index (UTI). The URL Trust Index provides a score between 1 and 10, signifying the trustworthiness of a website. This score is calculated using various parameters, including SSL certificate information, SSL certificate validation date, page rank, HTTPS usage, and more.
## Results
We've thoroughly evaluated the performance of each model using metrics like accuracy, precision, recall, F1-score, Cohen's Kappa, and more. Additionally, visualizations such as confusion matrices, decision boundaries, ROC curves, etc., are provided for each model. You can find these evaluation metrics and visualizations in the respective Jupyter Notebooks (*.ipynb) for each model.
## Sample Dataset
| Index | UsingIP | LongURL | ShortURL | Symbol@ | Redirecting// | PrefixSuffix- | SubDomains | HTTPS | DomainRegLen | Favicon | NonStdPort | HTTPSDomainURL | RequestURL | AnchorURL | LinksInScriptTags | ServerFormHandler | InfoEmail | AbnormalURL | WebsiteForwarding | StatusBarCust | DisableRightClick | UsingPopupWindow | IframeRedirection | AgeofDomain | DNSRecording | WebsiteTraffic | PageRank | GoogleIndex | LinksPointingToPage | StatsReport | class |
|-------|---------|---------|----------|---------|---------------|----------------|------------|-------|--------------|---------|------------|-----------------|------------|-----------|-------------------|-------------------|------------|--------------|-------------------|----------------|-------------------|------------------|-------------------|-------------|--------------|-----------------|----------|-------------|---------------------|-------------|-------|
| 0     | 1       | 1       | 1        | 1       | 1             | -1             | 0          | 1     | -1           | 1       | 1          | -1              | 1          | 0         | -1                | -1                | 1          | 1            | 0                 | 1              | 1                 | 1                | 1                 | -1          | -1           | 0               | -1       | 1           | 1                   | 1           | -1    |
