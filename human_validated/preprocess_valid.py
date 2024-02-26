import os
import json
import csv


def extract_sentences(html_text, label):
    """
    Extract sentences following the words "Premise" and "Hypothesis" from HTML text.

    Args:
    - html_text: HTML text containing the sentences.
    - labels: List of annotator labels for the data point.

    Returns:
    - A list of dictionaries containing sentences following "Premise" and "Hypothesis",
      along with the corresponding annotator labels.
    """
    if html_text is None:
        return None
    
    premise_start = html_text.find("Premise:")
    hypothesis_start = html_text.find("Hypothesis:")
    
    if premise_start == -1 or hypothesis_start == -1:
        return None
    
    premise_end = html_text.find("Hypothesis:", premise_start + len("Premise:"))
    hypothesis_end = html_text.find("</p>", hypothesis_start + len("Hypothesis:"))
    
    if premise_end == -1 or hypothesis_end == -1:
        return None
    
    premise_sentences = html_text[premise_start + len("Premise:"):premise_end].strip()
    hypothesis_sentences = html_text[hypothesis_start + len("Hypothesis:"):hypothesis_end].strip()

    
    result = {'label': label, 'sentence1': premise_sentences, 'sentence2': hypothesis_sentences}
    return result


def read_csv_files(directory):
    """
    Read CSV files in a directory.

    Args:
    - directory: The directory containing the CSV files.

    Returns:
    - A dictionary where keys are subject groups and values are lists of dictionaries.
      Each dictionary contains sentences following "Premise" and "Hypothesis",
      along with the corresponding annotator labels, for a specific subject group.
    """
    data_by_group = {}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", newline="") as file:
                csv_reader = csv.DictReader(file)
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        mind_label = row['mindsCode']
                    else: 
                        label = row['link']
                        sentences_data = extract_sentences(row['mindsCode'], label)  
                        if sentences_data is not None:
                    data_by_group[mind_label] = sentences_data  # Append the extracted sentences and labels to the existing list
    return data_by_group

def save_data_as_json(data_by_group, output_directory):
    """
    Save data organized by subject group as JSON files.

    Args:
    - data_by_group: A dictionary where keys are subject groups and values are lists of dictionaries.
      Each dictionary contains sentences following "Premise" and "Hypothesis",
      along with the corresponding annotator labels, for a specific subject group.
    - output_directory: The directory where JSON files will be saved.
    """
    for subject_group, data in data_by_group.items():
        output_file = os.path.join(output_directory, f"subject_group_{subject_group}.json")
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)

# Example usage:
directory_path = "/scratch/informed_nlu/human_validated/annotated_types/lexical/1"
output_directory = "/scratch/informed_nlu/human_validated/types_output"

data_by_group = read_csv_files(directory_path)
#save_data_as_json(data_by_group, output_directory)
