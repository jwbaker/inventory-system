import reversion

from django.contrib import admin

from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemFile,
    ItemImage,
    Comment
)


class AutocompleteDataAdmin(reversion.VersionAdmin):
    pass


class InventoryItemAdmin(reversion.VersionAdmin):
    pass


class ItemFileAdmin(reversion.VersionAdmin):
    pass


class ItemImageAdmin(reversion.VersionAdmin):
    pass

admin.site.register(AutocompleteData, AutocompleteDataAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(ItemFile, ItemFileAdmin)
admin.site.register(ItemImage, ItemImageAdmin)
admin.site.register(Comment)
