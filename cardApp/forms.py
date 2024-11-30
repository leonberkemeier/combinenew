from django import forms

from .models import ProjectCategory, Project, Card


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

class CardForm(forms.ModelForm):
    title=forms.CharField(required=True)
    front = forms.ImageField(required=False)
    back = forms.ImageField(required=False)
    fronttext = forms.CharField(required=False)
    backtext = forms.CharField(required=False)

    class Meta:
        model=Card
        fields=('title', 'front', 'back', 'fronttext', 'backtext')