import os

from factory import get_search_class
from image_core import ImageCore

DEPTH_CHOICE = 0
GREEDY_CHOICE = 1
STAR_CHOICE = 2
COST_UNIFORM_CHOICE = 3
WIDTH_CHOICE = 4
ALGORITHMS_CHOICES = (
    (0, 'depth'),
    (1, 'greedy'),
    (2, 'star'),
    (3, 'cost_uniform'),
    (4, 'width'),
)


class App:

    IMAGE_SOURCE_PATH = os.path.join('source', 'image.png')

    def __init__(self, search_method=None):
        self.search_method_choice = dict(ALGORITHMS_CHOICES). \
            get(search_method, 0)

    def run(self):
        image_core = ImageCore(self.IMAGE_SOURCE_PATH)
        search = get_search_class(self.search_method_choice,
                                  image_core.image_array)
        search.get_problem_image_solution()
        search.get_search_response_payload()


if __name__ == '__main__':
    app = App(search_method=COST_UNIFORM_CHOICE)
    app.run()
