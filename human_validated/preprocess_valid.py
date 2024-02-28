import os
import json
import csv

def extract_factive_sentences(html_text, label):
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
    
    premise_start = html_text.find("<b><p>")        
   
    premise_end = html_text.find(". ", premise_start + len("<b><p>"))
    hypothesis_start = premise_end
    
    if premise_start == -1 or hypothesis_start == -1:
        return None
    
    hypothesis_end = html_text.find("</p><b/>", hypothesis_start + len("."))
    
    if premise_end == -1 or hypothesis_end == -1:
        return None
    
    premise_sentences = html_text[premise_start + len("<b><p>"):premise_end].strip()
    hypothesis_sentences = html_text[hypothesis_start + len("."):hypothesis_end].strip()

    
    result = {'label': label, 'sentence1': premise_sentences, 'sentence2': hypothesis_sentences}
    return result


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

    
    result = {'label': label, 'sentence1': premise_sentences, 'sentence2': hypothesis_sentences.strip("\"")}
    return result


def read_csv_files(directory, output_dir):
    """
    Read CSV files in a directory.

    Args:
    - directory: The directory containing the CSV files.

    Returns:
    - A dictionary where keys are subject groups and values are lists of dictionaries.
      Each dictionary contains sentences following "Premise" and "Hypothesis",
      along with the corresponding annotator labels, for a specific subject group.
    """
    
    #TODO add correct path iteration
    data_by_type = []
    for type_folder in os.listdir(directory):
        type_path = os.path.join(directory, type_folder)
        type_out_path = os.path.join(output_dir, type_folder)
        
        for group_folder in  os.listdir(type_path):
            group_path = os.path.join(type_path, group_folder)
            group_out_path = os.path.join(type_out_path, group_folder)
            data_by_group = {}
            for filename in os.listdir(group_path):
                #data_by_annotator = []
                if filename.endswith(".csv"):
                    file_path = os.path.join(group_path, filename)
                    data_by_annotator = []
                    with open(file_path, "r", newline="") as file:
                        csv_reader = csv.DictReader(file)
                        for i, row in enumerate(csv_reader):
                            if i == 0:
                                mind_label = row['mindsCode']
                            else: 
                                label = row['link']
                                sentences_data = extract_sentences(row['mindsCode'], label)  
                                if sentences_data is not None:
                                    data_by_annotator.append(sentences_data)                 
                data_by_group[mind_label] = data_by_annotator  # Append the extracted sentences and labels to the existing list
                
                output_file = os.path.join(group_out_path, f"type_{type_folder}_group_{group_folder}.json")
                with open(output_file, 'w') as json_file:
                    json.dump(data_by_group, json_file, indent=4)
            data_by_type.append(data_by_group)
        #TODO: save one json per group
    return data_by_group, data_by_type

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
directory_path = "/scratch/informed_nlu/human_validated/annotated_types"
output_directory = "/scratch/informed_nlu/human_validated/types_output"

data_by_group, data_by_type = read_csv_files(directory_path, output_directory)
#save_data_as_json(data_by_group, output_directory)

#TODO: write script for defining the gold labels in two ways