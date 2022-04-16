class Channel(object):
    def __init__(self, source_name, instrument_name, codename, resolutions, metadata):
        self.source_name = source_name
        self.instrument_name = instrument_name
        self.codename = codename
        self.resolutions = resolutions
        self.metadata = metadata
        self.name = metadata['name']
        descriptions = metadata.get('descriptions', None)
        if descriptions:
            self.fullname = descriptions.get('full', None)
        self.tags = metadata['tags']
        unit_description = metadata.get('unit', None)
        if unit_description:
            self.unit = unit_description.get('plain', None)
        else:
            self.unit = None

    def __str__(self) -> str:
        return self.codename

    def __repr__(self) -> str:
        return f'<Channel object: codename={self.codename}, unit={self.unit}>'

    def stream_subscription_info(self):
        return {
            'channel_id': '{s}.{i}.{c}'.format(
                s=self.source_name,
                i=self.instrument_name,
                c=self.codename
            ),
            'resolution': self.resolutions[0]
        }
