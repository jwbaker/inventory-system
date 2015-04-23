from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource

from uw_inventory.models import (
    InventoryItem,
    ItemImage,
    ItemFile
)
from uw_inventory.templatetags.uw_inventory_misc_tags import contexual_file_icon


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

    def dehydrate(self, bundle):
        bundle.data['location'] = getattr(bundle.obj.location, 'name', '')
        bundle.data['manufacturer'] = getattr(
            bundle.obj.manufacturer,
            'name',
            ''
        )
        bundle.data['comments'] = bundle.obj.get_comments_as_string()
        if bundle.obj.owner:
            bundle.data['owner'] = {
                'name': bundle.obj.owner.get_name_display(),
                'username': bundle.obj.owner.username
            }
        else:
            bundle.data['owner'] = {
                'name': '',
                'username': ''
            }
        if bundle.obj.technician:
            bundle.data['technician'] = {
                'name': bundle.obj.technician.get_name_display(),
                'username': bundle.obj.technician.username
            }
        else:
            bundle.data['technician'] = {
                'name': '',
                'username': ''
            }
        if bundle.obj.sop_file:
            bundle.data['sop'] = {
                'url': bundle.obj.sop_file.file_field.url,
                'icon_class': contexual_file_icon(
                    bundle.obj.sop_file
                )['file_class'],
            }
        else:
            bundle.data['sop'] = {
                'url': '',
                'icon_class': '',
            }
        return bundle

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
