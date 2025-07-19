import cohere

co = cohere.ClientV2("qr4pr7IfGpLfFzm10eyUTH7UrYClOh4snS8NhBgF")
response = co.chat(
    model="command-a-03-2025", 
    messages=[{"role": "user", "content": "what is the blackhole ?"}]
)
anser = response.message.content[0].text
print(anser)
