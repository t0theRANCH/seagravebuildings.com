import re
from fractions import Fraction

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .calculate_angles import check_input
from .models import (
    Quote,
    NewUser,
    YES_NO,
    ZONES,
    PURPOSE,
    PROPERTY,
    TIMELINE,
    STYLE,
    INSULATION_ROOF,
    INSULATION_WALL,
    COLOUR,
    GUTTERS, Rectangle
)


def validate_selection(value, field):
    return value in [x[0] for x in SELECTIONS[field]]


def validate_email(value):
    regex = '^[A-Za-z0-9_!#$%&\'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+\.\w{2,3}$'
    return value if re.search(regex, value) else False


def validate_name(value):
    special = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
               '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    rules = [lambda s: any(x in s for x in special),
             lambda s: any(x.isdigit() for x in s)]
    return False if any(rule(value) for rule in rules) else value


def validate_password(value):
    special = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
               '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

    p_rules = [lambda s: any(x.isupper() for x in s),  # must have at least one uppercase
               lambda s: any(x.islower() for x in s),  # must have at least one lowercase
               lambda s: any(x in s for x in special),  # must contain special characters
               ]

    return value if all(rule(value) for rule in p_rules) else False


POSTAL_CODES = (
    ('Canada', "\w\d\w\s?-?\d\w\d"),
    ('US', "\d{5}(-?\d{4})?")
)

SELECTIONS = {
    'zoning': ZONES,
    "purpose": PURPOSE,
    "property": PROPERTY,
    'timeline': TIMELINE,
    'style': STYLE,
    'colour': COLOUR,
    'install': YES_NO,
    'insul_roof': INSULATION_ROOF,
    'insul_walls': INSULATION_WALL,
    'gutters': GUTTERS
}


class Login(forms.Form):
    username = forms.CharField(max_length=50, label='Username', required=True,
                               widget=forms.TextInput(attrs={'class': 'form__field text-input',
                                                             'placeholder': 'Username'}))
    password = forms.CharField(max_length=50, label='Password', required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form__field text-input',
                                                                 'placeholder': 'Password'}))


class ForgotPassword(forms.Form):
    email = forms.CharField(max_length=50, label='Email', required=True,
                            widget=forms.TextInput(attrs={'class': 'form__field text-input',
                                                          'placeholder': 'Email'}))


class ChangePassword(forms.Form):
    def clean_password1(self):
        value = self.cleaned_data['password1']
        if not validate_password(value):
            raise ValidationError('Password must have at least one uppercase, one digit, and one special character')
        if len(value) < 7:
            raise ValidationError('Password must be at least 7 characters')
        return value

    def clean_password2(self):
        value = self.cleaned_data['password2']
        if 'password1' not in self.cleaned_data:
            return value
        if value != self.cleaned_data['password1']:
            raise ValidationError('Both password fields must match')
        return value

    password1 = forms.CharField(max_length=50, label='New Password',
                                widget=forms.PasswordInput(attrs={'class': 'form__field text-input',
                                                                  'placeholder': 'New Password'}))
    password2 = forms.CharField(max_length=50, label='Confirm New Password',
                                widget=forms.PasswordInput(attrs={'class': 'form__field text-input',
                                                                  'placeholder': 'Confirm New Password'}))


class Register(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_first_name(self):
        value = self.cleaned_data['first_name']
        if not validate_name(value) and value:
            raise ValidationError("This field cannot have special characters")
        return value

    def clean_last_name(self):
        value = self.cleaned_data['last_name']
        if not validate_name(value) and value:
            raise ValidationError("This field cannot have special characters")
        return value

    def clean_email(self):
        value = self.cleaned_data['email']
        if not validate_email(value):
            raise ValidationError('Enter a valid email')
        return value

    def clean_password1(self):
        value = self.cleaned_data['password1']
        if not validate_password(value):
            raise ValidationError('Password must have at least one uppercase, one digit, and one special character')
        if len(value) < 7:
            raise ValidationError('Password must be at least 7 characters')
        return value

    def clean_password2(self):
        value = self.cleaned_data['password2']
        if 'password1' not in self.cleaned_data:
            return value
        if value != self.cleaned_data['password1']:
            raise ValidationError('Both password fields must match')
        return value

    class Meta:
        model = NewUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form__field text-input',
                                                    'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form__field text-input',
                                                    'placeholder': 'Confirm Password'}),
            'first_name': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Last Name'}),
        }


