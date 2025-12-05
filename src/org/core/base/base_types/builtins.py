from datetime import date, time, datetime, timezone
import locale

from org.core.base.foundation_types.terminology import TerminologyCode
from org.core.base.foundation_types.time import ISODate, ISOTime, ISODateTime, ISOTimeZone

class Env():
    """Class representing the real-world environment, providing 
    basic information like current time, date, etc."""

    def current_date() -> ISODate:
        """Return today’s date in the current locale."""
        return ISODate(datetime.now().date().isoformat())
    
    def current_time() -> ISOTime:
        """Return current time in the current locale."""
        return ISOTime(datetime.now().time().isoformat())
    
    def current_date_time() -> ISODateTime:
        """Return current date/time in the current locale."""
        return ISODateTime(datetime.now().isoformat())
    
    def current_time_zone() -> ISOTimeZone:
        """Return the timezone of the current locale."""
        return ISODateTime(datetime.now().astimezone().isoformat()).timezone()
    
class Locale():
    """Class representing current Locale."""

    def primary_language() -> TerminologyCode:
        """Primary language of the current locale."""
        tc = TerminologyCode("ISO639-1", locale.getlocale()[0][:2])
        return tc
