from django import forms
from .models import Profile
from django.core.exceptions import ValidationError


class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'maxlength': 500,
            'placeholder': 'Tell us about yourself (max 500 characters)'
        }),
        max_length=500,
        required=False,
        help_text='Maximum 500 characters'
    )

    profile_pic = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/png,image/jpeg,image/gif'
        }),
        required=False,
        help_text='Upload a profile picture (PNG, JPEG, or GIF). Max file size: 5MB.'
    )

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')

        if profile_pic:
            # Check file size (5MB limit)
            if profile_pic.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be no more than 5MB.")

            # Optional: Check file type (though Django's ImageField does basic image validation)
            allowed_types = ['image/png', 'image/jpeg', 'image/gif']
            if profile_pic.content_type not in allowed_types:
                raise ValidationError("Only PNG, JPEG, and GIF images are allowed.")

        return profile_pic

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '').strip()

        # Optional additional bio validation
        if bio and len(bio) > 500:
            raise ValidationError("Bio cannot exceed 500 characters.")

        return bio