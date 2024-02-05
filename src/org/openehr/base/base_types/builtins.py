from datetime import date, time, datetime, timezone
import locale

from org.openehr.base.foundation_types.terminology import TerminologyCode

class Env():
    """Class representing the real-world environment, providing 
    basic information like current time, date, etc."""

    def current_date() -> date:
        """Return today’s date in the current locale."""
        return datetime.now().date()
    
    def current_time() -> time:
        """Return current time in the current locale."""
        return datetime.now().time()
    
    def current_date_time() -> datetime:
        """Return current date/time in the current locale."""
        return datetime.now()
    
    def current_time_zone() -> timezone:
        """Return the timezone of the current locale."""
        return datetime.now().astimezone().tzinfo
    
class Locale():
    """Class representing current Locale."""

    def primary_language() -> TerminologyCode:
        """Primary language of the current locale."""
        tc = TerminologyCode()
        tc.code_string = locale.getlocale()[0]
        tc.terminology_id = "RFC-1766"
        return tc
    
print(Locale.primary_language())

