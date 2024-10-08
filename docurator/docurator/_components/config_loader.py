"""The module contains classes for loading default and custom configs."""
import yaml
from pathlib import Path
from copy import deepcopy

from docurator._defaults.md_templates import DEFAULT_TEMPLATES
from docurator._defaults.settings import DEFAULT_CONFIG

class  _TemplateCommonUtilities:
    """Utility class containing common utilities that can be used for config managment."""
    @staticmethod
    def load_yaml(path: str|Path) -> dict:
        """Method to load a yaml.
        
        Args: 
            path (str|Path): The path pointing to the yaml to load.
        
        Returns:
            dict: A dictionary containing the contents of the yaml.
        """
        with open(path) as file:
            f = yaml.safe_load(file)
        return f

    @staticmethod
    def test_file_exists(path: str|Path) -> None:
        """Method to test if a path points at an existing file.
        
        Args:
            path (str|Path): The path to check.

        Raises:
            FileNotFoundError: If the path points to a directory that does not exist,
                or if the path points to a directory.
        """
        if type(path) is str:
            path = Path(Path)
        if not (path.exists() and path.is_file()):
            raise FileNotFoundError(f'The file at the path: "{path}" does not exist.')
    
    @staticmethod
    def test_directory_exists(path: str|Path) -> None:
        """Method to test if a path points at an existing directory.
        
        Args:
            path (str|Path): The path to check.

        Raises:
            NotADirectoryError: If the path points to a directory that does not exist,
                or if the path points to a file.
        """
        if type(path) is str:
            path = Path(Path)
        if not (path.exists() and path.is_dir()):
            raise NotADirectoryError(f'The path: "{path}" Does not point to a directory.')
    
    
    @staticmethod
    def test_files_are_valid_format(path: str|Path, valid_formats: list[str]) -> None:
        """Method to test if a file or directory of files has valid file formats.
        
        Args:
            path (str|Path): The path to check.

        Raises:
            ValueError: If the given file or any files in the directory has an invalid
                file format.
        """
        if type(path) is str:
            path = Path(Path)

        error_found = False
        if path.is_file() and path.suffix not in valid_formats:
            error_found = True
            err_str = f'The file at path {path} has an invalid format.'
        elif any(p.suffix not in valid_formats for p in path.iterdir()):
            error_found = True
            err_str = f'Files in the given directory {path} has non valid formats.'

        if error_found:
            raise ValueError(f'{err_str} Valid formats are {valid_formats}')

class TemplateSetBuilder:
    """Class for building the set of templates that are used for documenting."""
    def __init__(self, path: str|Path) -> None:
        """Init function for the template set builder.
        
        Args:
            path (str|Path): A path pointing to the custom templates if any.
                Defaults to None in which there is no custom templates.
        """
        self.__valid_formats = ['.md']
        self.utilities = _TemplateCommonUtilities()

        if path is None:
            self.config_path = None
            return
        path = Path(path)
        self.utilities.test_directory_exists(path)
        self.utilities.test_files_are_valid_format(path, self.__valid_formats)
        self.config_path = path

    def get(self) -> dict[str, Path]:
        """Method to get the set of templates for the docurator.
        
        Returns:
            dict[str, Path]: A dictionary of template strings.
        
        Raises:
            KeyError: If any template file has a name not corresponding 
                to an existing template.
        """
        if self.config_path is None:
            return DEFAULT_TEMPLATES
        
        output_templates = deepcopy(DEFAULT_TEMPLATES)
        not_in_default = []
        for file in self.config_path.iterdir():
            filename = file.stem
            if output_templates.get(filename) is None:
                not_in_default.append(file.name)
                continue
            template = self.utilities.load_yaml(file)
            output_templates[filename] = template

        if len(not_in_default) > 0:
            raise KeyError(
                f'The given custom template files: {not_in_default}'
                ' are not valid filenames.'
            )
        return output_templates


class ConfigBuilder:
    """Class for building the config to be used by the docurator."""
    def __init__(self, path: str|None = None):
        """Init function for the config builder.
        
        Args:
            path (str|Path): A path pointing to the custom config if any.
                Defaults to None in which there is no custom config.
        """
        self.__valid_formats = ['.yaml', '.yml']
        self.utilities = _TemplateCommonUtilities()
        
        if path is None:
            self.config_path = None
            return
        path = Path(path)
        self.utilities.test_file_exists(path)
        self.utilities.test_files_are_valid_format(path, self.__valid_formats)
        self.config_path = path

    def get(self) -> dict:
        """Method to get the config for the docurator.
        
        Returns:
            dict[str, Path]: A dictionary of config variables.
        
        Raises:
            KeyError: If any key in the given config file has an invalid name.
        """
        if self.config_path is None:
            return DEFAULT_CONFIG
        
        custom_config = self.__load_yaml(self.config_path)
        output_config = deepcopy(DEFAULT_CONFIG)
        not_in_default = []
        for setting, value in custom_config.items():
            if output_config.get(setting) is None:
                not_in_default.append(setting)
                continue
            output_config[setting] = value

        if len(not_in_default) > 0:
            raise KeyError(
                f'The given settings in the custom config: {not_in_default}'
                ' are not valid settings in the config.'
            )
        return output_config
