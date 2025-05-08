from client.factory.interface import IFactory
from client.factory.pitch_factory import PitchFactory

if __name__ == "__main__":
    process_factory: IFactory = PitchFactory()
    sound_file_provider = process_factory.create_sound_file_provider()
    transcriptor = process_factory.create_transcriptor()
    data_extractor = process_factory.create_data_extractor()
    data_validator = process_factory.create_data_validator()
    data_sender = process_factory.create_data_sender()

    sound_file_path = sound_file_provider.get_sound_file()
    transcribed_text = transcriptor.transcribe(sound_file_path)
    extracted_data = data_extractor.extract_data(transcribed_text)
    is_valid = data_validator.validate_data(extracted_data)
    if is_valid:
        data_sender.send_data(extracted_data)
        print("Data sent successfully.")
    else:
        print("Data validation failed.")
        exit(1)
