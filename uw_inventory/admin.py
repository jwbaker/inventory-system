from django.contrib import admin

from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemFile,
    ItemImage,
    Comment
)

admin.site.register(AutocompleteData)
admin.site.register(InventoryItem)
admin.site.register(ItemFile)
admin.site.register(ItemImage)
admin.site.register(Comment)
