import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse


class FinancialCalculatorsTests(TestCase):

    def setUp(self):
        # Creating a test user for login
        self.user = User.objects.create_user(username='testuser', password='password123')

    # Test login page
    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')  # Assuming 'Login' is on the page

    # Test correct login with valid credentials
    def test_login_correct(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(response, reverse('home'))

    # Test incorrect login with invalid credentials
    def test_login_incorrect(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, 'Invalid username or password.')

    # Test EMI Calculator
    '''def test_emi_calculator_post(self):
    # Log in the user first if authentication is required
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('home'), {
            'principal': 100000,
            'rate': 7.5,
            'tenure': 20
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EMI')  # or another expected result'''



    # Test SIP Calculator
    def test_sip_calculator_post(self):
        response = self.client.post(reverse('sip_calculator'), {
            'monthly_investment': 10000,
            'rate': 12,
            'years': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maturity')  # Make sure maturity value is in the response

    # Test Loan Prediction View
    def test_loan_predictor_post(self):
        # Mocking data for loan prediction (make sure features match the ones expected by your model)
        response = self.client.post(reverse('loan_pre'), {
            'Age': 30,
            'Monthly_Income': 50000,
            'Credit_Score': 750,
            'Loan_Tenure_Years': 10,
            'Existing_Loan_Amount': 100000,
            'Num_of_Dependents': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prediction')  # Check if the prediction result is returned

    # Test EDA View (testing for presence of plots)
    '''def test_eda_view(self):
        response = self.client.get(reverse('loan_eda'))
        self.assertContains(response, 'Loan Amount Distribution')  # or check for <img> tags for the plot
 # Checking if plot name is includeding if another plot is included'''


class LoanEligibilityCalculatorTests(TestCase):

    def test_loan_eligibility_post(self):
        response = self.client.post(reverse('loan_eligibility_estimator'), {
            'monthly_income': 60000,
            'monthly_expenses': 20000,
            'tenure': 15,
            'interest_rate': 8
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Loan Eligibility')  # Check if loan eligibility result is displayed


'''class RetirementSavingsTests(TestCase):

    def test_retirement_savings_post(self):
        response = self.client.post(reverse('retirement_savings_estimator'), {
            'investment': 50000,
            'years': 20,
            'rate_of_return': 6,
            'current_savings': 10000  # Make sure this field is included
        })
        self.assertContains(response, 'Future Value')  # Check if 'Future Value' is included'''



class BudgetPlannerTests(TestCase):

    def test_budget_planner_post(self):
        response = self.client.post(reverse('simple_budget_planner'), {
            'income': 50000,
            'fixed_expenses': 10000,
            'variable_expenses': 15000
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Savings')  # Checking if savings is shown in the response


if __name__ == '__main__':
    unittest.main()
