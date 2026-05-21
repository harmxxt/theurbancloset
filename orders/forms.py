from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    """Checkout form - clean, simple, no extra field redefinitions"""

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone',
            'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country',
            'payment_method', 'notes',
        ]
        widgets = {
            'payment_method': forms.RadioSelect(),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Any special delivery instructions...'
            }),
            'address_line2': forms.TextInput(attrs={'placeholder': 'Apartment, suite, floor (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make address_line2 and notes optional
        self.fields['address_line2'].required = False
        self.fields['notes'].required = False

        # Apply luxury styling to all text inputs (not radio)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': 'form-control luxury-input'})

        # Pre-fill fields from logged-in user's profile
        if user:
            self.fields['full_name'].initial = user.get_full_name() or user.username
            self.fields['email'].initial = user.email
            try:
                profile = user.profile
                self.fields['phone'].initial = profile.phone
                self.fields['address_line1'].initial = profile.address_line1
                self.fields['address_line2'].initial = profile.address_line2
                self.fields['city'].initial = profile.city
                self.fields['state'].initial = profile.state
                self.fields['postal_code'].initial = profile.postal_code
                self.fields['country'].initial = profile.country
            except Exception:
                pass
