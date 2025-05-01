import os
import joblib
from django.shortcuts import render
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.conf import settings
# Create your views here.

model = joblib.load(os.path.join(settings.BASE_DIR, r'C:\Users\Administrator\Desktop\Final Project\Python-FinalProject-\bank_project\loan_model.pkl'))
features = joblib.load(os.path.join(settings.BASE_DIR, r'C:\Users\Administrator\Desktop\Final Project\Python-FinalProject-\bank_project\model_features.pkl'))
labels = {
    'Age': 'Age (years)',
    'Monthly_Income': 'Monthly Income (₹)',
    'Credit_Score': 'Credit Score (300–850)',
    'Loan_Tenure_Years': 'Loan Tenure (years)',
    'Existing_Loan_Amount': 'Existing Loan Amount (₹)',
    'Num_of_Dependents': 'Number of Dependents'
}

def loan_predictor(request):
    prediction = None
    if request.method == 'POST':
        try:
            input_data = [float(request.POST[f]) for f in features]
            prediction = round(model.predict([input_data])[0], 2)
        except Exception as e:
            prediction = f"Error: {e}"
    
    return render(request, 'predictor/predict.html', {'features': features, 'prediction': prediction,'labels': labels})
    
def eda_view(request):
    df = pd.read_csv(r'C:\Users\Administrator\Desktop\New folder (2)\loan_project\loan_amount_prediction_dataset_v2.csv').dropna()
    plots = []

    # Plot 1: Loan Amount Distribution
    fig, ax = plt.subplots()
    sns.histplot(df['Loan_Amount'], kde=True, ax=ax)
    ax.set_title('Loan Amount Distribution')
    plots.append(get_base64_plot(fig))

    # Plot 2: Loan Amount vs Income
    fig, ax = plt.subplots()
    sns.scatterplot(x='Monthly_Income', y='Loan_Amount', data=df, ax=ax)
    ax.set_title('Loan Amount vs Monthly Income')
    plots.append(get_base64_plot(fig))

    # Plot 3: Credit Score vs Loan Amount
    fig, ax = plt.subplots()
    sns.boxplot(x='Credit_Score', y='Loan_Amount', data=df, ax=ax)
    ax.set_title('Credit Score vs Loan Amount')
    plots.append(get_base64_plot(fig))

    return render(request, 'predictor/eda.html', {'plots': plots})

def get_base64_plot(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')