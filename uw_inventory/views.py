from StringIO import StringIO
import json

import qrcode

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from django_cas.decorators import permission_required

from uw_inventory.forms import (
    CommentForm,
    FileForm,
    ImageForm,
    ItemForm
)
from uw_inventory.models import (
    AutocompleteData,
    Comment,
    InventoryItem,
    ItemFile,
    ItemImage
)


def _collect_messages(request):
    '''
    Loops through stored messages and packages them for consumption.

    We need to iterate through in order to mark the message as seen, otherwise
    it will keep displaying on every page.

    This method also converts the 'error' class into the 'danger' class, so
    bootstrap will recognize and render it properly.

    Positional arguments:
        request - The request object passed to the view
    '''
    storage = messages.get_messages(request)
    message_list = []
    for msg in storage:
        msg_class = msg.tags
        message_list.append({
            'message': msg.message,
            'class': 'danger' if ('error' in msg_class) else msg_class,
        })
    return message_list


def _json_builder_user(user):
    '''
    Converts a user into a JSON object for autocomplete consumption

    Positional arguments:
        user -- the Django User object
    '''
    if user.first_name and user.last_name:
        label = '{0} {1} ({2})'.format(
            user.first_name,
            user.last_name,
            user.username
        )
    else:
        label = user.username
    return {
        'id': user.id,
        'label': label,
        'value': label,
    }


def _json_builder_autocomplete(obj):
    '''
    Converts a term record into a JSON object for autocomplete consumption

    Positional arguments:
        obj -- the AutocompleteData object
    '''
    return {
        'id': obj.id,
        'label': obj.name,
        'value': obj.name,
    }


@permission_required('uw_inventory.view_item')
def inventory_list(request):
    request.session['_scrollY'] = 0
    message_list = _collect_messages(request)
    item_count = InventoryItem.objects.all().count()
    return render(request, 'uw_inventory/list.html', {
        'item_count': item_count,
        'page_messages': message_list,
    })


@csrf_protect
@permission_required('uw_inventory.view_item')
def inventory_detail(request, item_id):
    inventory_item = InventoryItem.objects.get(pk=item_id)

    if not inventory_item.qr_code:
        qr_code = qrcode.make(
            reverse('uw_inventory.views.inventory_detail', args=[item_id])
        )

        temp_io = StringIO()
        qr_code.save(temp_io)

        temp_file = InMemoryUploadedFile(
            temp_io,
            None,
            '{0}_qr.jpg'.format(item_id),
            'image/jpeg',
            temp_io.len,
            None
        )

        inventory_item.qr_code.save('{0}_qr.jpg'.format(item_id), temp_file)

    CommentCreateFormset = inlineformset_factory(
        InventoryItem,
        Comment,
        form=CommentForm,
        extra=0,
    )
    FileUploadFormset = inlineformset_factory(
        InventoryItem,
        ItemFile,
        form=FileForm,
        extra=0,
    )
    ImageUploadFormset = inlineformset_factory(
        InventoryItem,
        ItemImage,
        form=ImageForm,
        extra=0,
    )

    comment_formset = CommentCreateFormset(
        request.POST or None,
        prefix='comments',
        instance=inventory_item
    )
    file_formset = FileUploadFormset(
        request.POST or None,
        request.FILES or None,
        prefix='files',
        instance=inventory_item,
        queryset=ItemFile.objects.exclude(
            id=inventory_item.sop_file_id
        )
    )
    image_formset = ImageUploadFormset(
        request.POST or None,
        request.FILES or None,
        prefix='images',
        instance=inventory_item
    )
    sop_formset = FileUploadFormset(
        request.POST or None,
        request.FILES or None,
        prefix='sop',
        instance=inventory_item,
        queryset=ItemFile.objects.filter(id=inventory_item.sop_file_id)
    )

    if request.method == 'POST':
        request.session['_scrollY'] = request.POST.get('scroll-position')
        form = ItemForm(request.POST, request.FILES, instance=inventory_item)

        if (
          form.is_valid() and
          comment_formset.is_valid() and
          file_formset.is_valid() and
          image_formset.is_valid() and
          sop_formset.is_valid()
        ):
            new_item = form.save(commit=False)
            new_item.custom_form_data = request.POST.get(
                'custom_form_data',
                ''
            )
            sop_files = sop_formset.save(commit=False)
            map(lambda f: f.save(), sop_files)

            if sop_files:
                new_item.sop_file_id = sop_files[0].id
            new_item.save()
            comment_formset.save()
            file_formset.save()
            image_formset.save()

            messages.success(request,
                             'Item saved successfully')
        else:
            messages.error(request,
                           'Something went wrong. Check below for errors')
        return HttpResponseRedirect(
            reverse(
                'uw_inventory.views.inventory_detail',
                args=[inventory_item.id]
            )
        )

    else:
        form = ItemForm(instance=inventory_item)

    message_list = _collect_messages(request)
    return render(request, 'uw_inventory/detail.html', {
        'inventory_item': inventory_item,
        'form': form,
        'page_messages': message_list,
        'shown_excluded_fields': [
            {'label': 'Creation date', 'value': inventory_item.creation_date}
        ],
        'scrollY': request.session.get('_scrollY') or 0,
        'can_edit': request.user.has_perm('uw_inventory.change_inventoryitem'),
        'form_id': 'itemForm',
        'forms': {
            'comment': CommentForm(),
        },
        'formsets': {
            'comment': comment_formset,
            'file': file_formset,
            'image': image_formset,
            'sop': sop_formset,
        }
    })


