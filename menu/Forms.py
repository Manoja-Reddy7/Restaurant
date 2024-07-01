from django import forms
from .models import Category,FoodItem

from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model   = Category
        fields  = ['category_name','description']
        
class FoodItemForm(forms.ModelForm):
    img = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}),validators=[allow_only_images_validator])
    
    class Meta:
        model  = FoodItem
        fields = ['category_name','description','food_title','price','img','is_available']
        
    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)
        if self.vendor:
            self.fields['category_name'].queryset = Category.objects.filter(vendor=self.vendor)
        
    def clean(self):
        cleaned_data = super().clean()
        food_title = cleaned_data.get('food_title')
        
        if self.vendor and food_title:
            
            if FoodItem.objects.filter(food_title=food_title, vendor=self.vendor).exists():
                print("Duplicate found in the database.")
                self.add_error('food_title', 'A FoodItem with this title already exists for this vendor.')
        
        return cleaned_data
    
    
    
        
    