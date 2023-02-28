# Exception
class IncorrectArgumentException(RuntimeError): pass


class BaseConverter:
    def __init__(self, base_digits: str):
        """
        Creates a conversion object between a positional numeral system in given base and decimal

        :param base_digits: Digits used in that positional numeral system
        :raises IncorrectArgumentException if base_digits parameter's length is smaller than 2
        :return: A conversion object
        """
        if len(base_digits) < 2:
            raise IncorrectArgumentException(f'Base is smaller than 2')
        self.base, self.digits = len(base_digits), base_digits

    def decimal_to_base(self, number: int) -> str:
        """
        Converting a natural number in decimal to given positional numeral system

        :param number: A natural number in decimal
        :raises IncorrectArgumentException if number is not a natural number
        :return: A number in given positional numeral system
        """
        from math import log
        if number < 0 or number % 1 != 0: raise IncorrectArgumentException(f'{number} is not a natural number')
        if number == 0: return self.digits[number]
        length, final = int(log(number) / log(self.base) + 1), ''
        for power in range(length):
            character = self.digits[number // self.base ** power % self.base]
            final += character
        return final[::-1]

    def base_to_decimal(self, number: str) -> int:
        """
        Converting a natural number in given positional numeral system to decimal

        :param number: A natural number in given positional numeral system
        :raises IncorrectArgumentException if number contains digits that are used in this numeral system
        :return: A number in decimal
        """
        for digit in number:
            if digit not in self.digits: raise IncorrectArgumentException(f"Digit '{digit}' is not used by this numberal system")
        length, decimal = len(number), 0
        for index in range(length): decimal += self.digits.find(number[length - index - 1]) * self.base ** index
        return decimal
