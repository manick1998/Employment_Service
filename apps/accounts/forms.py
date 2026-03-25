from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm

from .models import JobSeekerProfile, RecruiterProfile, User


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                css_class = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_class = 'form-select'
            elif isinstance(widget, forms.FileInput):
                css_class = 'form-control'
            elif isinstance(widget, forms.Textarea):
                css_class = 'form-control'
                widget.attrs.setdefault('rows', 4)
            else:
                css_class = 'form-control'
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {css_class}".strip()


class StyledAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class StyledPasswordChangeForm(BootstrapFormMixin, PasswordChangeForm):
    pass


class StyledPasswordResetForm(BootstrapFormMixin, PasswordResetForm):
    pass


class StyledSetPasswordForm(BootstrapFormMixin, SetPasswordForm):
    pass


class BaseSignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class JobSeekerSignUpForm(BaseSignUpForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.JOB_SEEKER
        if commit:
            user.save()
        return user


class RecruiterSignUpForm(BaseSignUpForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.RECRUITER
        if commit:
            user.save()
        return user


class UserUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class JobSeekerProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('phone', 'location', 'bio', 'years_of_experience', 'skills', 'resume')
        widgets = {
            'skills': forms.SelectMultiple(),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and resume.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Resume file size must be 2 MB or smaller.')
        return resume


class RecruiterProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ('designation', 'phone', 'contact_email', 'department')
