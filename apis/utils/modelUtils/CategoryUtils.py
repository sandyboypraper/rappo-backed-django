from apis.models.Category import *

def convertCategoriesToObjs(category_names):
    category_names_objects = []
    for category_name in category_names:
        category_name_object = Category.objects.get_or_create(category_title = category_name)[0]
        category_names_objects.append(category_name_object)
    return category_names_objects