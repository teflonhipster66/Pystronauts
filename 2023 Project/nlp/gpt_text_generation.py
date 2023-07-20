from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from transformers import pipeline




def gpt2_model(text):

    generator = pipeline("text-generation", model = "gpt2")

    output = generator(text, max_length = 100, num_return_sequences=1)
    output = output[0]
    return output["generated_text"]





