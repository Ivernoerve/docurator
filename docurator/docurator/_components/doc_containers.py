"""Conatins container dataclasses to store the different documentations."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Type

import inspect


@dataclass(frozen=True)
class Docs:
    """Represents documentation information.

    Attributes:
        name (str): The name of the object.
        docstring (Optional[str]): The docstring of the object, or None if no docstring is provided.
    """ #noqa: E501
    name: str
    docstring: str|None

    def __eq__(self, other: Docs) -> bool:
        """Equality for Docs."""
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name
    
    def __hash__(self) -> str:
        """Implement hash on the name.
        
        The name of the Docs should be unique within the different scopes they are saved.
        files must be distinct within the same directory
        Functions and classes must have distinct names in the various scopes in a file.
        """ #noqa: E501
        return hash(self.name)
    

@dataclass(frozen=True, eq=False)
class ModuleDocs(Docs):
    """Represents documentation information for a module.

    Attributes:
        name (str): The name of the object.
        docstring (str|None): The docstring of the object, or None if no docstring is provided.
        contents set[Docs]: A set of documentation objects.
    """ #noqa: E501
    __contents: set[Docs] = field(default_factory=set)
    
    @property
    def contents(self) -> list[Docs]:
        """Interact with the __object attribute."""
        return self.__contents

    def contains_class(self, class_name: str) -> bool:
        """Asserts if the class supposed to be documented exists in the contents.
        
        Args:
            class_name (str): The name of the class to look for.

        Returns:
            bool: True if the class exists in contents, False otherwise.
        """
        condition_map = map(
            lambda doc: (isinstance(doc, ClassDocs)) and (doc.name == class_name),
            self.__contents
        )
        return any(condition_map)
    
    def get_class(self, class_name: str) -> ClassDocs:
        """Gets the class with the given name from the contents.
        
        Args:
            class_name (str): The name of the class to get.

        Returns:
            ClassDocs: The docs for the given class.
        """
        return filter(
            lambda doc: (isinstance(doc, ClassDocs)) and (doc.name == class_name),
            self.__contents
        ).__next__




@dataclass(frozen=True, eq=False)
class ObjectDocs(Docs):
    """Represents documentation information for an object.

    Attributes:
        docstring (Optional[str]): The docstring of the object, or None if no docstring is provided.
        name (str): The name of the object.
        qualname (str): The qualified name of the object, which includes the module and class name if applicable.
        type (str): The type of the object as a string (e.g., "function", "class").
        f_signature (Type[signature]): The function signature, if applicable.
        module (Optional[str]): The name of the module where the object is defined, or None if not applicable.
    """ #noqa: E501
    qualname: str
    type: str
    f_signature: Type[inspect.signature]

@dataclass(frozen=True, eq=False)
class ClassDocs(ObjectDocs):
    """Represents documentation information for a class, including its parents.

    Inherits from:
        Docs: The base class containing common documentation attributes.

    Attributes:
        name (str): The name of the object.
        docstring (str|None): The docstring of the object, or None if no docstring is provided.
        parents (List[object]|None): A list of parent classes of the documented class.
            None if has no parents.
        contents set[Docs]: A set of documentation objects.
    """ #noqa: E501
    parents: list[object]|None
    __contents: set[Docs] = field(default_factory=set)
    
    @property
    def contents(self) -> set[Docs]:
        """Interact with the __object attribute."""
        return self.__contents
