from pesel import *
from base_converter import BaseConverter

# Creates a niftimal base converter
nc = BaseConverter('0123456789abcdefghijklmnopqrstuvwxyz')

# Exception
class WrongIDException(WrongPESELException): pass

class ID_Number:
    def __init__(self, date_of_birth: date = None, sequential_number: str = None, id_number: str = None, pesel: str = None):
        """
        Creates an ID number data object.\n
        Input "date_of_birth" and "sequential_number" parameter to create ID number from data,
        "id_number" parameter to parse from ID number or "pesel" parameter to parse from PESEL.
        :param date_of_birth: Date of birth
        :param sequential_number: Sequential number
        :param id_number: ID number to parse
        :param pesel: PESEL to parse
        :except IncorrectDataError: if invalid params combination is used
        """
        self.__minimal_date = date(1800, 1, 1)
        if date_of_birth is not None and sequential_number is not None and id_number is None and pesel is None: self.__create_from_data(date_of_birth, sequential_number)
        elif date_of_birth is None and sequential_number is None and id_number is not None and pesel is None: self.__parse_from_id_string(id_number)
        elif date_of_birth is None and sequential_number is None and id_number is None and pesel is not None: self.__parse_from_pesel(pesel)
        else: raise IncorrectDataError("Wrong arguments")

    def __create_from_data(self, date_of_birth: date, sequential_number: int):
        """
        Creates an ID object from data.
        :param date_of_birth: Date of birth
        :param sequential_number: Sequential number
        :raises IncorrectDataError: if sequential number is negative or has more than 3 digits in the niftimal base OR
        if date of birth is before January 1, 1800, or after the maximal date (August 8, 6398)
        :return: Nothing, creates values in objects instead.
        """
        if sequential_number < 0 or sequential_number > 36**3 - 1: raise IncorrectDataError('Invalid sequential number')
        if self.__minimal_date > date_of_birth or date_of_birth >= date(6398, 8, 20): raise IncorrectDataError('Invalid date')
        self.__general_init(date_of_birth, sequential_number)

    def __general_init(self, date_of_birth: date, sequential_number: int):
        """
        Creates an ID object from data.
        :param date_of_birth: Date of birth
        :param sequential_number: Sequential number
        :return: Nothing, creates values in objects instead.
        """
        self.__date_of_birth = date_of_birth
        self.__sequential_number = sequential_number
        self.__sex = 'F' if ((sequential_number % 100) / 10) % 2 == 0 else 'M'
        id_string = f'{nc.decimal_to_base((date_of_birth - self.__minimal_date).days).zfill(4)}-{nc.decimal_to_base(sequential_number).zfill(2)}'
        weights, base, checksum = (1, 3, 7, 9, 0, 1, 3, 7), 36, 0
        for index, character in enumerate(id_string):
            if character == '-': continue
            checksum += int(character, base) * weights[index]
        self.__checksum = nc.decimal_to_base((base - checksum % base) % base)
        self.__id_string = f'{id_string[0:4]}-{id_string[4:].lstrip("-")}{self.__checksum}'

    def __parse_from_id_string(self, id_string: str):
        """
        Parses ID number string.
        :param id_string: ID number to parse
        :raises WrongIDException: if ID number is in wrong format, checksum is incorrect or there's a bug in the ID string creation algorithm
        :return: Nothing, creates values in objects instead.
        """
        from datetime import timedelta
        from re import match
        if match(r'[0-9a-z]{4}-[0-9a-z]{3}', id_string) is None: raise WrongIDException('Incorrect ID')
        date_of_birth = self.__minimal_date + timedelta(days=nc.base_to_decimal(id_string[0:4]))
        self.__general_init(date_of_birth, nc.base_to_decimal(id_string[5:7]))
        if self.__checksum != id_string[-1]: raise WrongIDException('Incorrect checksum')
        if self.__id_string != id_string: raise WrongIDException('Error in id string creation algorithm')

    def __parse_from_pesel(self, pesel: str):
        """
        Parses PESEL string.
        :param pesel: PESEL to parse
        :raises WrongPESELException: if PESEL length is invalid, PESEL is not a number or checksum is invalid
        :return: Nothing, creates values in objects instead.
        """
        pesel_object = PESEL(pesel=pesel)
        self.__general_init(pesel_object.get_date_of_birth(), pesel_object.get_sequential_number())

    # Getters
    def __str__(self): return self.__id_string
    def get_date_of_birth(self) -> date: return self.__date_of_birth
    def get_sequential_number(self) -> int: return self.__sequential_number
    def get_sex(self) -> str: return self.__sex
    def get_checksum(self) -> int: return self.__checksum
