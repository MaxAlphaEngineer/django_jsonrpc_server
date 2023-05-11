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
from django.db import models
from django.utils import timezone


class Services(models.Model):
    class StatusType(models.Choices):
        ACTIVE = 0
        TEMPORARILY = 1
        DEPRECATED = 2

    class LoggingType(models.Choices):
        OFF = 0
        USER_BASED = 1
        SERVICE_BASED = 2

    method_name = models.CharField(max_length=50, default="")
    status = models.SmallIntegerField(default=0, choices=StatusType.choices)
    logging = models.SmallIntegerField(default=0, choices=LoggingType.choices)
    is_test = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return f'Service: {self.method_name} -> status: {self.StatusType.choices[self.status][1]}'


class TechnicalIssuePeriod(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    duration = models.DurationField()
    start_timestamp = models.DateTimeField(default=timezone.now)
    end_timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.end_timestamp = self.start_timestamp + self.duration
        super().save(*args, **kwargs)

    def is_active(self):
        now = timezone.now()
        status = self.start_timestamp <= now <= self.end_timestamp
        return status


from django import forms

from django.utils import timezone


class TechnicalIssuePeriodForm(forms.ModelForm):
    class Meta:
        model = TechnicalIssuePeriod
        exclude = ['end_timestamp']

    def clean(self):
        cleaned_data = super().clean()
        start_timestamp = cleaned_data.get('start_timestamp')
        duration = cleaned_data.get('duration')
        print(type(duration))
        if start_timestamp and duration:
            # duration_minutes = int(duration)  # Ensure duration is an integer
            cleaned_data['end_timestamp'] = start_timestamp + duration

        return cleaned_data
