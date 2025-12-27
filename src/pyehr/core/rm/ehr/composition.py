from pyehr.core.base.foundation_types.any import AnyClass

class Composition(AnyClass):
    
    def is_persistent(self) -> bool:
        """True if category is 431|persistent|, False otherwise. Useful for 
        finding Compositions in an EHR which are guaranteed to be of interest 
        to most users."""
        pass
