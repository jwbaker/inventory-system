from datetime import datetime
import re

from django.contrib.auth.models import User
from django.core.files import File
from django.core.validators import RegexValidator
from django.db import models


class AutocompleteData(models.Model):
    class Meta:
        # We don't want to have two locations (for instance) with the same name
        unique_together = ('name', 'kind',)
    KIND_CHOICES = [
        ('location', 'location'),
        ('manufacturer', 'manufacturer'),
        ('supplier', 'supplier'),
    ]
    name = models.CharField(max_length=255)
    kind = models.CharField(choices=KIND_CHOICES, max_length=255)

    def __unicode__(self):
        return self.name


class ItemFile(models.Model):
    class Meta:
        permissions = (
            ('view_deleted_itemfile', 'Can view deleted item files'),
        )

    MIMETYPES = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }
    description = models.TextField(blank=True, null=True)
    file_field = models.FileField(upload_to='files/%Y/%m/%d/')
    inventory_item = models.ForeignKey(
        # Using quotes evaluates this reference lazily, which lets us have
        # this circular reference
        'InventoryItem',
        blank=True,
        default=None,
        null=True
    )
    mimetype = models.CharField(max_length=255)
    to_display = models.BooleanField(default=True)

    def copy(self, parent_id):
        new_item_file = ItemFile()
        new_item_file.description = self.description
        new_item_file.mimetype = self.mimetype
        new_item_file.file_field = File(file(self.file_field.name))
        new_item_file.to_display = True
        new_item_file.inventory_item_id = parent_id
        new_item_file.save()

        return new_item_file

    def get_name_display(self):
        return self.description or self.file_field.name

    def save(self, *args, **kwargs):
        extension = re.search('.(\w+)$', self.file_field.name).group(1)
        self.mimetype = ItemFile.MIMETYPES.get(extension, '')
        super(ItemFile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_name_display()


class ItemImage(models.Model):
    class Meta:
        permissions = (
            ('view_deleted_itemimage', 'Can view deleted item images'),
        )
    description = models.TextField(blank=True, null=True)
    file_field = models.ImageField(upload_to='images/%Y/%m/%d/')
    inventory_item = models.ForeignKey(
        'InventoryItem',
        blank=True,
        default=None,
        null=True
    )
    to_display = models.BooleanField(default=True)


class InventoryItem(models.Model):
    class Meta:
        permissions = (
            ('view_item',         'Can view inventory items'),
            ('view_deleted_item', 'Can view deleted inventory items'),
        )

    STATUS_CHOICES = [
        ('SA', 'Stay'),
        ('SO', 'Storage'),
        ('SU', 'Surplussed'),
        ('LO', 'Lost'),
        ('DI', 'Disposed')
    ]

    @staticmethod
    def get_status(status_key):
        '''
        Looks up the display text of a given status key.

        Positional arguments:
            status_key -- The value of a status field.
                            One of: '', SA, SO, SU, LO, DI
        '''
        try:
            return [v[1] for v in InventoryItem.STATUS_CHOICES
                    if v[0] == status_key][0]
        except IndexError:
            # We return '' rather than None because the combination of Django
            # and JavaScript used in the detail page renders None as 'None'
            # (a string)
            return ''

    @staticmethod
    def get_status_key(status):
        '''
        Looks up the key of a given status text

        Positional arguments:
            status -- The display text of a status field
        '''
        try:
            return [v[0] for v in InventoryItem.STATUS_CHOICES
                    if v[1].lower() == status.lower()][0]
        except IndexError:
            return ''

    def get_comments_as_string(self):
        '''
        Packages the InventoryItem's comments into a space-delimited string.

        Use this method on the List page to make searching against comments as
        natural as possible.
        '''
        return ' '.join([str(f.body) for f in
                        [n for n in self.comment_set.all()]])

    def copy(self):
        copy = InventoryItem()
        for field in [attr for attr in vars(self) if attr != '_state']:
            if (
                'id' not in field and
                field not in ['creation_date', 'last_modified']
            ):
                setattr(copy, field, getattr(self, field))

        copy.supplier_id = self.supplier_id
        copy.technician_id = self.technician_id
        copy.owner_id = self.owner_id
        copy.manufacturer_id = self.manufacturer_id

        copy.save()

        for comment in self.comment_set.all():
            comment.copy(copy.id)

        for item_file in self.itemfile_set.all():
            new_file = item_file.copy(copy.id)

            if item_file.id == self.sop_file_id:
                copy.sop_file_id = new_file.id

        copy.save()
        return copy

    # save method is overriden so we can generate the UUID automatically
    def save(self, *args, **kwargs):
        super(InventoryItem, self).save()
        self.uuid = "{0}-{1}".format(
            self.creation_date.strftime('%Y%m%d'),
            self.id
        )
        # Double save so we can include a unique record ID in the UUID
        super(InventoryItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.uuid

    # These fields get automatically filled and cannot be edited
    creation_date = models.DateField(default=datetime.now)
    to_display = models.BooleanField(default=True)
    last_modified = models.DateTimeField(
        auto_now=True,
        default=datetime.now
    )

    # These fields are supplied by the user
    csa_cost = models.IntegerField(blank=True, default=None, null=True)
    csa_required = models.BooleanField(default=False)
    csa_special = models.BooleanField(default=False)
    csa_special_date = models.DateField(blank=True, default=None, null=True)
    description = models.TextField(blank=True, null=True)
    factory_csa = models.BooleanField(default=False)
    location = models.ForeignKey(
        AutocompleteData,
        blank=True,
        default=None,
        null=True,
        # Django complains because we have two fields that foreign key to the
        # same table. related_name defines the name of the reverse relation.
        # i.e. InventoryItem.locations.all() returns the set of locations
        # related to the given InventoryItem instance
        related_name='locations'
    )
    lifting_device = models.BooleanField(default=False)
    lifting_device_inspection_date = models.DateField(
        blank=True,
        default=None,
        null=True
    )
    manufacture_date = models.DateField(blank=True, default=None, null=True)
    manufacturer = models.ForeignKey(
        AutocompleteData,
        blank=True,
        default=None,
        null=True,
        # See the comment on InventoryItem.location field
        related_name='manufacturers'
    )
    model_number = models.CharField(
        blank=True,
        default=None,
        max_length=255,
        null=True,
    )
    modified_since_csa = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        User,
        blank=True,
        default=None,
        null=True,
        # See the comment on InventoryItem.location field
        related_name='owners'
    )
    purchase_date = models.DateField(blank=True, default=None, null=True)
    purchase_price = models.IntegerField(blank=True, default=None, null=True)
    replacement_cost = models.IntegerField(blank=True, default=None, null=True)
    replacement_cost_date = models.DateField(
        blank=True,
        default=None,
        null=True
    )
    serial_number = models.CharField(
        blank=True,
        default=None,
        max_length=255,
        null=True,
    )
    sop_file = models.ForeignKey(
        ItemFile,
        blank=True,
        default=None,
        null=True
    )
    sop_required = models.BooleanField(default=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='SA',
        max_length=2,
    )
    supplier = models.ForeignKey(
        AutocompleteData,
        blank=True,
        default=None,
        null=True,
        # See the comment on InventoryItem.location field
        related_name='suppliers'
    )
    tech_id = models.CharField(
        blank=True,
        default=None,
        max_length=255,
        null=True,
        validators=[
            RegexValidator(
                r'[A-Z]{2}-[0-9]*',
                'Must be of the form AA-0000'
            )
        ]
    )
    technician = models.ForeignKey(
        User,
        blank=True,
        default=None,
        null=True,
        # See the comment on InventoryItem.location field
        related_name='technicians'
    )
    undergraduate = models.BooleanField(default=False)
    uuid = models.CharField(
        max_length=255,
        # In reality this should *never* be null, but the only sane way to have
        # this field include the database ID is to do a preliminary save first,
        # but we have to insert a null value for that to happen
        null=True
    )


class Comment(models.Model):
    def copy(self, parent_id):
        new_comment = Comment()
        new_comment.author_id = self.author_id
        new_comment.body = self.body
        new_comment.inventory_item_id = parent_id
        new_comment.save()
        return new_comment

    def __unicode__(self):
        return self.body

    author = models.ForeignKey(User)
    body = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(default=datetime.now)
    inventory_item = models.ForeignKey(InventoryItem)
