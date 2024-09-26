# Intuitive Thinker
To enhance the reasoning capabilities of smaller-sized language models, employ a system of thinking that incorporates mental models, structured Chain-of-Thought processes, and thoughtful reflection before responding to user queries.

***Problem:*** 
smaller-sized transformer models exhibit inferior reasoning capabilities compared to their larger counterparts, whose advanced reasoning abilities stem from broader connection networks that facilitate cross-domain inference.

***Solution:***
Two-Step Approach:
> 1. Finetuning: Commence by fine-tuning the Llama 3.1, a smaller-sized transformer model with 8 billion parameters, on an enhanced reasoning dataset to bolster its cognitive capabilities.
> 2. Revelation of Internal Processes: Subsequently, leverage a system of thinking model guidance techniques (Think, Plan, Reasoning and Reflection) to unveil the model's internal thought processes and the rationales underlying its processing mechanisms.

## Features 
> Finetuned Llama 3.1 8B model to improve small LLM model reasoning
> API for static or dynamic thinking guidance of system of thinking
> Support Ollama for local usage

## Available Mental Models 
System of thinking, reasoning and reflection
> 1. Chain-of-Thoughts
> 2. Thinking Fast and Slow
> 3. Critical Thinking
> 4. Iceberg Mental Model
> 5. Second Order Thinking

## Available LLM Models

#### Huggingface.co
https://huggingface.co/collections/mychen76/intuitive-thinker-66f305e9cbe35a1ea95d54cb

Base Model: mychen76/Llama-3.1_Intuitive-Thinker
https://huggingface.co/mychen76/Llama-3.1_Intuitive-Thinker

Quantized:  mychen76/Llama-3.1_Intuitive-Thinker_8B_2309_GGUF
https://huggingface.co/mychen76/Llama-3.1_Intuitive-Thinker_8B_2309_GGUF

 
#### Ollama.com
https://ollama.com/mychen76/llama3.1-intuitive-thinker

For direct easy to use each mental model has been package on own model package. 

1. Chain-of-Thoughs: [mychen76/llama3.1-intuitive-thinker:chain-of-thoughts.q5]
2. Thinking Fast and Slow: [mychen76/llama3.1-intuitive-thinker:thinking-fast-n-slow.q5]
3. Critical Thinking: [mychen76/llama3.1-intuitive-thinker:critical-thinking.q5]
4. Iceberg Mental Model: [mychen76/llama3.1-intuitive-thinker:iceberg-mental-model.q5]
5. Second Order Thinking: [mychen76/llama3.1-intuitive-thinker:second-order-thinking.q5]


## Installation

clone repo:

python package only
```bash
cd intuitive_thinker
pip install dist/intuitive_thinker-0.1.0-py3-none-any.whl
```

## Development