@csrf_protect
@permission_required('uw_inventory.add_inventoryitem')
def inventory_add(request):
    request.session['_scrollY'] = 0
    CommentCreateFormset = inlineformset_factory(
        InventoryItem,
        Comment,
        form=CommentForm,
        extra=0
    )
    FileUploadFormset = inlineformset_factory(
        InventoryItem,
        ItemFile,
        form=FileForm,
        extra=0
    )
    ImageUploadFormset = inlineformset_factory(
        InventoryItem,
        ItemImage,
        form=ImageForm,
        extra=0
    )

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.custom_form_data = request.POST.get(
                'custom_form_data',
                ''
            )
            comment_formset = CommentCreateFormset(
                request.POST,
                prefix='comments',
                instance=new_item
            )
            file_formset = FileUploadFormset(
                request.POST,
                request.FILES,
                prefix='files',
                instance=new_item
            )
            image_formset = ImageUploadFormset(
                request.POST,
                request.FILES,
                prefix='images',
                instance=new_item
            )
            sop_formset = FileUploadFormset(
                request.POST,
                request.FILES,
                prefix='sop',
                instance=new_item
            )

            if (
              comment_formset.is_valid() and
              file_formset.is_valid() and
              image_formset.is_valid() and
              sop_formset.is_valid()
            ):
                sop_files = sop_formset.save(commit=False)
                map(lambda x: x.save(), sop_files)
                if sop_files:
                    new_item.sop_file_id = sop_files[0].id
                try:
                    new_item.save()
                except IndexError:
                    messages.error(
                        request,
                        '''Too many items have been created.
                        Please contact an administrator.'''
                    )
                else:
                    comment_formset.save()
                    file_formset.save()
                    image_formset.save()
                    map(
                        lambda x: setattr(x, 'inventory_item_id', new_item.id),
                        sop_files
                    )
                    map(lambda x: x.save(), sop_files)

                    messages.success(request,
                                     'Inventory item saved successfully')
                    return HttpResponseRedirect(
                        '/list/{0}'.format(new_item.pk)
                    )
            else:
                messages.error(request, 'Fatal formset badness')
        else:
            messages.error(request,
                           'Something went wrong. Check below for errors')
    else:
        form = ItemForm()

    message_list = _collect_messages(request)
    return render(request, 'uw_inventory/add.html', {
        'form': form,
        'page_messages': message_list,
        'can_add': request.user.has_perm('uw_inventory.add_inventoryitem'),
        'form_id': 'itemForm',
        'forms': {
            'file': FileForm(),
            'comment': CommentForm(),
        },
        'formsets': {
            'comment': CommentCreateFormset(prefix='comments'),
            'file': FileUploadFormset(prefix='files'),
            'image': ImageUploadFormset(prefix='images'),
            'sop': FileUploadFormset(prefix='sop'),
        }
    })


