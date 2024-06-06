# CogLM
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





 