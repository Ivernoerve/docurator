"""Contains the docurator factory, and storing class.

This module provides a utility for collecting and storing documentation information of callable objects.
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
""" # noqa: E501

import logging
from typing import Callable, TypeVar, Any
import inspect
from docurator._components.doc_containers import Docs, ModuleDocs, ObjectDocs, ClassDocs

logger = logging.getLogger(__name__)
CallableObject = TypeVar("F", bound=Callable[..., Any])


class Docurator:
    """A class for collecting documentation information for callable objects.

    Attributes:
        docs (List[Docs]): A list of documentation information collected for the callable objects.
    """ #noqa E501
    def __init__(self) -> None:
        """Initializes an empty list to store documentation information."""
        self.__module_docs = {}

        # Due to class method wrappers being initialized prior
        # to the class wrapper, this stores the methods to be appended
        # to the calss at a later time.
        self.__class_method_cache = {}

    @property
    def docs(self) -> dict[str, Docs]:
        """Get the dictionary containing the fetched documentations."""
        return self.__module_docs

    def add(self, func: CallableObject) -> None:
        """Adds documentation information for a given callable object.

        Args:
            func (Callable): The callable object (e.g., function, method) for which to collect documentation.

        Raises:
            ValueError: If `func` is not a callable object.
        """ #noqa: E501
        if isinstance(func, classmethod):
            f = func.__func__
        else: 
            f = func

        if not callable(f):
            raise ValueError('The provided object must be callable.')
        
        module = inspect.getmodule(f)
        module_name = module.__name__
        module_docs = self.__module_docs.get(module_name)
        if module_docs is None:
            module_docs = ModuleDocs(
                module_name, 
                module.__doc__
            )
            self.__module_docs[module_name] = module_docs

        shared_content = {
            'docstring':f.__doc__, 
            'name':f.__name__,
            'qualname':f.__qualname__,
            'type':f.__class__.__name__,
            'f_signature': inspect.signature(f),
        }
        if inspect.isclass(f):
            doc_content = self.__create_class_doc(shared_content, f)
            # Fetch methods from method cache if exists.
            cached_class_methods = self.__pop_from_method_cache(
                module_name, doc_content.qualname
            )
            doc_content.contents.update(cached_class_methods)
        else:
            doc_content = ObjectDocs(**shared_content)


        if self.__is_method(f):
            class_name = self.__create_class_belonging_key(doc_content)
            if module_docs.contains_class(class_name):
                module_docs.get_class(class_name).contents.add(doc_content)
            else:
                self.__add_to_method_cache(module_name, doc_content)
            return
        module_docs.contents.add(doc_content)


    @staticmethod
    def __create_class_doc(base_content: dict, class_: object) -> ClassDocs:
        parents = [obj for obj in class_.__bases__ if obj is not object]
        base_content['parents'] = parents or None
        return ClassDocs(**base_content)

    def __add_to_method_cache(self, module_name: str, doc: ObjectDocs) -> None:
        method_path = self.__create_class_belonging_key(doc)
        key = f'{module_name}.{method_path}'
        cache = self.__class_method_cache.get(key)
        if cache is None:
            cache = set()
            self.__class_method_cache[key] = cache
        cache.add(doc)

    def __pop_from_method_cache(self, module_name: str, class_qualname: str) -> list[Docs]: #noqa E501
        key = f'{module_name}.{class_qualname}'
        if self.__class_method_cache.get(key) is not None:
            methods = self.__class_method_cache.pop(key)
        else:
            methods = set()
        return methods
    
        
    @staticmethod
    def __is_method(func: Callable) -> bool:
        return len(func.__qualname__.split('.')) > 1
    
    @staticmethod
    def __create_class_belonging_key(doc: ObjectDocs) -> str:
        return '.'.join(doc.qualname.split('.')[:-1])



mode = 'doc'
docurator = Docurator()



def decorator_factory(mode: str) -> Callable:
    """Factory function to create a decorator based on the specified mode.

    The function returns a decorator depending on the mode.
    For a production mode the decorater simply returns the function
    In document mode the decorator passes the function to the 
    docurator for retrieving the documentation for the class. 

    Args:
        mode: A string indicating the mode of the decorator. 
              Possible values are 'production', 'document', or 'doc'.

    Returns:
        A decorator function.

    Raises:
        ValueError: If the provided mode is not recognized.
    """
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