[Poetry](https://python-poetry.org/docs/#installation) is used for dependency management.

```bash
poetry install
```
shell
```bash
cd intuitive_thinker
poetry shell
```

## Usage: Ollama

Directly using ollama CLI:
Example: Chain-of-Thoghts, Reasoning and Reflection

***download model***
see list here: https://ollama.com/mychen76/llama3.1-intuitive-thinker

```bash
ollama pull mychen76/llama3.1-intuitive-thinker:chain-of-thoughts.q5
```
***run model***
```bash
ollama run mychen76/llama3.1-intuitive-thinker:chain-of-thoughts.q5
```
***ask question***
```
>> Patel family who is planning a road trip from Toronto to Vancouver, covering a total distance of 4,400 km. They want to divide the drive into equal parts over 5 days, with each day's drive being 15 km longer than the previous day. If they drive x km on the first day, what is the value of x that will allow them to complete the trip in 5 days?
```
response
```bash
>>>
<thinking>

To solve this problem, we need to determine the value of x, which represents the distance driven on the first day.

Step 1: Understand the constraints of the problem
The total distance to be covered is 4,400 km, and the drive should be divided into equal parts over 5 days. Each day's drive 
should be 15 km longer than the previous day.

..........
```

## Usage: API calling Ollama  

***Installation***
```bash
git clone
poetry shell
```
***Usage***
```bash
query = "Patel family who is planning a road trip from Toronto to Vancouver, covering a total distance of 4,400 km. They want to divide the drive into equal parts over 5 days, with each day's drive being 15 km longer than the previous day. If they drive x km on the first day, what is the value of x that will allow them to complete the trip in 5 days?"

thinker = IntuitiveThinker(llm_url=ollama_url,options=None)
response = await thinker.llmchat(question=query, llm_model=ollama_model, 
                                 mental_model=MentalModel.THINKING_FAST_N_SLOW)

print("======Full Response=========")
print(response)
```
Result
```bash
***The model didn't use the function. Its response was:
======Full Response=========
<thinking>
<thinking-fast>
Initial analysis:
- The Patel family needs to cover a total distance of 4,400 km.
- They want to divide the drive into equal parts over 5 days.
- Each day's drive should be 15 km longer than the previous day.
- We need to find the value of x that represents the distance driven on the first day.

Approach:
1. Calculate the total additional distance covered over 5 days.
2. Divide this by 5, as each day is 15 km longer than the previous one.
3. Add this increase to the distance driven on the first day (x) to find the value of x.

<thinking-slow>
Carefully interpreting the problem:
- Understanding the total distance and number of days are constant, so we can calculate based on given variables.
- Recognizing that each day's drive is 15 km longer due to a linear progression in distance.
- Breaking down the thought process into step-by-step calculations.

Suppressing biases:
- Ensuring the assumption about equal daily progressions doesn't skew reasoning.
- Double-checking for any potential oversights or simplifications.

Overriding initial impulse:
- Allowing for the calculation of x without assuming it's a simple arithmetic progression due to the given 
constraints.
</thinking-fast>
<thinking-slow>
Detailed step-by-step calculation:

1. Calculate the total additional distance covered over 5 days:
   Since each day is 15 km longer than the previous, this forms an arithmetic sequence where the difference between
consecutive terms (d) = 15 km.
   
2. The sum of the distances covered over these 5 days can be represented as:
   S = x + (x+15) + (x+30) + (x+45) + (x+60)
   
3. Since the total distance is 4,400 km and this sum equals 5x + 150, we can set up an equation:
   5x + 150 = 4400
   
4. Solving for x to find the initial day's distance:

   5x = 4400 - 150
   5x = 4250
   x = 850
   
Therefore, the value of x that will allow the Patel family to complete the trip in 5 days is 850 km.
</thinking-fast>

<reflection>
Reviewing reasoning and potential errors:
- The assumption about equal daily progressions and linear increase seems valid given the constraints.
- Ensuring the arithmetic progression calculation accounts for all additional distances.

Checking calculations:
1. Confirm the sequence of daily distances: x, (x+15), (x+30), (x+45), (x+60)
2. Verify that the total distance is correctly represented as 5x + 150
3. Double-check the arithmetic in the equation: 5x = 4400 - 150

Conclusion seems sound, but always worth a careful check.
</reflection>

<output>
The value of x that allows the Patel family to complete their road trip from Toronto to Vancouver in 5 days is 850 
km on the first day. This calculation accounts for the linear increase in daily distance and ensures the total trip
length covers the required 4,400 km over the specified period.
</thinking>
```
Parsed Final Result
```bash
final_answer = thinker.parse_output(response)
print("========Final Answer=========")
print(final_answer)
```
Result
```
========Final Answer=========
The value of x that allows the Patel family to complete their road trip from Toronto to Vancouver in 5 days is 850 
km on the first day. This calculation accounts for the linear increase in daily distance and ensures the total trip
length covers the required 4,400 km over the specified period.
```

## Usage Chatbot
```bash
./ollamachatbot.sh
```

## License

Intuitive_thinker source ode is released under the MIT License. You are free to use, modify, and distribute this software for any purpose, commercial or non-commercial, as long as the original copyright and license notice are included.

LLM follow Meta LLama Licensing model

### export requirements.txt
poetry export --output requirements.txt


### Credit
Inspiration from OpenAI-01 and Reflection-70B

