from django.contrib import admin
from .models import Listing, Price_History
# Register your models here.
from django.utils.html import format_html
from import_export.admin import ImportExportMixin

class PriceHistoryAdmin(admin.TabularInline):
    model = Price_History

class ListingAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('title','finn_code', 'Model','State',
                    'orignal_price', 'phone_number','link_url' ,'status_tag')
    search_fields = ['finn_code', 'title', 'description','status', ]

    list_filter = ('status','Boat_location','State','Type','Brand','Model_Year','Engine_Included','Engine_Type','Color','Sleeps','Seating')

    list_per_page = 15

    readonly_fields = ["finn_code","status","url"]

    inlines = [
        PriceHistoryAdmin,
    ]

    def link_url(self, obj):
        return format_html(f'<a href="{obj.url}" target="_blank"><i class="fas fa-link"></i></a>')


    def image_tag(self, obj):
        return format_html(f"""\
        <img src="{obj.image}" width="auto" height="100"/>\
            <div id="myModal" class="modal">

            <span class="close">&times;</span>

            <img class="modal-content" id="img01">

            <div id="caption"></div>
        </div>
        """)

    def status_tag(self, obj):
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


        
        return format_html(f'<div class="{status_class}" >{obj.status}</div>')

    image_tag.short_description = 'Image'
    status_tag.short_description = "Status"



# class PriceHistoryAdmin(admin.ModelAdmin):
#     list_display = ("listing" , "changed_price","price_changed_date")

# class DefinitionAdmin(admin.ModelAdmin):
#     list_display = ('finn_code', 'title', 'Model', 'Brand',
#                     'Engine_Type', 'Fuel', 'Color', 'Seating', 'Sleeps')


admin.site.register(Listing, ListingAdmin)
# admin.site.register(Price_History,PriceHistoryAdmin)
# admin.site.register(Definition, DefinitionAdmin)
