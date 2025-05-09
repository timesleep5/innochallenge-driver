from client.components.data_extractors.interface import IDataExtractor
from client.components.data_extractors.data_extractor import DataExtractor
from client.components.data_senders.interface import IDataSender
from client.components.data_validators.data_validator import DataValidator
from client.components.data_validators.interface import IDataValidator
from client.components.sound_file_providers.interface import ISoundFileProvider
from client.components.data_senders.data_sender import DataSender
from client.components.sound_file_providers.local_sound_file_provider import LocalSoundFileProvider
from client.components.transcriptors.transcriptor import Transcriptor
from client.components.transcriptors.interface import ITranscriptor
from client.factory.interface import IFactory


class PitchFactory(IFactory):
    def create_sound_file_provider(self) -> ISoundFileProvider:
        return LocalSoundFileProvider()

    def create_transcriptor(self) -> ITranscriptor:
        transcription_service_url = "http://127.0.0.1:8000/v1/speech/transcribe"
        return Transcriptor(transcription_service_url)

    def create_data_extractor(self) -> IDataExtractor:
        llm_service_url = "http://127.0.0.1:8000/v1/llm/process"
        return DataExtractor(llm_service_url)

    def create_data_validator(self) -> IDataValidator:
        return DataValidator()

    def create_data_sender(self) -> IDataSender:
        return DataSender()