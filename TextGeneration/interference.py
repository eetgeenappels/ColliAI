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
              prompt_prefix=prompt_prefix,
              prompt_suffix=prompt_suffix,
              use_mlock = True)
        

    def generate_response(self, user_input, api_prompt = None):
        # Join messages
        conversation_history_input = "".join(user_input)

        if api_prompt != None:
            conversation_history_input = "\n" + conversation_history_input[1:] + api_prompt + conversation_history_input[-1:]



        generated_response = ""

        # Wrap the loop with tqdm
        for token in tqdm(self.model.generate(conversation_history_input,
                                            antiprompt='You:',
                                            n_threads=6,
                                            n_predict=40),
                        desc='Generating response',
                        unit='token'):
            generated_response += token
            if len(generated_response) >= 4:
                continue

            if generated_response[-4:] == "You:":
                # remove Colli from document
                generated_response = generated_response[4:]
                break
        
            if len(generated_response) >= 6:
                continue

            # check if last 6 characters are COlli
            if generated_response[-6:] == "Colli:":
                # remove Colli from document
                generated_response = generated_response[6:]
                break
            # check if last 4 characters are You:

        return generated_response
