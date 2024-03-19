from datetime import date

# Exceptions
class IncorrectDataError(ValueError): pass
class WrongPESELException(ValueError): pass

class PESEL():
    def __init__(self, date_of_birth: date = None, sequential_number: str = None, pesel: str = None):
        """
        Creates a PESEL data object.\n
        Input "date_of_birth" and "sequential_number" parameter to create PESEL from data or "pesel" parameter to parse from PESEL.
        :param date_of_birth: Date of birth
        :param sequential_number: Sequential number
        :param pesel: PESEL to parse
        :raises IncorrectDataError: if invalid params combination is used
        """
        if date_of_birth is not None and sequential_number is not None and pesel is None: self.__create_from_data(date_of_birth, sequential_number)
        elif date_of_birth is None and sequential_number is None and pesel is not None: self.__parse_from_pesel_string(pesel)
        else: raise IncorrectDataError("Wrong arguments")

    def __create_from_data(self, date_of_birth: date, sequential_number: int):
        """
        Creates a PESEL object from data.
        :param date_of_birth: Date of birth
        :param sequential_number: Sequential number
        :raises IncorrectDataError: if
        :return: Nothing, creates values in objects instead.
        """
        centuries = {18: 80, 19: 0, 20: 20, 21: 40, 22: 60}
        if date_of_birth < date(1800, 1, 1) or date_of_birth > date(2299, 12, 31): raise IncorrectDataError('Incorrect date of birth')
        if sequential_number < 0 or sequential_number > 10**4 - 1: raise IncorrectDataError('Incorrect sequence number')
        self.__date_of_birth = date_of_birth
        self.__sequential_number = sequential_number
        self.__sex = 'F' if sequential_number % 2 == 0 else 'M'
        pesel_string = f'{str(date_of_birth.year % 100).zfill(2)}{str(centuries[date_of_birth.year // 100] + date_of_birth.month).zfill(2)}' \
                       f'{str(date_of_birth.day).zfill(2)}{str(self.__sequential_number).zfill(4)}'
        self.__calculate_checksum(pesel_string)
        self.__pesel_string = f'{pesel_string}{self.__checksum}'

    def __parse_from_pesel_string(self, pesel: str):
        """
        Parses PESEL string.
        :param pesel: PESEL to parse
        :raises WrongPESELException: if PESEL length is invalid, PESEL is not a number or checksum is invalid
        :return: Nothing, creates values in objects instead.
        """
        if len(pesel) != 11: raise WrongPESELException('Invalid PESEL length')
        try: _ = int(pesel)
        except ValueError: raise WrongPESELException('Invalid PESEL')
        centuries, year_2_digit, month, day = (19, 20, 21, 22, 18), pesel[0:2], pesel[2:4], pesel[4:6]
        year, checksum = centuries[int(month) // 20] * 100 + int(year_2_digit), self.__calculate_checksum(pesel)
        if str(self.__checksum) != pesel[-1]: raise WrongPESELException('Invalid checksum')
        self.__pesel_string = pesel
        self.__date_of_birth = date(year, int(month) % 20, int(day))
        self.__sequential_number = int(pesel[6:10])
        self.__sex = 'F' if int(pesel[-2]) % 2 == 0 else 'M'

    def __calculate_checksum(self, pesel: str):
        """
        Calculates PESEL's checksum
        :param pesel: PESEL
        :return: Nothing, creates value "checksum" in object instead.
        """
        weight = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
        weighted_sum = (sum([int(pesel[i]) * weight[i] for i in range(10)]) % 10)
        self.__checksum = 0 if weighted_sum == 0 else (10 - weighted_sum)

    # Getters
    def __str__(self) -> str: return self.__pesel_string
    def get_date_of_birth(self) -> date: return self.__date_of_birth
    def get_sequential_number(self) -> int: return self.__sequential_number
    def get_sex(self) -> str: return self.__sex
    def get_checksum(self) -> int: return self.__checksum
