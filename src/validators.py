import re

from molten import Field, FieldValidationError
from molten.validation.field import _T

date_format = (
    r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
    r"[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})"
    r"(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?"
    r"(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$"
)


class DateValidator:
    """
    Date validator for pattern 2008-09-15T13:30:00+03:00
    """

    def validate(self, field: Field[_T], value: str):

        if not re.match(date_format, value):
            raise FieldValidationError(f"must match pattern 2008-09-15T13:30:00+03:00")

        return value
