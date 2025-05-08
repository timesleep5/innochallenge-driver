from client.components.data_extractors.interface import IDataExtractor
from client.components.data_senders.interface import IDataSender
from client.components.data_validators.interface import IDataValidator
from client.components.sound_file_providers.interface import ISoundFileProvider
from client.components.transcriptors.interface import ITranscriptor


class IFactory:
    def create_sound_file_provider(self) -> ISoundFileProvider:
        pass

    def create_transcriptor(self) -> ITranscriptor:
        pass

    def create_data_extractor(self) -> IDataExtractor:
        pass

    def create_data_validator(self) -> IDataValidator:
        pass

    def create_data_sender(self) -> IDataSender:
        pass