class QuoteForm(forms.ModelForm):
    def clean_full_name(self):
        value = self.cleaned_data['full_name']
        if not validate_name(value):
            raise ValidationError("This field cannot have special characters")
        return value

    def clean_email(self):
        value = self.cleaned_data['email']
        if not validate_email(value):
            raise ValidationError('Enter a valid email')
        return value

    def clean_phone(self):
        value = self.cleaned_data['phone']
        regex = '\+?1?\s?\(?\d{3}\)?\s?-?\d{3}\s?-?\d{4}'
        if not re.search(regex, value) or len(value) > 17:
            raise ValidationError('Enter a valid phone number with area code')
        return value

    def clean_postal_code(self):
        value = self.cleaned_data['postal_code']
        if rules := [True for x in POSTAL_CODES if re.search(x[1], value)]:
            return value
        raise ValidationError('Enter a valid postal/zip code')

    def clean_zoning(self):
        field = 'zoning'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_purpose(self):
        field = 'purpose'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_property(self):
        field = 'property'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_timeline(self):
        field = 'timeline'
        value = self.cleaned_data[field]
        print(self.cleaned_data)
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_style(self):
        field = 'style'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_colour(self):
        field = 'colour'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_install(self):
        field = 'install'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_insul_roof(self):
        field = 'insul_roof'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_insul_walls(self):
        field = 'insul_walls'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    def clean_gutters(self):
        field = 'gutters'
        value = self.cleaned_data[field]
        if not validate_selection(value, field):
            raise ValidationError('Please make a valid selection')
        return value

    class Meta:
        model = Quote
        fields = '__all__'
        labels = {
            'full_name': _('Full Name'),
            'email': _('Email'),
            'phone': _('Phone Number'),
            'country': _('Country'),
            'province': _('Province/State'),
            'city': _('City'),
            'county': _('Township/County'),
            'postal_code': _('Postal/Zip Code'),
            'zoning': _('Zoning'),
            'purpose': _('Building\'s Purpose'),
            'property': _('Purchased Property?'),
            'timeline': _('Timeline until completion'),
            'width': _('Width in feet (endwall)'),
            'length': _('Length in feet (sidewall)'),
            'height': _('Height in feet (eave)'),
            'style': _('Building style'),
            'colour': _('Colours'),
            'install': _('Do you require professional installation?'),
            'insul_roof': _('Roof insulation'),
            'insul_walls': _('Wall insulation'),
            'gutters': _('Gutters and downspouts'),
            'walk_doors': _('Walk Doors (people access)'),
            'overhead_doors': _('Overhead Doors (vehicle access)'),
            'oh_door_height': _('Size of Overhead Door'),
            'oh_door_LE': _('Left Endwall'),
            'oh_door_RE': _('Right Endwall'),
            'oh_door_FS': _('Front Sidewall'),
            'oh_door_BS': _('Back Sidewall'),
            'additional': _('Additional Requirements'),
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Full Name'}),
            'email': forms.TextInput(
                attrs={'class': 'form__field text-input', 'placeholder': 'Email', 'type': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Phone Number'}),
            'country': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Country'}),
            'province': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Province/State'}),
            'city': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'City'}),
            'county': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Township/County'}),
            'postal_code': forms.TextInput(attrs={'class': 'form__field text-input', 'placeholder': 'Postal/Zip Code'}),
            'zoning': forms.Select(attrs={'class': 'select-text select-input'}),
            'purpose': forms.Select(attrs={'class': 'select-text select-input'}),
            'property': forms.Select(attrs={'class': 'select-text select-input'}),
            'timeline': forms.Select(attrs={'class': 'select-text select-input'}),
            'width': forms.NumberInput(
                attrs={'class': 'form__field number-input', 'placeholder': 'Width in feet(endwall)'}),
            'length': forms.NumberInput(
                attrs={'class': 'form__field number-input', 'placeholder': 'Length in feet (sidewall)'}),
            'height': forms.NumberInput(
                attrs={'class': 'form__field number-input', 'placeholder': 'Height in feet (eave)'}),
            'style': forms.Select(attrs={'class': 'select-text select-input'}),
            'colour': forms.Select(attrs={'class': 'select-text select-input'}),
            'install': forms.Select(attrs={'class': 'select-text select-input'}),
            'insul_roof': forms.Select(attrs={'class': 'select-text select-input'}),
            'insul_walls': forms.Select(attrs={'class': 'select-text select-input'}),
            'gutters': forms.Select(attrs={'class': 'select-text select-input'}),
            'walk_doors': forms.NumberInput(
                attrs={'class': 'form__field number-input', 'placeholder': 'Walk Doors (people access)'}),
            'overhead_doors': forms.NumberInput(
                attrs={'class': 'form__field number-input', 'placeholder': 'Overhead Doors (vehicle access)'}),
            'oh_door_height': forms.NumberInput(
                attrs={'class': 'form__field number-input', 'placeholder': 'Size of Overhead Door'}),
            'oh_door_LE': forms.CheckboxInput(attrs={'class': 'mdc-checkbox__native-control'}),
            'oh_door_RE': forms.CheckboxInput(attrs={'class': 'mdc-checkbox__native-control'}),
            'oh_door_FS': forms.CheckboxInput(attrs={'class': 'mdc-checkbox__native-control'}),
            'oh_door_BS': forms.CheckboxInput(attrs={'class': 'mdc-checkbox__native-control'}),
            'additional': forms.Textarea(attrs={'class': 'form__field', 'placeholder': 'Additional Requirements',
                                                "rows": "5", "cols": "50"}),
        }


