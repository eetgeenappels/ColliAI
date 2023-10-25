from llama_cpp import Llama
import json
import credentials

class ConversationalAI:
    def __init__(self):
        self.memory = None

        with open("character.json", 'r')as file:
            self.prompt_context = json.loads(file.read())["character_description"]

        prompt_prefix = ""
        prompt_suffix = "\n### Colli"
                
        # load model
        self.model = Llama(model_path=credentials.model, use_mlock=True, n_gpu_layers=-1,prompt_prefix=prompt_prefix,
              prompt_suffix=prompt_suffix)
        

    def generate_response(self, user_input,memory_prompt = None, api_prompt = None):
        # Join messages
        conversation_history_input = "".join(self.prompt_context)

        if memory_prompt != None:
            conversation_history_input = "\n" + conversation_history_input[1:].join(memory_prompt) + conversation_history_input[-1:]
        if api_prompt != None:
            conversation_history_input = "\n" + conversation_history_input[1:] + api_prompt + conversation_history_input[-1:]
        
        conversation_history_input = conversation_history_input.join(user_input)

        return self.model(conversation_history_input, stop=["\n","###"],repeat_penalty=1.5,echo=True)["choices"][0]["text"][len(conversation_history_input):]
