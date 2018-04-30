from search_methods.base import SearchAbstract


class Search(SearchAbstract):

    NAME = "Busca em Largura"

    def __init__(self, image_array):
        super(Search, self).__init__(image_array)

    def get_problem_image_solution(self):
        pass

    def get_search_response_payload(self):
        pass