@permission_required('uw_inventory.view_item')
def inventory_label(request, item_id):
    item = InventoryItem.objects.get(id=item_id)

    return render(request, 'uw_inventory/label.html', {
        'item': item,
    })


@permission_required('uw_inventory.add_inventoryitem')
def inventory_copy(request, item_id):
    item = InventoryItem.objects.get(pk=item_id)

    try:
        new_item = item.copy()
    except IndexError:
        messages.error(
            request,
            '''Unable to copy. Too many items have been created.
            Please contact an administrator.'''
        )
        dest = item_id
    else:
        messages.success(
            request,
            'Successfully duplicated item {0}'.format(item.uuid)
        )
        dest = new_item.id

    return HttpResponseRedirect('/list/{0}'.format(dest))


@permission_required('uw_inventory.change_inventoryitem')
def inventory_delete(request, item_id):
    item = InventoryItem.objects.get(pk=item_id)
    item.to_display = False
    try:
        item.save()
    except:
        messages.error(request,
                       'Could not delete')
        dest = '/list/{0}'.format(item_id)
    else:
        messages.success(
            request,
            'Deleted item {0}'.format(item.uuid)
        )
        dest = '/list/'
    return HttpResponseRedirect(dest)


@permission_required('uw_inventory.change_inventoryitem')
def inventory_undelete(request, item_id):
    item = InventoryItem.objects.get(pk=item_id)
    item.to_display = True
    try:
        item.save()
    except:
        messages.error(
            request,
            'Could not restore'
        )
        dest = ''
    else:
        messages.success(
            request,
            'Restored item {0}'.format(item.uuid)
        )
        dest = item.id
    return HttpResponseRedirect('/list/{0}'.format(dest))


@permission_required('uw_inventory.change_inventoryitem')
def autocomplete_list(request, source):
    if request.is_ajax():
        query = request.GET.get('term', '')
        data = []

        if source in ['technician', 'owner']:
            result_set = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            json_builder = _json_builder_user
        else:
            result_set = AutocompleteData.objects.filter(
                kind=source,
                name__icontains=query
            )
            json_builder = _json_builder_autocomplete

        for result in result_set:
            data.append(json_builder(result))
        response = json.dumps(data)
    else:
        response = 'fail'
    mimetype = 'application/json'
    return HttpResponse(response, mimetype)


@csrf_protect
@permission_required('uw_inventory.add_autocompletedata')
def autocomplete_new(request):
    response = {}
    if request.is_ajax() and request.method == 'POST':
        name = request.POST['termName']
        data_set = request.POST['dataSet']
        try:
            if data_set == 'user':
                request_obj = User(
                    username=name,
                    first_name=request.POST['termFirstName'],
                    last_name=request.POST['termLastName']
                )
            else:
                request_obj = AutocompleteData(
                    name=name,
                    kind=data_set
                )
            request_obj.save()
        except IntegrityError:
            error = 'The {0} "{1}" already exists.'.format(data_set, name)
            response = json.dumps({'error': error})
        else:
            response = json.dumps({
                'id': request_obj.id,
                'name': request_obj.get_name_display(),
            })
    return HttpResponse(response, 'application/json')


@csrf_protect
@permission_required('change_autocompletedata')
def associate_terms(request):
    if request.method == 'POST':
        transactions_list = json.loads(request.POST['term_data'])

        for transaction in transactions_list:
            key = '{0}_id'.format(transaction['kind'])
            items_with_old_term = InventoryItem.objects.filter(**{
                key: transaction['old']
            })
            map(lambda i: setattr(i, key, transaction['new']), items_with_old_term)
            AutocompleteData.objects.get(
                id=transaction['old'],
                kind=transaction['kind']
            ).delete()

        return redirect('uw_inventory.views.associate_terms')
    else:
        terms = {}

        for choice in AutocompleteData.KIND_CHOICES:
            terms[choice[0]] = AutocompleteData.objects.filter(kind=choice[0])

    message_list = _collect_messages(request)
    return render(request, 'uw_inventory/associate_terms.html', {
        'page_messages': message_list,
        'terms': terms,
        'can_add': True,
        'can_edit': True,
        'form_id': 'term-form',
    })
