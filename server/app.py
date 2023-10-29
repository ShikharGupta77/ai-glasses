import together
import openai

openai.api_key = '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'
together.api_key = '85ef951589f8fd8bfe69e6ef83d82dd664050bbe22ecddc7eee53c6b07718b5d'

output = together.Complete.create(
  prompt = "<human>: What are your thoughts on making an app that works like tinder for babies\n<bot>:", 
  model = "togethercomputer/LLaMA-2-7B-32K", 
  max_tokens = 256,
  temperature = 0.8,
  top_k = 60,
  top_p = 0.6,
  repetition_penalty = 1.1,
  stop = ['<human>', '\n\n']
)

# print generated text
print(output['prompt'][0]+output['output']['choices'][0]['text'])


