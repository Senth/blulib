import configparser
from pathlib import Path
from shutil import copy
from site import getuserbase
from typing import Any


class ConfigParserHelper:
    """Helper methods for parsing configurations"""

    @staticmethod
    def _set_str(args: Any, section: configparser.SectionProxy, *varnames: str) -> None:
        for varname in varnames:
            default = getattr(args, varname)
            value = section.get(varname, fallback=default)
            setattr(args, varname, value)

    @staticmethod
    def _set_str_list(args: Any, section: configparser.SectionProxy, *varnames: str) -> None:
        for varname in varnames:
            values = getattr(args, varname)
            value = section.get(varname, fallback="")
            if value != "":
                values = value.split("\n")
            setattr(args, varname, values)

    @staticmethod
    def copy_example_if_conf_not_exists(app_name: str) -> None:
        """If there is no configuration, copy the example to the configuration"""
        conf_path = Path.home().joinpath(f".{app_name}.cfg")

        if conf_path.exists():
            return

        # Copy file from config location to home
        example_name = f"{app_name}-example.cfg"
        example_path = Path(getuserbase()).joinpath("config", example_name)

        if not example_path.exists():
            return

        copy(example_path, conf_path)
