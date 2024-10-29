from requests.exceptions import JSONDecodeError


class CustomExeption(Exception):
    pass


class ApiNotFoundExeption(CustomExeption):
    pass


class DataNotJsonExeption(JSONDecodeError, CustomExeption):
    pass


class EmptyResultExeption(CustomExeption):
    pass
