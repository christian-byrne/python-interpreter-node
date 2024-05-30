from textgenrnn import textgenrnn

# Initialize textgenrnn model
textgen = textgenrnn.TextgenRnn()

def generate_prompt(seed_text, max_length=50):
    prompts = textgen.generate(return_as_list=True, prefix=seed_text, max_gen_length=max_length)
    return prompts[0]

# Example usage
seed_text = "A surreal landscape with"
prompt = generate_prompt(seed_text)
print(prompt)