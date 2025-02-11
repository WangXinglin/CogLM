# CogLM: Tracking Cognitive Development of Large Language Models [NAACL2025 Main]

**Piaget's Theory of Cognitive Development (PTC) posits that the development of cognitive levels forms the foundation for human learning across various abilities. As Large Language Models (LLMs) have recently shown remarkable abilities across a wide variety of tasks, we are curious about the cognitive levels of current LLMs: to what extent they have developed and how this development has been achieved. To this end, we construct a benchmark CogLM (Cognitive Ability Evaluation for Language Model) based on PTC to assess the cognitive levels of LLMs. CogLM comprises 1,220 questions spanning 10 cognitive abilities crafted by more than 20 human experts, providing a comprehensive testbed for the cognitive levels of LLMs. Through extensive experiments across multiple mainstream LLMs with CogLM, we find that: (1) Human-like cognitive abilities have emerged in advanced LLMs (GPT-4), comparable to those of a 20-year-old human. (2) The parameter size and optimization objective are two key factors affecting the cognitive levels of LLMs. (3) The performance on downstream tasks is positively correlated with the level of cognitive abilities. These findings fill the gap in research on the cognitive abilities of LLMs, tracing the development of LLMs from a cognitive perspective and guiding the future direction of their evolution.**

## About
CogLM is a dataset designed and built based on Piaget's cognitive theory, comprising 1,220 questions spanning 10 cognitive abilities crafted by more than 20 human experts, providing a comprehensive testbed for the cognitive levels of LLMs.

## Quick Start
To get started, please first setup the environment:
```bash
conda create --name coglm --file requirements.txt
conda activate coglm
```

For the convenience of reproducing the results, we open-source the test data, test code, and final results. The following is an introduction to the code functions according to the process.

### Model Sampling
test_{OPT, GPT2, OPT_logit, GPT2_logit, llama, ChatGPT}.py are scripts for data sampling on different models, obtaining the model's responses on CogLM, and saving the results in the ./result directory. GPT2_logit and OPT_logit concatenate different answers to the corresponding questions and inputting them into the model, and the answer with the highest logit is selected as the model's output.

### Model Result Evaluation
{llama_chat, chatgpt, llm}_result.py are scripts for calculating the accuracy of different models on CogLM.





 
