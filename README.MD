Creates a PESEL data object from a date of birth and sequence number or PESEL number.<br>
Create ID number data object (my suggested alternative to PESEL number) from a date of birth and sequence number, ID or PESEL number.<br>

Example for PESEL object:
```
>>> from pesel import *
>>> str(PESEL(date(2004, 5, 4), 846))
'04250408463'
>>> PESEL = PESEL(pesel="04250408463")
>>> pesel.get_date_of_birth()
datetime.date(2004, 5, 4)
>>> pesel.get_sequential_number()
846
```

Example for ID_Number object:
```
>>> from id_number import *
>>> str(ID_Number(date(2004, 5, 4), 846))
'1ll5-nir'
>>> str(ID_Number(pesel="04250408463"))
'1ll5-nir'
>>> id_number.get_date_of_birth()
datetime.date(2004, 5, 4)
>>> id_number.get_sequential_number()
846
```