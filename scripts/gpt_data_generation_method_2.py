import openai
import random
import re
import json
import time
from informed_nlu.data_classes.initial_contradiction_types import *
from informed_nlu.utils.api_key import api_key # you need to provide your personal API key in this file
from informed_nlu.utils.openai_utils import calculate_api_call_len_and_price

# path to adjust to your system, where the repository is located
base_path = "/cluster/"

# OpenAI config
openai.api_key=api_key
model_new_types='gpt-4'
model_new_samples = "gpt-4"
max_tokens=512
temperature=1

# total iterations
iterations = 1
# number of contradiction type examples to provide in each prompt
prompt_examples = 3
# number of new contradictions to generate for each type
num_contradictions = 5

total_cost = 0
total_num_contradictions = 0
total_num_types = 0

contradiction_types = [structure, lexical, factive_embedded_verb, factive_antonym]

for i in range(iterations):
    
    for contradiction_type in contradiction_types:

        messages=[
                {"role": "system", "content": "You are an expert on semantics and linguistics, with a profound knowledge\
                in Natural Language Processing. You are especially aware of the work by Marneffe et al., classifying\
                different types of contradictions, such as contradictions arising from antonymity, negation, or numeric mismatch.\
                 To this end, a contradiction is defined as a mismatch between two statements, such that they cannot possibly both be true.\
                 It is assumed, that both statements refer to the same fact or event, even if this is not explicitly stated."},
                {"role": "user", "content": f"Please generate {num_contradictions} different contradictions based on {contradiction_type.name}.\
                    The contradictions should be original and reasonably different from each other. Both premise and hypothesis should contain at least 10 word each,\
                    and should not be too similar. Please take care that they are actually contradicting and semantically meaningful.\
                 Be creative! Format your response in the following way: 'Premise: [PREMISE], Hypothesis: [HYPOTHESIS]'. Keep to this format strictly and do not add\
                 extra text or numbers."},
                {"role": "assistant", "content": contradiction_type.description},
            ]
        for i in range(5):
            try:
                res = openai.ChatCompletion.create(
                model=model_new_samples,
                max_tokens=max_tokens,
                messages=messages,
                temperature=temperature
                )
                break
            except Exception as e:
                print(e)
                time.sleep(10)

        output = res["choices"][0]["message"]["content"]
        prompt = " ".join([m["content"] for m in messages])
        max_length, cost = calculate_api_call_len_and_price(prompt, model_new_samples, max_tokens, output_text=output)
        total_cost += cost

        print(output)
        
        processed_length = 0
        for i in range(num_contradictions):
            #substring = output[processed_length:]
            try:
                premise = re.findall("(?<=Premise:\s).*(?=\s+Hypothesis:)", output)[i]
                hypothesis = re.findall("(?<=Hypothesis:\s).*(?=\s+\d?\.?\s?Premise:\s|\Z)", output)[i]
                contradiction_type.instances.append(Contradiction(premise=premise, hypothesis=hypothesis))
                print(f"\nGenerated Contradiction of type {contradiction_type.name}:")
                print(f"Premise: {premise}")
                print(f"Hypothesis: {hypothesis}")
                total_num_contradictions += 1
            except Exception as e:
                print(f"Could not parse output {output}")
                print(e)

        time.sleep(10)


    types_to_provide = random.sample(contradiction_types, 3)
    messages=[
                    {"role": "system", "content": "You are an expert on semantics and linguistics, with a profound knowledge\
                    in Natural Language Processing. You are especially aware of the work by Marneffe et al., classifying\
                    different types of contradictions, such as contradictions arising from antonymity, negation, or numeric mismatch."},
                    {"role": "user", "content": f"Please come up with a new category of contradiction (other than\
                      {', '.join([type.name for type in contradiction_types])}). Format your output in the following way: Contradiction type name:\
                        [TYPE_NAME], Contradiction type description: [TYPE_DESCRIPTION]."},
                    {"role": "assistant", "content": " ".join([type.description for type in types_to_provide])},
                ]
    
    for i in range(5):
        try:
            res = openai.ChatCompletion.create(
            model=model_new_types,
            max_tokens=max_tokens,
            messages=messages,
            temperature=temperature,
            )
            break
        except Exception as e:
            print(e)
            time.sleep(10)

    output = res["choices"][0]["message"]["content"]
    
    prompt = " ".join([m["content"] for m in messages])
    max_length, cost = calculate_api_call_len_and_price(prompt, model_new_types, max_tokens, output_text=output)
    total_cost += cost

    try:
        name = re.search("(?<=Contradiction type name:\s).*(?=\s+Contradiction type description:)", output).group(0)
        desc = re.search("(?<=Contradiction type description: ).*", output).group(0)
        if name not in [type.name for type in contradiction_types]:
            total_num_types += 1
            contradiction_types.append(ContradictionType(name=name, description=desc, instances=[]))
            print("Generated new Contradiction Type:")
            print(f"Name: {name}")
            print(f"Description: {desc}")
        else:
            print(f"Type {name} already existing!")
    except Exception as e:
        print(f"Could not parse output {output}")
        print(e)

print(f"In total the API calls amounted to a cost of {total_cost}.")
print(f"Generated {total_num_types} new contradiction types and {total_num_contradictions} contradiction samples")

for type in contradiction_types:
    with open(f"{base_path}informed_nlu/data/generated_contradictions/{model_new_samples}/{type.name}.json", "w") as fp:
        json.dump(type.to_dict(), fp)
