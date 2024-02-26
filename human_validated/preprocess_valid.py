import os
import json

def combine_data_from_folders(input_directory, output_directory):
    """
    Combine data from folders and save the combined data for each sentence pair.

    Args:
    - input_directory: Path to the input directory containing folders 1 to 8.
    - output_directory: Path to the output directory where combined data will be saved.
    """
    for folder in os.listdir(input_directory):
        folder_path = os.path.join(input_directory, folder)
        if os.path.isdir(folder_path):
            combined_data = {}
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                for entry in data:
                    sentence_pair_key = (entry['sentence1'], entry['sentence2'])
                    if sentence_pair_key not in combined_data:
                        combined_data[sentence_pair_key] = {
                            'sentence1': entry['sentence1'],
                            'sentence2': entry['sentence2'],
                            'annotator1': [],
                            'annotator2': [],
                            'annotator3': []
                        }
                    combined_data[sentence_pair_key]['annotator1'].append(entry['annotator1'])
                    combined_data[sentence_pair_key]['annotator2'].append(entry['annotator2'])
                    combined_data[sentence_pair_key]['annotator3'].append(entry['annotator3'])

            # Save combined data for each sentence pair
            output_file_path = os.path.join(output_directory, f"group_{folder}.json")
            with open(output_file_path, 'w') as output_file:
                json.dump(list(combined_data.values()), output_file, indent=4)

# Example usage:
input_directory = "input_directory"
output_directory = "output_directory"
combine_data_from_folders(input_directory, output_directory)
