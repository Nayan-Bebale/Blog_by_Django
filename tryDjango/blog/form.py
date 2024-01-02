from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import BlogPost
from django.contrib.auth.models import User


class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

    
class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','image', 'slug', 'content', 'publish_date']


    def clean_title(self, *args, **kwargs):
        instance = self.instance
        # print(instance)
        title = self.cleaned_data.get("title")
        qs = BlogPost.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)  # id = instance.id
        if qs.exists():
            raise forms.ValidationError("This title has already been used. Please try again.")
        return title
    
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )

    full_name = forms.CharField(
        max_length=150,
        help_text='Required. Enter your full name.',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # Customize the appearance of the form fields
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    # You can add custom validation or override existing methods as needed
    # Example: Custom validation for the entire form
    def clean(self):
        cleaned_data = super().clean()
        # Your custom validation logic here
        return cleaned_data


class LoginForm(AuthenticationForm):
    # Customizing the LoginForm
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Add custom classes or attributes to form fields
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['remember_me'].widget.attrs.update({'class': 'form-check-input'})

    # You can custom validation
    def clean(self):
        cleaned_data = super().clean()
        # Your custom validation logic here
        return cleaned_data 