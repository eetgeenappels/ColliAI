python -m venv env
source env/bin/activate

pip install --upgrade pip

pip install discord.py
pip install selenium==4.9.0 selenium-wire
pip install tqdm
pip install torch torchvision torchaudio
pip install InstructorEmbedding
pip install sentence-transformers
pip install chromadb
pip install pyTelegramBotAPI


CMAKE_ARGS="-DCMAKE_OSX_ARCHITECTURES=arm64" pip install --upgrade --verbose --force-reinstall --no-cache-dir llama-cpp-python