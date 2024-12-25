import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("Ashikan/dut-recipe-generator")
model = AutoModelForCausalLM.from_pretrained("Ashikan/dut-recipe-generator")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

input_ingredients = ["cheese", "onion", "chicken"]

input_text = '{"prompt": ' + json.dumps(input_ingredients)

output = pipe(input_text, max_length=1024, temperature=0.2, do_sample=True, truncation=True)[0]["generated_text"]

#JSON formatted output with "title", "ingredients" and "method" nodes available
print(output)
