from django.contrib import admin

from uw_inventory.models import AutocompleteData, InventoryItem

admin.site.register(AutocompleteData)
admin.site.register(InventoryItem)
