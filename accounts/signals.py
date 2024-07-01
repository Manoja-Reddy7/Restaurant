from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import UserProfile,User

# The below @receiver(post_save,sender=User) will create UserProfile when user is created
    
@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwrgs ):
    # case 1: If user is created then automatically Userprofile gets created.
    if created:
        UserProfile.objects.create(user=instance)
    # case 2: If user is trying to update the User class,but UserProfile is not created then we will handle here.
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)            
@receiver(pre_save,sender=User)           
def  pre_save_create_profile(sender,instance,**kwrgs):
       pass
