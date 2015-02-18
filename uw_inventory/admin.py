from django.contrib import admin

from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemFile,
    Comment
)

admin.site.register(AutocompleteData)
admin.site.register(InventoryItem)
admin.site.register(ItemFile)
admin.site.register(Comment)