class RectangleForm(forms.ModelForm):
    def clean_side_ab(self):
        value = self.cleaned_data['side_ab']
        if ab := check_input(value):
            return value
        raise ValidationError("Input must be an integer or an integer/fraction eg. 1 1/2")

    def clean_side_ac(self):
        value = self.cleaned_data['side_ac']
        if ac := check_input(value):
            return value
        raise ValidationError("Input must be an integer or an integer/fraction eg. 1 1/2")

    def clean_side_bd(self):
        value = self.cleaned_data['side_bd']
        if bd := check_input(value):
            return value
        raise ValidationError("Input must be an integer or an integer/fraction eg. 1 1/2")

    def clean_side_cd(self):
        value = self.cleaned_data['side_cd']
        if cd := check_input(value):
            return value
        raise ValidationError("Input must be an integer or an integer/fraction eg. 1 1/2")

    def clean_diag_ad(self):
        value = self.cleaned_data['diag_ad']
        if ad := check_input(value):
            return value
        raise ValidationError("Input must be an integer or an integer/fraction eg. 1 1/2")

    def clean_diag_bc(self):
        value = self.cleaned_data['diag_bc']
        if bc := check_input(value):
            return value
        raise ValidationError("Input must be an integer or an integer/fraction eg. 1 1/2")

    class Meta:
        model = Rectangle
        fields = '__all__'
        labels = {
            'side_ab': _('Side AB'),
            'side_ac': _('Side AC'),
            'side_bd': _('Side BD'),
            'side_cd': _('Side CD'),
            'diag_ad': _('Diagonal AD'),
            'diag_bc': _('Diagonal BC'),
        }
        widgets = {
            'side_ab': forms.TextInput(attrs={'class': 'form__field text-input',
                                              'placeholder': 'Side AB'}),
            'side_ac': forms.TextInput(attrs={'class': 'form__field text-input',
                                              'placeholder': 'Side AC'}),
            'side_bd': forms.TextInput(attrs={'class': 'form__field text-input',
                                              'placeholder': 'Side BD'}),
            'side_cd': forms.TextInput(attrs={'class': 'form__field text-input',
                                              'placeholder': 'Side CD'}),
            'diag_ad': forms.TextInput(attrs={'class': 'form__field text-input',
                                              'placeholder': 'Diagonal AD'}),
            'diag_bc': forms.TextInput(attrs={'class': 'form__field text-input',
                                              'placeholder': 'Diagonal BC'}),

        }
