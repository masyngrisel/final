from django.forms.models import inlineformset_factory
from django import forms
from .models import Course, Module, Portfolio

ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    fields=['title', 'description'],
    extra=2,
    can_delete=True,
)



class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'content_type', 'file', 'image', 'video_url', 'course']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }