from typing import Dict

from .instrument import Instrument


class Source(object):
    def __init__(self, codename: str, metadata: Dict):
        self.codename = codename
        self.metadata = metadata
        self.instruments = {
            i_codename: Instrument(
                source_name=codename,
                codename=i_codename,
                metadata=i_metadata
            ) for i_codename, i_metadata in metadata['instruments'].items()
        }
        descriptions = metadata.get('descriptions', None)
        if descriptions:
            self.fullname = descriptions.get('full', None)
        else:
            self.fullname = None
        self.tags = metadata['tags']

    def __repr__(self) -> str:
        return f'<Source object: codename={self.codename}, instruments={list(self.instruments.keys())}>'
