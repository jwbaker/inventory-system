import pyexcel
import pyexcel.ext.xlsx

from django.core.exceptions import ValidationError

from uw_inventory.models import AutocompleteData, InventoryItem


def __get_autocomplete_term_or_create(name, kind, new_terms_list):
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


def parse_file(file_up):
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

                location = __get_autocomplete_term_or_create(
                    row['Location'],
                    'location',
                    new_terms,
                )
                kwargs['location_id'] = location.id or location.name

                manufacturer = __get_autocomplete_term_or_create(
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
                    new_items.append(kwargs)
        response = {
            'status': True,
            'message': 'Import successful',
            'new_items': new_items,
            'destination': 'uw_file_io.views.add_terms',
            'new_terms': new_terms,
        }
        return response


def __flatten_terms(term_hierarchy):
    return [{'kind': x, 'name': k} for (x, y) in term_hierarchy.iteritems()
            for (k, v) in y.iteritems() if v == {}]


def associate_terms(item_list, term_hierarchy):
    locations = term_hierarchy['location']
    manufacturers = term_hierarchy['manufacturer']
    for item in item_list:
        location_id = item['location_id']
        if (
            location_id in locations and
            'parent' in locations[location_id]
        ):
            item['location_id'] = locations[location_id]['parent']

        manufacturer_id = item['manufacturer_id']
        if (
            manufacturer_id in manufacturers and
            'parent' in manufacturers[manufacturer_id]
        ):
            item['manufacturer_id'] = manufacturers[manufacturer_id]['parent']

    return __flatten_terms(term_hierarchy)
