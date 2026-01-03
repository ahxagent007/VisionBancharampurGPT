from django import forms
from .models import ContributionCycle, Payment

class CycleForm(forms.ModelForm):
    class Meta:
        model = ContributionCycle
        fields = ["year", "month", "due_date"]

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "method", "reference"]
