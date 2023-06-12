from pyllamacpp.model import Model
import json
from tqdm import tqdm
from Telegram import credentials

class ConversationalAI:
    def __init__(self):
        self.model = None
        self.memory = None

    def start(self):

        with open("character.json", 'r')as file:
             prompt_context = json.loads(file.read())["character_description"]

        prompt_prefix = "\nYou:"
        prompt_suffix = "\nColli:"
                
        # load model
        self.model = Model(model_path=credentials.model,
              n_ctx=512,
              prompt_context=prompt_context,
              prompt_prefix=prompt_prefix,
              prompt_suffix=prompt_suffix,
              n_gpu_layers=32,
              use_mlock = True)
        

    def generate_response(self, user_input, api_prompt = None):
        # Join messages
        conversation_history_input = "".join(user_input)

        if api_prompt != None:
            conversation_history_input = api_prompt + "\n" + conversation_history_input

        generated_response = ""

        # Wrap the loop with tqdm
        for token in tqdm(self.model.generate(conversation_history_input,
                                            antiprompt='You:',
                                            n_threads=6,
                                            n_predict=40,
                                            repeat_penalty=.5,
                                            frequency_penalty=.5),
                        desc='Generating response',
                        unit='token'):
            generated_response += token

        return generated_response
