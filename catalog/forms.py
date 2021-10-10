from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as txtlazy
import datetime

from django import forms
from django.forms import ModelForm
from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):

      def clean_due_back(self):
            data = self.cleaned_data['due_back']

            #checking if date is not in the past
            if data < datetime.date.today():
                  raise ValidationError(txtlazy('Invalid date - renewal in past'))

            #check if date is in allowed parameters (+4 weeks from today).
            if data > datetime.date.today() + datetime.timedelta(weeks = 4):
                  raise ValidationError(txtlazy('Invalid date - renewal more than 4 weeks ahead'))

            return data

      class Meta:
            model = BookInstance
            fields = ['due_back']
            labels = {'due_back': txtlazy('Renewal date')}
            help_text = {'due_back': txtlazy('Enter a date between now and 4 weeks(default 3).')}


# class RenewBookForm(forms.Form):
#       renewal_date = forms.DateField(help_text = "Enter a date between now and 4 weeks (default 3).")

#       def clean_renewal_date(self):
#        	data = self.cleaned_data['renewal_date']

#        	#checking if date is valid and not in the past
#        	if data < datetime.date.today():
#        		raise ValidationError(txtlazy('Invalid date - renewal in past'))

#        	if data > datetime.date.today() + datetime.timedelta(weeks=4):
#        		raise ValidationError(txtlazy('Invalid date - renewal more then 4 weeks ahead'))

#        	return data