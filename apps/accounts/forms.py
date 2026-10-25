from django import forms
from .models import User, TravelerProfile, ProviderProfile

class TravelerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-teal-200 outline-none'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-teal-200 outline-none'}))
    travel_style = forms.ChoiceField(choices=TravelerProfile.TRAVEL_STYLE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-teal-200 outline-none'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-teal-200 outline-none'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-teal-200 outline-none'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-teal-200 outline-none'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-teal-200 outline-none'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class ProviderRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-teal-200 outline-none'}))
    business_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}))
    business_type = forms.ChoiceField(choices=ProviderProfile.BUSINESS_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}))
    license_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}))
    office_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 2}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }
