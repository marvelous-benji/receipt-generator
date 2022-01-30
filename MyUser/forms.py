from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    '''
    Form for user creation from the admin interface (not neccessarily needed)
    '''

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "fullname",
            "business_name",
        )


class CustomUserChangeForm(UserChangeForm):
    '''
    Form for user update from the admin interface (not neccessarily needed)
    '''
    
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "fullname",
            "business_name",
        )
