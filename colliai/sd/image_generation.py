# stable diffusion using diffusers

import spacy
from diffusers import DiffusionPipeline
from diffusers import DDPMScheduler
from Telegram import credentials


def load_model():

    global pipeline
    global spacy_model


    # load models
    pipeline = DiffusionPipeline.from_pretrained(credentials.sd_model, vae = credentials.sd_model_vae)
    pipeline.scheduler = DDPMScheduler.from_config(pipeline.scheduler.config)

    spacy_model = spacy.load("en_core_web_trf")

def get_image_from_message(message):
    
    global spacy_model
    global pipeline

    doc = spacy_model(message)

    subject = None
    adjectives = []
    
    for token in doc:
        if token.dep_ == "nsubj":
            subject = token.text
        if token.pos_ == "ADJ":
            adjectives.append(token.text)

    prompt = f"{subject}, "

    for i in adjectives:
        prompt += f"{i}, "

    return pipeline(message)
