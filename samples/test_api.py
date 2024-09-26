
import ollama
from ollama import Options
import asyncio
from intuitive_thinker.thinker import IntuitiveThinker

query = "count number of letter r in word strawberry?"

thinker = IntuitiveThinker(llm_url=ollama_url)
response = await thinker.llmchat(question=query,
                                 llm_model=ollama_model,
                                 mental_model=MentalModel.CHAIN_OF_THOUGHTS)

print("========Full Response========")
print(response)

final_answer = thinker.parse_output(response)
print("\n========Final Answer=========")
print(final_answer)
