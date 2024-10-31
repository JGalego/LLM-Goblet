r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⣤⣤⣤⣤⣤⣤⣀⣀⡀⠀
⠀⠀⠀⠀⠀⢀⣴⠾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⢶⣄
⠀⠀⠀⠀⠀⢸⣷⣤⣀⡉⠛⠛⠿⠿⠿⠿⠿⠿⠟⠛⠋⣁⣠⣴⣿
⠀⠀⠀⠀⠀⠈⣉⠙⢿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⠟⢉⡉
⠀⠀⠀⠀⠀⢸⣿⣧⠀⣿⣿⣿⣿⡟⢉⣈⠙⢿⣿⣿⣿⡇⢠⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⠀⡾⠻⠇⢘⣿⣿⣿⣇
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣆⠀⠀⢀⣼⣿⣿⣿⠟⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣾⣿⣿⡿⠛⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣭⣩⣥⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣬⣭⣭⣭⣄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣆
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠛⠿⢿⣿⣿⣿⣿⣿⠿⠟⠂⣀⡀
⠀⠀⠀⠀⠀⠀⠀⠘⠻⢿⣷⣶⣶⣤⣤⣤⣤⣴⣶⣶⣿⡿⠟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠁
  _      _      __  __    _____       _     _      _
 | |    | |    |  \/  |  / ____|     | |   | |    | |
 | |    | |    | \  / | | |  __  ___ | |__ | | ___| |_
 | |    | |    | |\/| | | | |_ |/ _ \| '_ \| |/ _ \ __|
 | |____| |____| |  | | | |__| | (_) | |_) | |  __/ |_
 |______|______|_|  |_|  \_____|\___/|_.__/|_|\___|\__|

LLM proxy powered by LiteLLM and Chalice
"""

import litellm

from chalice import Chalice

app = Chalice(app_name='llm-goblet')

@app.route("/chat/completions", methods=['POST'])
def completion():
    """
    Perform a completion using supported LLMs
    """
    request = app.current_request.json_body
    return litellm.completion(**request).to_json()

@app.route("/embeddings", methods=['POST'])
def embedding():
    """
    Generates embeddings for a given input.
    """
    request = app.current_request.json_body
    return litellm.embedding(**request).to_json()

@app.route("/images/generations", methods=['POST'])
def image_generation():
    """
    Generates a new image from a prompt.
    """
    request = app.current_request.json_body
    return litellm.image_generation(**request).to_json()

@app.route("/health", methods=['GET'])
def health():
    """For health check, if needed"""
    return {'status': "I'm alive!"}
