import pyexcel
import pyexcel.ext.xlsx

from django.core.exceptions import ValidationError

from uw_inventory.models import AutocompleteData, InventoryItem


def __get_autocomplete_term_or_insert(name, kind, new_terms_list):
    try:
        var = AutocompleteData.objects.get(
            name__iexact=name,
            kind=kind
        )
    except AutocompleteData.DoesNotExist:
        var = AutocompleteData(name=name, kind=kind)
        if kind not in new_terms_list:
            new_terms_list[kind] = []

        # This is another uniqueness test - we don't want to add the same item
        # to our new_terms list twice.

        # This function call essentially boils down to a long if-chain, so that
        # array_contains = list[0] == var.name or list[1] == var.name or ...

        # If any one element in the array fails the test, the whole thing will
        # be false.
        array_contains = reduce(
            lambda b, i: b or i.name == var.name,
            new_terms_list[kind],
            False
        )

        if not array_contains:
            new_terms_list[kind].append(var)
    return var


def parse(file_up):
    extension = file_up.name.split('.')[1]
    try:
        sheet = pyexcel.load_from_memory(
            extension,
            file_up.read(),
            name_columns_by_row=0
        )
    except NotImplementedError:
        return {
            'status': False,
            'message': '''Invalid file type {0}. Please upload one of: xls, xlsx, csv.
            '''.format(extension),
            'destination': 'uw_file_io.views.file_import',
        }

    else:
        data = sheet.to_records()
        new_terms = {}
        new_items = []
        for row in data:
            if row['ID']:
                # If saving goes south, we're going to want to back out of
                # any datatabse changes, so keep track of them
                kwargs = {}

                location = __get_autocomplete_term_or_insert(
                    row['Location'],
                    'location',
                    new_terms,
                )
                kwargs['location_id'] = location.id or location.name

                manufacturer = __get_autocomplete_term_or_insert(
                    row['Manufacturer'],
                    'manufacturer',
                    new_terms,
                )
                kwargs['manufacturer_id'] = (
                    manufacturer.id or manufacturer.name
                )

                # Now for the flat fields
                for (col, val) in row.iteritems():
                    if col in [
                        'Attachements',
                        'ID',
                        'Location',
                        'Manufacturer',
                        'Technician',
                        'Owner',
                        'SOP',
                        'Picture',
                        'Lifting_Device_Inspected_By',
                    ]:
                        continue
                    elif col in [
                        'CSA_Required',
                        'Factory_CSA',
                        'CSA_Special',
                        'Modified_Since_CSA',
                    ]:
                        kwargs[col.lower()] = (
                            True if val == 'yes' else False
                        )
                    elif col == 'Apparatus':
                        kwargs['name'] = val or None
                    elif col == 'Model':
                        kwargs['model_number'] = val or None

                item = InventoryItem(**kwargs)
                try:
                    item.full_clean(
                        exclude=['uuid', 'location', 'manufacturer']
                    )
                except ValidationError as e:
                    print e
                    # Back out of all changes so far
                    return {
                        'status': False,
                        'message': '''Failed to insert row {0}. Please look at your file
                                    and try again.'''.format(row['ID']),
                        'destination': 'uw_file_io.views.file_import',
                    }
                else:
                    new_items.append(item)
        response = {
            'status': True,
            'message': 'Import successful',
        }
        if new_terms:
            response.update({
                'destination': 'uw_file_io.views.add_terms',
                'new_terms': new_terms,
                'new_item_args': new_items,
            })
        else:
            response.update({
                'destination': 'uw_inventory.views.inventory_list',
                'new_item_args': new_items,
            })
        return response
