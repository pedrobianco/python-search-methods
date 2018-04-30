import importlib


def get_search_class(search_method_choice, image_array):
    module = 'search_methods.backends.{}'.format(search_method_choice)
    module = importlib.import_module(module)
    search_module = getattr(module, 'Search')
    search_class = search_module(image_array)
    return search_class
