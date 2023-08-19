import argparse
import os.path
import logging
import yaml
from dataclasses import dataclass

logger = logging.getLogger(f'log.{__name__}')
protoblocks = []


@dataclass(slots=True)
class Context:
    """Program context class."""

    first_path: str
    second_path: str
    first_path_to_workflow: str
    second_path_to_workflow: str

    def __init__(self):
        args = self._get_args()
        self.first_path = os.path.abspath(args.first_path)
        self.second_path = os.path.abspath(args.second_path)
        self.get_paths_to_workflow()

    def get_paths_to_workflow(self):
        if os.path.isdir(self.first_path):
            self.first_path_to_workflow = os.path.join(self.first_path, '.p7', 'workflow.json')
        else:
            logger.debug(self.first_path)
            self.first_path_to_workflow = self.first_path
        if os.path.isdir(self.second_path):
            self.second_path_to_workflow = os.path.join(self.second_path, '.p7', 'workflow.json')
        else:
            logger.debug(self.second_path)
            self.second_path_to_workflow = self.second_path

    @staticmethod
    def _get_args():
        """Getting arguments from the console."""
        parser = argparse.ArgumentParser(description='Add path to workflow directories.')
        parser.add_argument('first_path', type=str, help='Path to first directory')
        parser.add_argument('second_path', type=str, help='Path to second directory')
        parser.add_argument("-l", "--log", help="Write log into log.log", action="store_true")

        if parser.parse_args().log:
            logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
                                datefmt='%m-%d %H:%M', filename='./log.log', filemode='w')

        return parser.parse_args()

    def load_protoblocks(self):
        """Loads protoblock names."""

        protoblocks.extend([self._get_protoblocks(self.first_path), self._get_protoblocks(self.second_path)])

    @staticmethod
    def _get_protoblocks(path_of_directory: str) -> dict:
        """Opens manifest.yaml about every protoblock from the directory and returns a dict(version_id: name)."""

        dict_names = {}

        if os.path.isdir(path_of_directory):
            path = os.path.join(path_of_directory, '.p7',  'protoblocks')
        else:
            path = os.path.join(os.path.dirname(path_of_directory), 'protoblocks')

        if os.path.exists(path):
            list_of_protoblock_paths = [os.path.join(path, id_version) for id_version in os.listdir(path=path)
                                        if os.path.isdir(os.path.join(path, id_version))]

            for path in list_of_protoblock_paths:
                path = os.path.abspath(path)
                id_version = os.path.basename(path)
                path = os.path.join(path, 'manifest.yaml')

                try:
                    with open(path, 'r', encoding='utf-8') as fh:
                        manifest = yaml.load(fh, Loader=yaml.FullLoader)
                    dict_names[id_version] = manifest['name']['']

                except FileNotFoundError as ex:
                    logger.warning(ex)
        else:
            logger.warning("It is not possible to find protoblocks on the specified path.")

        return dict_names
