import shutil
import asyncio
import argparse
import sys
import ollama
from rich import print
import json


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--llm_model', type=str,
                        default="mychen76/llama3.1-intuitive-thinker:chain-of-thoughts.q5")
    # parser.add_argument('--llm_model', type=str, default="mychen76/llama3.1-intuitive-thinker:q5")
    parser.add_argument('--llm_api_url', type=str,
                        default="http://localhost:11434")
    args = parser.parse_args()
    print(args.llm_model, args.llm_api_url)

    client = ollama.AsyncClient(args.llm_api_url)
    messages = []

    while True:
        if content_in := input('>>> '):
            if content_in == "\bye":
                print("good bye!\n")
                sys.exit(0)

            # add message
            messages.append({'role': 'user', 'content': content_in})

            content_out = ''
            message = {'role': 'assistant', 'content': ''}
            async for response in await client.chat(model=args.llm_model,
                                                    messages=messages,
                                                    stream=True):
                if response['done']:
                    messages.append(message)
                else:
                    content = response['message']['content']
                    print(content, end='', flush=True)

                    content_out += content
                    if content in ['.', '!', '?', '\n']:
                        content_out = ''

                    message['content'] += content

            if content_out:
                print(content_out)
            print()
try:
    asyncio.run(main())
    # await main()
except (KeyboardInterrupt, EOFError):
    ...
