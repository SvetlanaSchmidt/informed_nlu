# Informed NLU
Authors: Svetlana Schmidt, Maren Pielka

This repository contains the code that was used for the experiments in the paper "Generating Prototypes for Contradiction Detection Using Large Language Models and Linguistic Rules" (submitted to the IEEE Big Data Conference) [1].

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

## 1. Reproduce the data generation experiments
Navigate to the /scripts directory.

Method 1: 
    From informed_nlu/scripts:
    - prepare the data by running `create_datalists.py`;
    - in order to generate samples from SNLI premises with rule-based approach run `gen_simple_contradictions.py`;

Method 2:
    From informed_nlu/scripts:
    - run `scrape_WK_premises.py`to scrape the premises for the world knowledge contradiction type; 
    - run `gpt_data_generation_complex.py` for generating samples with GPT model from SNLI premises;

Method 3:
    - run `gpt_data_generation_method_3.py` in order to generate new types of contradictions with GPT model only

### Important: 
You need to add your personal OpenAI API key under ./informed_nlu/utils/api_key.py, in order to make requests to the OpenAI API.

# 2. Gold labels determination and Inter-Annotator Agreement

## Compute the agreement and define the gold labels for annotated data
From informed_nlu/human_validated/scripts/main:
    - run `define_gold_labels.py` to create the files with gold labels based on the simple majority vote    
    - `iaa_measure.py` this contains functions for computation of the pairwise percent agreement, Cohen's Kappa, Fleiss' Kappa and Krippendorff's alpha

The validated data is prepared and located at `informed_nlu/human_validated/data`:
 - `annotated_types` contains the raw and cleaned validated samples;
 - `combined_dfs`contains prepared data with determined gold labels for contradiciton types
  and for contradiciton/no contradiction classes    

# 3. Prepare prototypical data for evaluation with transformer models
To create the reduced datasets and combine them with prototypes:
    - run `prototypes_dataset_prep.py` to create combined datasets with reduced SNLI human validated prototypes, 
real-world contradictions and structural contradictions from BBC news [2]



## References:
1. 
Pielka, Maren, Svetlana Schmidt, and Rafet Sifa. 
"Generating Prototypes for Contradiction Detection Using Large Language Models and Linguistic Rules." 
2023 IEEE International Conference on Big Data (BigData). IEEE, 2023.
2. 
Freischlad, Marie-Christin et al. (n.d.). “Training on Prototypical Contradictions”. work in
progress.