# ColliAI

ColliAI is a presonal assistant telegram bot. Powererd by llama.cpp and chromadb

## How to install dependencies

> Make sure to use python 3.12 because python 3.12 is cool

First you need to create a new conda/ venv environment

Then you need to install the dependencies

```sh

pip install pyTelegramBotAPI

# for most people
pip install llama-cpp-python

or

# if you have a mac
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

pip install selenium==4.9.0 selenium-wire
pip install tqdm
pip install torch torchvision torchaudio
pip install InstructorEmbedding
pip install sentence-transformers
pip install chromadb
```

## How to use it

Fill in everything in config.json.

Then run colli_ai.py
