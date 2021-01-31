from typing import Dict, List
from .channel import Channel
from typing import Dict


class Instrument(object):
    def __init__(self, source_name, codename, metadata):
        self.source_name = source_name
        self.codename = codename
        self.metadata = metadata
        self.channels = {
            c_codename: Channel(
                source_name=source_name,
                instrument_name=codename,
                codename=c_codename,
                resolutions=metadata['series'][0]['avg'],
                metadata=c_metadata
            ) for c_codename, c_metadata in metadata['series'][0]['data'].items()
        }
        self.resolutions = metadata['series'][0]['avg']
        self.name = metadata['title']
        descriptions = metadata.get('descriptions', None)
        if descriptions:
            self.fullname = descriptions.get('full', None)
        else:
            self.fullname = None

    def __repr__(self) -> str:
        return f'<Instrument object: codename={self.codename}, channels={list(self.channels.keys())}>'
