import datetime
from django import forms

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks.",
        widget=forms.SelectDateWidget()
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Check if the date is in the past
        if data < datetime.date.today():
            raise forms.ValidationError("Invalid date - renewal in past")

        # Check if the date is too far in the future
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise forms.ValidationError("Invalid date - renewal more than 4 weeks ahead")

        return data
