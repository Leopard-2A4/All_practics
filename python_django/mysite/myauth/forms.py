from django import forms
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "bio",
            "avatar",
        )

    def save(self, commit=True):
        user = super().save(commit)

        profile = user.profile
        profile.bio = self.cleaned_data["bio"]
        profile.avatar = self.cleaned_data["avatar"]

        profile.save()

        return user