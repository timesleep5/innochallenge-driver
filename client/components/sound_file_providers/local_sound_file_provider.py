from client.components.sound_file_providers.interface import ISoundFileProvider
from client.config import config


class LocalSoundFileProvider(ISoundFileProvider):
    def get_sound_file(self) -> str:
        return config.file_location
