from django import forms

from .models import ProjectCategory, Project


class ProjectCategoryForm(forms.ModelForm):
    name=forms.CharField(required=True)

    class Meta:
        model = ProjectCategory
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
        }

class ProjectForm(forms.ModelForm):
    name=forms.CharField(required=True)
    category=forms.models.ModelChoiceField(queryset=ProjectCategory.objects.all())

    class Meta:
        model = Project
        fields = ('name', 'category')