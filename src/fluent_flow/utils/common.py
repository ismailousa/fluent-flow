import os
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
import yaml
from ensure import ensure_annotations

from fluent_flow import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        config_path = Path(__file__).resolve().parent.parent.parent.parent / path_to_yaml
        with open(config_path, "r") as file:
            content = yaml.safe_load(file)
            logger.info(f"Read the YAML file: {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"Error reading the YAML file: {path_to_yaml}")
    except Exception as e:
        raise Exception(f"Error reading the YAML file: {path_to_yaml} \n {str(e)}")


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")
