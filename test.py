import json

js = "{\"choices\": [{\"finish_reason\": \"length\",\"index\": 0,\"logprobs\": null,\"text\": \"This is a test\"}],\"created\": 1654199133,\"id\": \"cmpl-5El37lZ4dHnQ2P8KsJu8EzulrpzQo\",\"model\": \"text-davinci-002\",\"object\": \"text_completion\"}"

print(js[70:80])

response = json.loads(js)
print(response['choices'][0]['text'])