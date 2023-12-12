#  Copyright (c) 2023 - Muzaffar Makhkamov
#
#
#  This file is part of  "Django JsonRPC Server Template".
#
#  "Django JsonRPC Server Template" is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  "Django JsonRPC Server Template" is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with "Django JsonRPC Server Template".  If not, see <http://www.gnu.org/licenses/>.

# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm

from v1.models import Partner


class PartnerCreationForm(UserCreationForm):
    file_password = forms.CharField(max_length=100, required=True, help_text='Enter zip file password')

    class Meta:
        model = Partner
        fields = UserCreationForm.Meta.fields + ('file_password',)

    # def save(self, commit=True):
    #     user = super(BaseUserCreationForm).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"], self.cleaned_data['file_password'])
    #     if commit:
    #         user.save()
    #         if hasattr(self, "save_m2m"):
    #             self.save_m2m()
    #     return user
