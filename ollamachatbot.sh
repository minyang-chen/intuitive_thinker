#echo "ollama pull model"
#ollama pull "mychen76/llama3.1-intuitive-thinker:chain-of-thoughts.q5"

echo "run ollama chatbot"
python intuitive_thinker/ollama_chatbot.py --llm_model "mychen76/llama3.1-intuitive-thinker:chain-of-thoughts.q5" --llm_api_url "http://192.168.0.47:11434"
