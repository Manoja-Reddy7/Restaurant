from django.db import models
from vendor.models import Vendor

from django.template.defaultfilters import slugify
from django.db import models, IntegrityError

# Create your models here.
class Category(models.Model):
    # at that time vendor account gets deleted it also deletes the Category model.
    vendor          = models.ForeignKey(Vendor,on_delete = models.CASCADE)
    category_name   = models.CharField(max_length = 30)
    slug            = models.SlugField(max_length = 30,unique= True )
    description     = models.TextField(max_length= 250,blank = True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now = True)
    
    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'
        
    def clean(self):
        self.category_name = self.category_name.capitalize()
    
    def __str__(self):
        return self.category_name
    

class FoodItem(models.Model):
    vendor          = models.ForeignKey(Vendor,on_delete = models.CASCADE)
    category_name   = models.ForeignKey(Category,on_delete = models.CASCADE,related_name='fooditems')
    food_title      = models.CharField(max_length=50)
    slug            = models.SlugField(max_length=30,unique=True)
    description     = models.TextField(max_length= 250,blank = True)
    price           = models.DecimalField(max_digits= 10, decimal_places = 2)
    img             = models.ImageField(upload_to='foodimages')
    is_available    = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now = True)
    
    class Meta:
        unique_together = ('food_title', 'vendor','slug')
    
    
   
    def clean(self):
        self.food_title = self.food_title.capitalize()
    
    def __str__(self):
        return self.food_title
  
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.food_name)
            self.slug = f"{slug_base}-{self.vendor.id}"
        
        original_slug = self.slug
        counter = 1
        
        while True:
            try:
                super().save(*args, **kwargs)
                break
            except IntegrityError:
                self.slug = f"{original_slug}-{counter}"
                counter += 1
    
def generate_unique_slug(model_instance, title, slug_field_name):
    slug = slugify(title)
    model_class = model_instance.__class__
    unique_slug = slug
    counter = 1

    while model_class.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug
    
     
