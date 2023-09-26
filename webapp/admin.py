from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from import_export.admin import ImportExportMixin

from .models import Listing, Price_History


class PriceHistoryAdmin(admin.TabularInline):
    model = Price_History


class ListingAdmin(ImportExportMixin, admin.ModelAdmin):
    # list_display = ('title','finn_code', 'Model','State',
    #                 'orignal_price', 'phone_number','link_url' ,'status_tag')
    list_display = (
        "title",
        "Brand",
        "Model",
        "orignal_price",
        "current_price",
        "Model_Year",
        "link_url",
        "status_tag",
    )
    search_fields = [
        "finn_code",
        "title",
        "description",
        "status",
    ]

    list_filter = (
        "status",
        "Boat_location",
        "State",
        "Type",
        "Brand",
        "Model_Year",
        "Engine_Included",
        "Engine_Type",
        "Color",
        "Sleeps",
        "Seating",
    )

    list_per_page = 15

    readonly_fields = ["finn_code", "status", "url"]

    inlines = [
        PriceHistoryAdmin,
    ]

    def get_queryset(self, request):
        return Listing.objects.prefetch_related("history")

    def current_price(self, obj: Listing):
        return format_html(obj.current_price_property)

    def link_url(self, obj):
        return format_html(
            f'<a href="{obj.url}" target="_blank"><i class="fas fa-link"></i></a>'
        )

    def image_tag(self, obj):
        return format_html(
            f"""\
        <img src="{obj.image}" width="auto" height="100"/>\
            <div id="myModal" class="modal">

            <span class="close">&times;</span>

            <img class="modal-content" id="img01">

            <div id="caption"></div>
        </div>
        """
        )

    def status_tag(self, obj):
        if obj.status:
            if obj.status == "Active":
                status_class = "active"
            elif obj.status == "Sold":
                status_class = "sold"
            elif obj.status == "SOLGT":
                status_class = "sold"
            elif obj.status == "Expired":
                status_class = "expired"
            elif obj.status == "Inaktiv":
                status_class = "inactive"
            else:
                status_class = "None"

            return format_html(f'<div class="{status_class}" >{obj.status}</div>')
        else:
            return format_html(f'<div class="" ></div>')

    image_tag.short_description = "Image"
    status_tag.short_description = "Status"


class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "listing",
        "changed_price",
        "price_changed_date",
        "last_changed_datetime",
    )
    list_per_page = 10


admin.site.register(Listing, ListingAdmin)
admin.site.register(Price_History, PriceHistoryAdmin)
