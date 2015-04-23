from django import template

register = template.Library()


@register.inclusion_tag('uw_inventory/comments_list.html')
def show_comments(comment_set, can_add):
    '''
    Shows the comments associated with an InventoryItem

    Positional arguments:
        comment_set -- The list of Comment objects associated with the
                       InventoryItem instance
        can_add -- True if the currently logged-in user is allowed to add
                   comments
    '''
    return {
        'comment_set': comment_set,
        'can_add': can_add
    }


@register.inclusion_tag('uw_inventory/images_list.html')
def show_images(image_set, can_add, can_edit, view_deleted):
    return {
        'image_set': image_set,
        'view_deleted': view_deleted,
        'can_add': can_add,
        'can_edit': can_edit,
    }
