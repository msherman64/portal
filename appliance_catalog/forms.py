from django.forms import ModelForm, CharField, TextInput
from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError
from .models import Appliance
import logging

logger = logging.getLogger('default')
class ApplianceForm(ModelForm):
	new_keywords = CharField(label="Assign new keywords", widget=TextInput(attrs={'placeholder': 'Provide comma separated keywords that are not in the list above.'}), required=False)
	author_url = CharField(label="Author: Contact URL or Email")
	support_contact_name = CharField(label="Support: Contact name")
	support_contact_url = CharField(label="Support: Contact URL or Email")
	class Meta:
		model = Appliance
		fields = ['name', 'description', 'appliance_icon', 'chi_tacc_appliance_id', 'chi_uc_appliance_id', 'kvm_tacc_appliance_id', 'author_name',
		          'author_url', 'support_contact_name', 'support_contact_url', 'project_supported', 'keywords', 'new_keywords', 'version']

	def __init__(self, user, *args, **kwargs):
		super(ApplianceForm, self).__init__(*args, **kwargs)
		if not user.is_staff:
			del self.fields['project_supported']

	def _is_valid_email_or_url(self, text):
		valid_email = True
		valid_url = True
		try:
			validate_email(text)
		except ValidationError:
			valid_email = False
		validate_url = URLValidator()
		try:
			validate_url(text)
		except ValidationError:
			valid_url = False
		if valid_email or valid_url:
			return True
		else:
			return False

	def clean(self):
		cleaned_data = super(ApplianceForm, self).clean()
		author_url = cleaned_data.get('author_url')
		support_contact_url = cleaned_data.get('support_contact_url')
		chi_tacc_appliance_id = cleaned_data.get('chi_tacc_appliance_id')
		chi_uc_appliance_id = cleaned_data.get('chi_uc_appliance_id')
		kvm_tacc_appliance_id = cleaned_data.get('kvm_tacc_appliance_id')


		if not self._is_valid_email_or_url(author_url):
			msg = 'Please enter a valid email or url.'
			self.add_error('author_url', msg)
		if not self._is_valid_email_or_url(support_contact_url):
			msg = 'Please enter a valid email or url.'
			self.add_error('support_contact_url', msg)
		if not (chi_tacc_appliance_id or chi_uc_appliance_id or kvm_tacc_appliance_id):
			msg = 'At least one form of appliance id is required.'
			self.add_error('chi_tacc_appliance_id', '')
			self.add_error('chi_uc_appliance_id', '')
			self.add_error('kvm_tacc_appliance_id', msg)
