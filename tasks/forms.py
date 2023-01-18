from django import forms
from .models import Task

class CreateTaskForm(forms.ModelForm):
    class Meta:
        # Modelo a usar en el form
        model = Task
        # Campos a mostrar y usar en el form
        # el usuario no es necesario mencionarlo porque va automático
        fields = ["title","description","important"]
        # los widgets sirven para agregar clases 
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }