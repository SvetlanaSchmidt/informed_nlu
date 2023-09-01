import openai
from informed_nlu.utils.openai_utils import calculate_api_call_len_and_price
from informed_nlu.utils.api_key import api_key

import tqdm
import json
import time
import re

openai.api_key=api_key
model = "gpt-3.5-turbo"

"""messages=[
                {"role": "system", "content": "You are an expert in professional communication,\
                specifically related to the finance sector."},
                {"role": "user", "content": f"Please generate a professional e-mail that an auditor could receive.\
                Also classify the mail with respect to the internal service it belongs to.\
                 Possible categories could be: HC, risk, legal, other. Format your answer as follows:\
                 E-MAIL: [E-MAIL-TEXT], CATEGORY: [CATEGORY].\
                 Please adhere to this format strictly. The output should end with the category, and there should be\
                 no additional text after that. The category should be one of 'HC', 'Risk', 'Legal' or 'Other'.\
                 Please do only use those exact terms."},
            ]"""
"""messages = [{"role": "system", "content": "Du bist ein Experte in beruflicher Kommunkation,\
                speziell bezogen auf den Finanzsketor."},
                {"role": "user", "content": f"Bitte generiere eine professionelle E-Mail, die ein Wirtschaftsprüfer erhalten könnte.\
                Klassifiziere die Mail außerdem dahingehend, zu welchem internen Service sie gehört.\
                 Mögliche Kategorien sind: HC, risk, legal, other. Formatiere deine Antwort folgendermaßen:\
                 E-MAIL: [E-MAIL-TEXT], CATEGORY: [KATEGORIE].\
                 Bitte halte dich strikt an dieses Format. Der Output sollte mit der Kategorie enden, und danach\
                 sollte kein weiterer Text folgen. Die Kategorie sollte eine von folgenden sein: 'HC', 'Risk', 'Legal' oder 'Other'.\
                 Bitte benutze nur diese exakten Begriffe."},]"""

# 6 Prompts: DE/EN, 3 Label, 400 Samples pro Prompt

total_cost = 0
generated_samples = []

for int_service in ["Human Capital", "Risk", "Legal"]:
    for lang in ["DE", "EN"]:
        print(int_service)
        print(lang)
        if lang == "EN":
            messages = [
                        {"role": "system", "content": "You are an expert in professional communication,\
                        specifically related to the finance sector."},
                        {"role": "user", "content": f"Please write a professional e-mail that an auditing firm could receive and that it would manually forward to its internal service\
                         line '{int_service}'. Write the e-mail so that the assignment to {int_service} is not too obvious, e.g. do not mention {int_service} explicitly in your formulations."},
                    ]
        else:
            messages = [
                        {"role": "system", "content": "You are an expert in professional communication,\
                        specifically related to the finance sector."},
                        {"role": "user", "content": f"Please write a professional e-mail that an auditing firm could receive and that it would manually forward to its internal service\
                         line '{int_service}'. Write the e-mail so that the assignment to {int_service} is not too obvious, e.g. do not mention {int_service} explicitly in your formulations.\
                            Please write the answer in German."},
                    ]
        for i in tqdm.tqdm(range(400)):
            for j in range(5):
                try:
                    res = openai.ChatCompletion.create(
                                model=model,
                                max_tokens=256,
                                messages=messages,
                                temperature=0.7
                                )
                    break
                except Exception as e:
                    print(e)
                    time.sleep(10)

            time.sleep(5)
                    
            output = res["choices"][0]["message"]["content"]
            #print(int_service)
            #print(output)
            #print("#############################################################################################")
            prompt = " ".join([m["content"] for m in messages])
            max_length, cost = calculate_api_call_len_and_price(prompt, model, 256, output_text=output)
            total_cost += cost
            
            generated_samples.append({"text": output, "category": int_service})

            json.dump(generated_samples, open("/cluster/pwc_ali/email_generation/all_samples_gpt-35_new.json", "w"), ensure_ascii=False)
            if (i % 50) == 0:
                print(int_service)
                print(output)
                print(f"Cost so far: {total_cost}")

            #print("-------------------------------------------------------------------------------------")
        
print(f"The total cost amounted to {total_cost}")
print(f"Generated {len(generated_samples)} samples")
