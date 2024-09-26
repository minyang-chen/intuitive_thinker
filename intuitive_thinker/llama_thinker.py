from intuitive_thinker.mental_model import apply_thinking_model, MentalModel
from openai import OpenAI
import asyncio
import os
import json
from dotenv import load_dotenv
load_dotenv()

# openai_url = os.getenv("OPENAI_URL")
# openai_api_key = os.getenv("OPENAI_KEY")
# openai_model = os.getenv("OPENAI_MODEL")

# print(10*"-----")
# print(openai_url, openai_api_key, openai_model)
# print(10*"-----")

chat_completion = ""
use_stream = False


class LlamaIntuitiveThinker:

    def __init__(self, llm_url: str, llm_api_key: str, keep_alive: int = 100, options=None):
        self._llm_url = llm_url
        self._client = OpenAI(base_url=llm_url, api_key=llm_api_key)
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

    def llmchat(self, question: str,
                llm_model: str = None,
                mental_model: str = MentalModel.CHAIN_OF_THOUGHTS,
                available_functions=None,
                use_streaming: bool = False,
                options={"temperature": 0.7, "max_tokens": 1024}
                ):
        """invoke llm api"""

        # Initialize conversation with a user query
        if mental_model is None:
            mental_model = MentalModel.CHAIN_OF_THOUGHTS

        self._mental_model = MentalModel(mental_model)
        model_question = self._mental_model(question)
        # print("...mental model: ",mental_model)
        # print("...user_input: ",question)
        prompt = json.loads(model_question)

        # prepare first message
        messages = self.create_messages(
            prompt["user_input"], prompt['system_message'])

        chat_completion = ""
        if use_streaming:
            # Send the query and function description to the model
            print("Streaming...\n")
            stream = self._client.chat.completions.create(
                model=llm_model,
                messages=messages,
                temperature=options["temperature"], max_tokens=options["max_tokens"],
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")
                    chat_completion = chat_completion + \
                        chunk.choices[0].delta.content
            print()
            messages.append(chat_completion)
            return chat_completion
        else:
            # Send the query and function description to the model
            response = self._client.chat.completions.create(
                model=llm_model,
                messages=messages,
                temperature=options["temperature"], max_tokens=options["max_tokens"]
            )
            # Add the model's response to the conversation history
            messages.append(response.choices[0].message.content)
            return response.choices[0].message.content

    def parse_output(self, full_response):
        # Removing closing TAGS because sometimes skipped by GEMMA2
        text = full_response.replace('</thinking>', '')
        text = text.replace('</output>', '')
        text = text.replace('</reflection>', '')
        thinking = text.split('<thinking>')[-1].split('<reflection>')[0]
        reflection = text.split('<reflection>')[-1].split('<output>')[0]
        think_answer = text.split('<output>')[-1]  # full_response.split('<o
        return think_answer


if __name__ == "__main__":
    query = """
    Patel family who is planning a road trip from Toronto to Vancouver, covering a total distance of 4,400 km. They want to divide the drive into equal parts over 5 days, with each day's drive being 15 km longer than the previous day. If they drive x km on the first day, what is the value of x that will allow them to complete the trip in 5 days?]
    """
    # query = "how many r in word Strawberry?"

    openai_url = "http://192.168.0.26:11434/v1/"
    openai_api_key = "ollama"
    openai_model = "mychen76/llama3.1-intuitive-thinker:q5"

    options = {"temperature": 0.8, "max_tokens": 1024}

    openthinker = OpenAIIntuitiveThinker(
        llm_url=openai_url, llm_api_key=openai_key)
    response = openthinker.llmchat(question=query, llm_model=openai_model,
                                   use_streaming=True,
                                   mental_model=MentalModel.CHAIN_OF_THOUGHTS,
                                   options=options)
    print("======Full Response=========")
    print(response)
