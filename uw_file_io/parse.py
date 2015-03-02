import pyexcel
import pyexcel.ext.xlsx

from django.db import IntegrityError

from uw_inventory.models import AutocompleteData, InventoryItem


def __get_autocomplete_term_or_insert(name, kind):
    try:
        var = AutocompleteData.objects.get(
            name__iexact=name,
            kind=kind
        )
    except AutocompleteData.DoesNotExist:
        var = AutocompleteData(name=name, kind=kind)
        var.save()
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
            '''.format(extension)
        }

    else:
        data = sheet.to_records()
        for row in data:
            if row['ID']:
                # If saving goes south, we're going to want to back out of
                # any datatabse changes, so keep track of them
                inserted_rows = []
                kwargs = {}

                location = __get_autocomplete_term_or_insert(
                    row['Location'],
                    'location'
                )
                kwargs['location_id'] = location.id
                inserted_rows.append(location)

                manufacturer = __get_autocomplete_term_or_insert(
                    row['Manufacturer'],
                    'manufacturer'
                )
                kwargs['manufacturer_id'] = manufacturer.id
                inserted_rows.append(manufacturer)

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
                    item.save()
                except IntegrityError:
                    # Back out of all changes so far
                    map(lambda x: x.delete(), inserted_rows)
                    return {
                        'status': False,
                        'message': '''Failed to insert row {0}. Please look at your file
                        and try again.'''.format(row['ID'])
                    }
                else:
                    inserted_rows.append(item)

            return {
                'status': True,
                'message': 'Import successful'
            }
