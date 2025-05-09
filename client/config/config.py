import os

def find_file(relative_path):
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), relative_path)
    )
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Die angegebene Datei wurde nicht gefunden: {file_path}")
    return file_path

file_location = find_file("../../data/bad_test_english/iamdriverp5.wav")

backend_url = 'https://optimaloptimizer.thankfulbeach-22a876ac.westus2.azurecontainerapps.io/api/v1'
backend_truck_drivers_url = f'{backend_url}/truck-drivers'
backend_trailers_url = f'{backend_url}/trailers'
backend_trucks_url = f'{backend_url}/trucks'
