# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TransactionForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        min_value=0.01, 
        widget=forms.NumberInput(attrs={'placeholder': 'Amount'})
    )

class LoanPredictionForm(forms.Form):
    age = forms.IntegerField(label="Age")
    income = forms.FloatField(label="Monthly Income (₹)")
    credit_score = forms.IntegerField(label="Credit Score (300–850)")
    tenure = forms.IntegerField(label="Loan Tenure (Years)")
    existing_loan = forms.FloatField(label="Existing Loan Amount")
    dependents = forms.IntegerField(label="Number of Dependents")
