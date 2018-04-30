class SearchAbstract:

    def __init__(self, image_array):
        self.image_array = image_array

    def get_problem_image_solution(self):
        return NotImplementedError

    def get_search_response_payload(self):
        return NotImplementedError
