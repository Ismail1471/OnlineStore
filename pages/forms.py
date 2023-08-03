from django.forms import ModelForm
from .models import Product, Review
from django import forms


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["title", "price", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Напишите название продукта"
            }),
            "price": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Напишите цену продукта"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Напишите описание продуктF"
            })
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Напишите здесь свой отзыв..."
            })
        }