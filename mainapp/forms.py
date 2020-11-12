from django.contrib.auth.forms import AuthenticationForm

from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    """
    Форма захода пользователя
    """
    class Meta:
        model = ShopUser
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'