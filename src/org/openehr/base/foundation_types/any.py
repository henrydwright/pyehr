from abc import ABC, abstractmethod

class AnyClass(ABC):
    """
    Defines a bare minimum of operations.
    """

    def __init__(self, **kwargs):
        super(ABC).__init__(**kwargs)

    @abstractmethod
    def is_equal(self, other) -> bool:
        """
        Returns `True` if this and other are equal in value; typically
         defined in descendants
        """
        pass