from requests import HTTPError

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
    print(f"Sound file path: {sound_file_path}")
    transcribed_text = transcriptor.transcribe(sound_file_path)
    print(f"Transcribed text: {transcribed_text}")
    extracted_data = data_extractor.extract_data(transcribed_text)
    print(f"Extracted data: {extracted_data}")
    is_valid = data_validator.validate_data(extracted_data)
    if is_valid:
        print("Data is valid.")
        try:
            data_sender.send_data(extracted_data)
            print("Data sent successfully.")
        except HTTPError as e:
            print(f"Failed to send data: {e}")
            exit(1)
    else:
        print("Data validation failed.")
        exit(1)
