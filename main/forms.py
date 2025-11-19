from django.forms import ModelForm
from main.models import Product, News

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "thumbnail", "stock", "brand", "description", "is_featured"]

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "category", "thumbnail", "is_featured"]