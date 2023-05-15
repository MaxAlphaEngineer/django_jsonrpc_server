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

from django import forms
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
    status = models.SmallIntegerField(default=StatusType.ACTIVE.value, choices=StatusType.choices)
    logging = models.SmallIntegerField(default=LoggingType.OFF.value, choices=LoggingType.choices)
    is_test = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return f'Service: {self.method_name} -> status: {self.StatusType.choices[self.status][1]}'

    def is_active(self):
        now = timezone.now()

        tip = TechnicalIssuePeriod.objects.filter(
            service_id=self.id,
            start_timestamp__lte=now,
            end_timestamp__gte=now
        ).exists()

        if not tip:
            if self.status != self.StatusType.ACTIVE.value:
                self.status = self.StatusType.ACTIVE.value
                self.save(update_fields=['status'])

        return self.status


class TechnicalIssuePeriod(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    start_timestamp = models.DateTimeField(default=timezone.now)
    end_timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.end_timestamp = self.start_timestamp + timezone.timedelta(minutes=self.duration)
        super().save(*args, **kwargs)


class TechnicalIssuePeriodForm(forms.ModelForm):
    class Meta:
        model = TechnicalIssuePeriod
        exclude = ['end_timestamp']

    def clean(self):
        cleaned_data = super().clean()
        start_timestamp = cleaned_data.get('start_timestamp')
        duration = cleaned_data.get('duration')
        if start_timestamp and duration:
            cleaned_data['end_timestamp'] = start_timestamp + timezone.timedelta(minutes=duration)

        return cleaned_data
