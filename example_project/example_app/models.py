from django import forms
from django.db import models


class FeaturefulButton(models.Model):
    class Meta:
        app_label = 'example_app'
        verbose_name = 'Featureful Button'

    Prefix = models.CharField(max_length=200, blank=True)
    entity = models.CharField(
        max_length=200, verbose_name='Person', help_text='help text')


class SomeButton(FeaturefulButton):
    class Meta:
        app_label = 'example_app'


class GenericButtonModel(FeaturefulButton):
    class Meta:
        app_label = 'example_app'


class SomeMenubutton(FeaturefulButton):
    class Meta:
        app_label = 'example_app'


class IconMenubutton(FeaturefulButton):
    class Meta:
        app_label = 'example_app'


class GenericMenubutton(FeaturefulButton):
    class Meta:
        app_label = 'example_app'


class FeaturefulButtonForm(forms.ModelForm):
    class Meta:
        model = FeaturefulButton
        fields = '__all__'


class SomeButtonForm(forms.ModelForm):
    class Meta:
        model = SomeButton
        fields = '__all__'


class GenericButtonForm(forms.ModelForm):
    class Meta:
        model = GenericButtonModel
        fields = '__all__'


class SomeMenubuttonForm(forms.ModelForm):
    class Meta:
        model = SomeMenubutton
        fields = '__all__'


class IconMenubuttonForm(forms.ModelForm):
    class Meta:
        model = IconMenubutton
        fields = '__all__'


class GenericMenubuttonForm(forms.ModelForm):
    class Meta:
        model = GenericMenubutton
        fields = '__all__'
