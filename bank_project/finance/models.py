# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Account"

class Transaction(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'

    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} on {self.timestamp}"

    def save(self, *args, **kwargs):
        if self.transaction_type == self.DEPOSIT:
            self.account.balance += self.amount
        elif self.transaction_type == self.WITHDRAWAL:
            self.account.balance -= self.amount
        self.account.save()
        super().save(*args, **kwargs)
