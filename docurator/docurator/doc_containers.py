"""Conatins container dataclasses to store the different documentations. """

from dataclasses import dataclass, field
from typing import Type

import inspect


@dataclass(frozen=True)
class Docs:
    """Represents documentation information.

    Attributes:
        name (str): The name of the object.
        docstring (Optional[str]): The docstring of the object, or None if no docstring is provided.
    """
    name: str
    docstring: str|None
    

@dataclass(frozen=True)
class ModuleDocs:
    """Represents documentation information for a module.

    Attributes:
        name (str): The name of the object.
        docstring (str|None): The docstring of the object, or None if no docstring is provided.
        contents list[Docs]: A list of documentation objects.
    """
    name: str
    docstring: str|None
    __contents: list[Docs] = field(default_factory=list)
    
    @property
    def contents(self) -> list[Docs]:
        """Interact with the __object attribute"""
        return self.__contents


@dataclass(frozen=True)
class ObjectDocs(Docs):
    """Represents documentation information for an object.

    Attributes:
        docstring (Optional[str]): The docstring of the object, or None if no docstring is provided.
        name (str): The name of the object.
        qualname (str): The qualified name of the object, which includes the module and class name if applicable.
        type (str): The type of the object as a string (e.g., "function", "class").
        f_signature (Type[signature]): The function signature, if applicable.
        module (Optional[str]): The name of the module where the object is defined, or None if not applicable.
    """
    qualname: str
    type: str
    f_signature: Type[inspect.signature]


class ClassDocs(ObjectDocs):
    """Represents documentation information for a class, including its parents.

    Inherits from:
        Docs: The base class containing common documentation attributes.

    Attributes:
        name (str): The name of the object.
        docstring (str|None): The docstring of the object, or None if no docstring is provided.
        parents (List[object]): A list of parent classes of the documented class.
        contents list[Docs]: A list of documentation objects.
    """
    parents: list[object]
    __contents: list[Docs] = field(default_factory=list)
    
    @property
    def contents(self) -> list[Docs]:
        """Interact with the __object attribute"""
        return self.__contents

