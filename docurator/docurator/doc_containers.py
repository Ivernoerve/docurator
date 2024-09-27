"""Conatins container dataclasses to store the different documentations. """

from dataclasses import dataclass
from typing import Type

from inspect import signature


@dataclass(frozen=True)
class Docs:
    """Represents documentation information for an object.

    Attributes:
        docstring (Optional[str]): The docstring of the object, or None if no docstring is provided.
        name (str): The name of the object.
        qualname (str): The qualified name of the object, which includes the module and class name if applicable.
        type (str): The type of the object as a string (e.g., "function", "class").
        f_signature (Type[signature]): The function signature, if applicable.
        module (Optional[str]): The name of the module where the object is defined, or None if not applicable.
    """
    docstring: str|None
    name: str
    qualname: str
    type: str
    f_signature: Type[signature]
    module: str|None = None

class ClassDocs(Docs):
    """Represents documentation information for a class, including its parents.

    Inherits from:
        Docs: The base class containing common documentation attributes.

    Attributes:
        parents (List[object]): A list of parent classes of the documented class.
    """
    parents: list[object]

