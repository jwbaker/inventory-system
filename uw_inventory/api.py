from django.contrib.auth.models import User

from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource

from uw_inventory.models import (
    AutocompleteData,
    InventoryItem,
    ItemImage,
    ItemFile
)


def permission(user):
    return user.has_perm('uw_inventory.view_item')


class PermissionAuthorization(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        if permission(bundle.request.user):
            return object_list
        else:
            raise Unauthorized('You do not have permission to view this API')

    def read_detail(self, object_list, bundle):
        return permission(bundle.request.user)


class InventoryItemResource(ModelResource):
    image = fields.ToManyField(
        'uw_inventory.api.ItemImageResource',
        'itemimage_set',
        null=True,
        blank=True,
        full=True
    )
    sop = fields.ToOneField(
        'uw_inventory.api.ItemFileResource',
        'sop_file',
        null=True,
        blank=True,
        full=True
    )
    manufacturer = fields.ToOneField(
        'uw_inventory.api.AutocompleteDataResource',
        'manufacturer',
        null=True,
        blank=True,
        full=True
    )
    supplier = fields.ToOneField(
        'uw_inventory.api.AutocompleteDataResource',
        'supplier',
        null=True,
        blank=True,
        full=True
    )
    location = fields.ToOneField(
        'uw_inventory.api.AutocompleteDataResource',
        'location',
        null=True,
        blank=True,
        full=True
    )
    owner = fields.ToOneField(
        'uw_inventory.api.UserResource',
        'owner',
        null=True,
        blank=True,
        full=True
    )
    technician = fields.ToOneField(
        'uw_inventory.api.UserResource',
        'technician',
        null=True,
        blank=True,
        full=True
    )

    class Meta:
        queryset = InventoryItem.objects.all()
        resource_name = 'InventoryItem'
        allowed_methods = ['get']
        authorization = PermissionAuthorization()
        authentication = SessionAuthentication()


class ItemImageResource(ModelResource):
    class Meta:
        queryset = ItemImage.objects.all()
        resource_name = 'ItemImage'


class ItemFileResource(ModelResource):
    class Meta:
        queryset = ItemFile.objects.all()
        resource_name = 'ItemFile'


class AutocompleteDataResource(ModelResource):
    class Meta:
        queryset = AutocompleteData.objects.all()
        resource_name = 'AutocompleteData'


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'User'
