import os
import asyncio
import ollama
from ollama import Options
from rich import print

from intuitive_thinker.mental_model import apply_thinking_model
from intuitive_thinker.mental_model import MentalModel

from dotenv import load_dotenv
load_dotenv()


class OllamaIntuitiveThinker:

    def __init__(self, llm_url: str, keep_alive: int = 100, options=None):
        self._llm_url = llm_url
        # self._client=ollama.Client(host=llm_url)
        self._client = ollama.AsyncClient(host=llm_url)
        self._options = options
        self._keep_alive = keep_alive

    def create_messages(self, user_input: str, system_message: str = None):
        messages = []
        if system_message is None:
            messages = [{'role': 'user', 'content': user_input}]
        else:
            messages = [{'role': 'system', 'content': system_message}, {
                'role': 'user', 'content': user_input}]
        return messages

    def set_available_tools(self, tool_functions=None):
        tools = [
            {
                'type': 'function',
                'function': {
                    'name': 'apply_thinking_model',
                    'description': 'apply thinking model ',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'model': {
                                'type': 'string',
                                'description': 'thinking model name',
                            },
                            'query': {
                                'type': 'string',
                                'description': 'user query',
                            },
                        },
                        'required': ['model'],
                        'required': ['query'],
                    },
                },
            },
        ]
        self._tools = tools
        if tool_functions is not None:
            self._tools = tool_functions

    def set_api_options(self):
        options = Options()
        options["seed"] = 7676
        options["timeout"] = 120
        options["num_ctx"] = 4096
        # options["num_gpu"]=1
        # options["low_vram"]=True
        # options["num_thread"]=8
        # options["num_predict"]=2048
        # options["top_k"]=1
        self._options = options

    async def llmchat(self, question: str, llm_model: str = None, mental_model: str = None, available_functions=None):
        """invoke llm api"""
        self.set_available_tools(available_functions)
        self.set_api_options()

        # Initialize conversation with a user query
        if mental_model is not None:
            self._mental_model = MentalModel(mental_model)
            question = self._mental_model(question)
            # print("...mental model: ",mental_model)
            # print("...user_input: ",question)
            self._tools = None
        else:
            self.set_available_tools()

        # prepare fist message
        messages = self.create_messages(question)

        # First API call: Send the query and function description to the model
        response = await self._client.chat(
            model=llm_model,
            messages=messages,
            tools=self._tools,
            keep_alive=self._keep_alive,
            options=self._options
        )

        # Add the model's response to the conversation history
        messages.append(response['message'])

        # Check if the model decided to use the provided function
        if not response['message'].get('tool_calls'):
            print("***The model didn't use the function. Its response was:")
            # print(response['message']['content'])
            return response['message']['content']
        else:
            print("...calling tool:\n", response['message'].get('tool_calls'))

            # Process function calls made by the model
            if response['message'].get('tool_calls'):
                available_functions = {
                    'apply_thinking_model': apply_thinking_model, }
                for tool in response['message']['tool_calls']:
                    function_to_call = available_functions[tool['function']['name']]
                    function_args = tool['function']['arguments']
                    function_response = function_to_call(**function_args)
                    # print("call response:\n",function_response)
                    # print(10*"----")
                    if function_to_call == "apply_thinking_model":
                        res = json.loads(function_response)
                        messages = self.create_messages(
                            res['user_input'], res['system_message'])
                    else:
                        # Add function response to the conversation
                        messages.append(
                            {'role': 'tool', 'content': function_response})
                # Second API call: Get final response from the model
                final_response = await self._client.chat(model=llm_model,
                                                         messages=messages,
                                                         keep_alive=self._keep_alive,
                                                         options=self._options)
                print("***after tool call response***")
                return final_response['message']['content']

    def parse_output(self, full_response):
        # Removing closing TAGS because sometimes skipped by GEMMA2
        text = full_response.replace('</thinking>', '')
        text = text.replace('</output>', '')
        text = text.replace('</reflection>', '')
        thinking = text.split('<thinking>')[-1].split('<reflection>')[0]
        reflection = text.split('<reflection>')[-1].split('<output>')[0]
        think_answer = text.split('<output>')[-1]  # full_response.split('<o
        return think_answer

# if __name__ == "__main__":
#     ## Usage ###
#     ############
#     ollama_url = os.getenv("OLLAMA_URL")
#     ollama_key = os.getenv("OLLAMA_KEY")
#     ollama_model = os.getenv("OLLAMA_MODEL_BASE")

#     print(10*"-----")
#     print(ollama_url, ollama_key, ollama_model)
#     print(10*"-----")

#     query = "count number of letter r in word strawberry?"

#     thinker = OllamaIntuitiveThinker(llm_url=ollama_url)
#     response = await thinker.llmchat(question=query,
#                                llm_model=ollama_model,
#                                mental_model=MentalModel.CHAIN_OF_THOUGHTS)
#     print(10*"===")
#     print(response)

#     final_answer = thinker.parse_output(response)
#     print("========Final Answer=========")
#     print(final_answer)
