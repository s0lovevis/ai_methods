from transformers import GPT2Tokenizer, GPT2LMHeadModel

class ruGPTModel:
    def __init__(self, model_name_or_path):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_name_or_path)

    def generate(self, text,
                 do_sample=True, max_length=60, repetition_penalty=5.0,
                 top_k=5, top_p=0.95, temperature=0.8,
                 num_beams=10, no_repeat_ngram_size=3):
        
        input_ids = self.tokenizer.encode(text, return_tensors="pt")

        out = self.model.generate(
            input_ids,
            max_length=max_length,
            repetition_penalty=repetition_penalty,
            do_sample=do_sample,
            top_k=top_k, top_p=top_p, temperature=temperature,
            num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size
        )

        return list(map(self.tokenizer.decode, out))[0]