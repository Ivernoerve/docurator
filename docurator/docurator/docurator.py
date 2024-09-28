"""
This module provides a utility for collecting and storing documentation information of callable objects 
using a decorator-based approach. It is designed for both development and production environments, allowing
documentation gathering to be toggled on or off.

Classes:
    Docurator: Collects documentation information for callable objects and stores them in a list.

Functions:
    decorator_factory(mode: str): Creates a decorator function to either collect documentation information 
        (in 'development' or 'doc' mode) or do nothing (in 'production' mode).

Decorators:
    document_me: A decorator created by `decorator_factory`, used to annotate callable objects and collect 
        their documentation information based on the current mode.

Usage:
    - Use the `document_me` decorator to annotate functions, methods, or other callable objects that need 
      their documentation collected.
    - `Docurator` instances will store relevant metadata such as docstrings, function signatures, names, 
      and module information.
"""
import logging
from typing import Callable, TypeVar, Any
from inspect import signature, getmodule
from doc_containers import Docs, ModuleDocs, ObjectDocs

logger = logging.getLogger(__name__)
CallableObject = TypeVar("F", bound=Callable[..., Any])


class Docurator:
    """A class for collecting documentation information for callable objects.

    Attributes:
        docs (List[Docs]): A list of documentation information collected for the callable objects.
    """
    def __init__(self):
        """Initializes an empty list to store documentation information."""
        self.__docs = {}

    @property
    def docs(self) -> dict[str, Docs]:
        return self.__docs

    def add(self, func: CallableObject) -> None:
        """Adds documentation information for a given callable object.

        Args:
            func (Callable): The callable object (e.g., function, method) for which to collect documentation.

        Raises:
            ValueError: If `func` is not a callable object.
        """
        if isinstance(func, classmethod):
            f = func.__func__
        else: 
            f = func
        
        if not callable(f):
            raise ValueError('The provided object must be callable.')
        
        module = getmodule(f)
        module_docs = self.__docs.get(module.__name__)
        if module_docs is None:
            module_docs = ModuleDocs(
                module.__name__, 
                module.__doc__
            )
            self.__docs[module.__name__] = module_docs

        doc_content = ObjectDocs(
            docstring=f.__doc__, 
            name=f.__name__,
            qualname=f.__qualname__,
            type=f.__class__.__name__,
            f_signature = signature(f),
        )
        module_docs.contents.append(doc_content)

mode = 'doc'
docurator = Docurator()


def decorator_factory(mode: str):
    if mode == 'production':
        logger.info('In production setting docurator does nothing.')
        def documentor(func: CallableObject) -> CallableObject:
            return func
    elif mode in ['document', 'doc']:
        logger.info(f'In {mode} setting docurator collects documentation.')
        def documentor(func: CallableObject) -> CallableObject:
            docurator.add(func)
            return func
    else:
        raise ValueError(f'Mode {mode} was not recognized.')

    return documentor


document_me = decorator_factory(mode)
