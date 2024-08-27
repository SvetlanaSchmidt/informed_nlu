import openai
import json
from informed_nlu.data_classes.initial_contradiction_types_snli import *
from informed_nlu.utils.utils import read_prem

openai.api_key="API KEY"
model='gpt-4'
max_tokens=512 # the maximum generated tokens

temperature=1 #the diversity of the output

train_path="/shared_with_maren/contradiction_detection/data/raw/snli_data_original/tokenized_format/snli_train_pos_dep.json"
train_premises=read_prem(train_path)
#descriptions of the contradiciton types: instances of the ContradictionType class
contradiction_types = [factive_embedded_verb, factive_antonym, structure, lexical, wk]


responses=[] 
#adjust the number of premises for generation
for premise in train_premises[:50]:
    response=[]
    for contradiction_type in contradiction_types:
        res = openai.ChatCompletion.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
                {"role": "system", "content": "You are an expert on semantics and linguistics, with a profound knowledge\
                in Natural Language Processing. You are especially aware of the work by Marneffe et al., classifying\
                different types of contradictions, such as factive, structural, lexical, and world knowledge contradictions. The Premise is provided,\
                you have to create a Hypothesis of one of the contradiction types for this premise."},
                {"role": "user", "content": f"Please generate one contradictory Hypothesis for a {premise}, based on {contradiction_type.description}.\
                Format your response in the following way: {contradiction_type.name} P: [PREMISE], H: [HYPOTHESIS]."},
                {"role": "assistant", "content": contradiction_type.description},
            ]
        )

  
  