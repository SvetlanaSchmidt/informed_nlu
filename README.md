# Informed NLU
Authors: Svetlana Schmidt, Maren Pielka

This repository contains the code that was used for the experiments in the paper "Generating Prototypes for Contradiction Detection Using Large Language Models and Linguistic Rules" (submitted to the IEEE Big Data Conference) [1] and the research project [4]. 
The datasets of [simple prototypical contradictions](https://huggingface.co/datasets/SvetaPetrush/prototypical_contradictions_ant_neg_num) and human validated [complex prototypical contradictions](https://huggingface.co/datasets/SvetaPetrush/prototypical_contradictions) are available at Hugging Face Datasets.

## Install the repository
1. Install Python on your system and create a new virtual environment (recommended: Python >= 3.8.0):
```bash
$ conda create -n informed_nlu python==3.8
```
2. Navigate to the repository folder:
```bash
$ cd informed_nlu
```
3. Install the package:
```bash
$ pip install -e .
```

## Reproduce the experiments
Navigate to the /scripts directory.

Method 1: 
    - prepare the data by running `create_datalists.py`;
    - in order to generate samples from SNLI premises with rule-based approach run `gen_contr.py`;

Method 2:
    - run `gpt_data_generation_snli.py` for generating samples with GPT model from SNLI premises;

Method 3:
    - run `gpt_data_generation_method_3.py` in order to generate new types of contradictions with GPT model only

### Important: You need to add your personal OpenAI API key under ./informed_nlu/utils/api_key.py, in order to make requests to the OpenAI API.

