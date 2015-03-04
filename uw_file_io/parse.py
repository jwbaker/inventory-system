import re

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

                if 'Location' in row and row['Location']:
                    location = __get_autocomplete_term_or_create(
                        row['Location'],
                        'location',
                        new_terms,
                    )
                    kwargs['location_id'] = location.id or location.name

                if 'Manufacturer' in row and row['Manufacturer']:
                    manufacturer = __get_autocomplete_term_or_create(
                        row['Manufacturer'],
                        'manufacturer',
                        new_terms,
                    )
                    kwargs['manufacturer_id'] = (
                        manufacturer.id or manufacturer.name
                    )

                if 'Supplier' in row and row['Supplier']:
                    supplier = __get_autocomplete_term_or_create(
                        row['Supplier'],
                        'supplier',
                        new_terms,
                    )
                    kwargs['supplier_id'] = (
                        supplier.id or supplier.name
                    )

                # Now for the flat fields
                for (col, val) in row.iteritems():
                    if col in [
                        'Attachements',
                        'ID',
                        'Location',
                        'Manufacturer',
                        'Supplier',
                        'Technician',
                        'Status',
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
                        'Undergraduate',
                    ]:
                        kwargs[col.lower()] = (
                            True if val == 'yes' else False
                        )
                    elif col in [
                        'Manufacture_Date',
                        'Purchase_Date',
                        'Replacement_Cost_Date',
                        'CSA_Special_Date',
                    ]:
                        if val:
                            date_components = val.split('-')
                            assembled_date = '{0}-{1}-{2}'.format(
                                date_components[2],
                                date_components[1],
                                date_components[0]
                            )
                            kwargs[col.lower()] = assembled_date
                        else:
                            kwargs[col.lower()] = None
                    elif col in [
                        'Purchase_Price',
                        'Replacement_Cost',
                        'CSA_Cost',
                    ]:
                        currencyRE = re.match(r'^\$(\d+)\.\d{2}$', val)
                        if currencyRE:
                            kwargs[col.lower()] = int(currencyRE.group(1))
                        else:
                            kwargs[col.lower()] = 0
                    elif col == 'Apparatus':
                        kwargs['name'] = val or None
                    elif col == 'Model':
                        kwargs['model_number'] = val or None
                    elif col == 'Tech_ID':
                        kwargs['tech_id'] = val or None
                    elif col == 'Serial':
                        kwargs['serial_number'] = val or None
                    elif col == 'Model':
                        kwargs['model_number'] = val or None
                    elif col == 'Notes':
                        kwargs['notes'] = val or None
                    elif col == 'Description':
                        kwargs['description'] = val or None

                item = InventoryItem(**kwargs)
                try:
                    item.full_clean(
                        exclude=[
                            'uuid',
                            'location',
                            'manufacturer',
                            'supplier'
                        ]
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


def process_terms_transactions(term_list):
    term_to_index = {}

    while len(term_list) > 0:
        term = term_list.pop(0)

        if term['action'] == 'skip':
            continue
        elif term['action'] == 'create':
            temp = AutocompleteData(
                kind=term['kind'],
                name=term['name']
            )
            temp.save()

            term_to_index[term['name']] = temp.id
        elif term['action'] == 'rename':
            if term['type'] == 'new->new':  # Assoc new with new
                if term['replace'] in term_to_index:
                    term_to_index[term['name']] = term_to_index[
                        term['replace']
                    ]
                else:
                    term_list.append(term)
            elif term['type'] == 'new->old':  # Assoc new with existing
                temp = AutocompleteData.objects.get(
                    kind=term['kind'],
                    name=term['replace']
                )
                term_to_index[term['name']] = temp.id
                term_to_index[term['replace']] = temp.id
            elif term['type'] == 'old->new':
                temp = AutocompleteData.objects.get(
                    kind=term['kind'],
                    name=term['name']
                )
                temp.name = term['replace']
                temp.save()
                term_to_index[term['replace']] = temp.id
                term_to_index[term['name']] = temp.id

    return term_to_index
