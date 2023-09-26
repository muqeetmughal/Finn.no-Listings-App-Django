from django.db import models

# Create your models here.


class Price_History(models.Model):
    listing = models.ForeignKey(
        "Listing",
        on_delete=models.CASCADE,
        related_name="history",
        db_index=True,
        editable=False,
    )
    changed_price = models.FloatField(null=True, blank=True, editable=False)
    price_changed_date = models.CharField(
        null=True, max_length=100, blank=True, editable=False
    )
    last_changed_datetime = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.listing)

    class Meta:
        unique_together = (("listing", "changed_price", "price_changed_date"),)


class Listing(models.Model):
    finn_code = models.IntegerField(unique=True, db_index=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # definitions_html = models.TextField(null=True,max_length=2000,blank=True)
    Boat_location = models.CharField(null=True, max_length=10, blank=True)
    State = models.CharField(null=True, max_length=10, blank=True)
    Type = models.CharField(null=True, max_length=100, blank=True)
    Brand = models.CharField(null=True, max_length=100, blank=True)
    Model = models.CharField(null=True, max_length=100, blank=True)
    Model_Year = models.CharField(null=True, max_length=5, blank=True)
    Length_feet = models.CharField(null=True, max_length=10, blank=True)
    Length_cm = models.CharField(null=True, max_length=10, blank=True)
    Width = models.CharField(null=True, max_length=100, blank=True)
    Depth = models.CharField(null=True, max_length=100, blank=True)
    Engine_Included = models.CharField(null=True, max_length=10, blank=True)
    Engine_Manufacturer = models.CharField(null=True, max_length=100, blank=True)
    Engine_Type = models.CharField(null=True, max_length=100, blank=True)
    Motorstr = models.CharField(null=True, max_length=100, blank=True)
    Max_Speed = models.CharField(null=True, max_length=100, blank=True)
    Fuel = models.CharField(null=True, max_length=100, blank=True)
    Weight = models.CharField(null=True, max_length=100, blank=True)
    Material = models.CharField(null=True, max_length=100, blank=True)
    Color = models.CharField(null=True, max_length=100, blank=True)
    Seating = models.CharField(null=True, max_length=5, blank=True)
    Sleeps = models.CharField(null=True, max_length=5, blank=True)
    orignal_price = models.FloatField(null=True, blank=True)
    last_changed = models.CharField(null=True, max_length=100, blank=True)
    last_changed_datetime = models.DateTimeField(null=True, blank=True, default=None)

    contact_name = models.CharField(null=True, max_length=100, blank=True)
    phone_number = models.CharField(null=True, max_length=100, blank=True)
    address = models.CharField(null=True, max_length=100, blank=True)
    image = models.CharField(null=True, max_length=300, blank=True)
    last_updated = models.CharField(null=True, max_length=100, blank=True)
    url = models.CharField(null=True, max_length=300, blank=True)
    status = models.CharField(null=True, max_length=100, blank=True)

    def __str__(self):
        return str(self.finn_code)

    @property
    def current_price_property(self):
        orignal_price = self.orignal_price
        last_price_change = self.history.filter().order_by("-id").first()
        if last_price_change:
            changed_price = last_price_change.changed_price
            if changed_price > orignal_price:
                color = "red"
            elif changed_price < orignal_price:
                color = "green"
            else:
                color = "yellow"

            return f"<span style='color:{color}'>{str(changed_price)}</span>"

        else:
            return str(orignal_price)
