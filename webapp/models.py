from django.db import models

# Create your models here.

class Price_History(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE,related_name='history')
    changed_price = models.CharField(null=True,max_length=50,blank=True)
    price_changed_date = models.CharField(null=True,max_length=50,blank=True)
    def __str__(self):
        return str(self.listing)

    class Meta:
        unique_together = (("listing", "changed_price", "price_changed_date"),)
    
class Listing(models.Model):
    finn_code = models.IntegerField(unique=True)
    title = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,max_length=20000,blank=True)
    # definitions_html = models.TextField(null=True,max_length=2000,blank=True)
    Boat_location = models.CharField(null=True,max_length=10,blank=True)
    State = models.CharField(null=True,max_length=10,blank=True)
    Type = models.CharField(null=True,max_length=50,blank=True)
    Brand = models.CharField(null=True,max_length=50,blank=True)
    Model = models.CharField(null=True,max_length=50,blank=True)
    Model_Year = models.CharField(null=True,max_length=5,blank=True)
    Length_feet = models.CharField(null=True,max_length=10,blank=True)
    Length_cm = models.CharField(null=True,max_length=10,blank=True)
    Width = models.CharField(null=True,max_length=20,blank=True)
    Depth = models.CharField(null=True,max_length=20,blank=True)
    Engine_Included = models.CharField(null=True,max_length=10,blank=True)
    Engine_Manufacturer = models.CharField(null=True,max_length=50,blank=True)
    Engine_Type = models.CharField(null=True,max_length=50,blank=True)
    Motorstr = models.CharField(null=True,max_length=20,blank=True)
    Max_Speed = models.CharField(null=True,max_length=20,blank=True)
    Fuel = models.CharField(null=True,max_length=20,blank=True)
    Weight = models.CharField(null=True,max_length=20,blank=True)
    Material = models.CharField(null=True,max_length=20,blank=True)
    Color = models.CharField(null=True,max_length=20,blank=True)
    Seating = models.CharField(null=True,max_length=5,blank=True)
    Sleeps= models.CharField(null=True,max_length=5,blank=True)
    orignal_price = models.BigIntegerField(null=True,blank=True)
    last_changed = models.CharField(null=True,max_length=100,blank=True)
    contact_name = models.CharField(null=True,max_length=100,blank=True)
    phone_number = models.CharField(null=True,max_length=100,blank=True)
    address = models.CharField(null=True,max_length=100,blank=True)
    image = models.CharField(null=True,max_length=300,blank=True)
    last_updated = models.CharField(null=True,max_length=100,blank=True)
    url = models.CharField(null=True,max_length=300,blank=True)
    status = models.CharField(null=True,max_length=100,blank=True)
    
    def __str__(self):
        return str(self.finn_code)