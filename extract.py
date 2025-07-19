# extract_keywords.py
from click import prompt
from cohere_utils import co
import cohere
from Resume import *

def extract_keywords(jd_text, role="job"):
    # prompt = f"Extract keywords from the following {role} description:\n{jd_text}"
    # response = co.chat(
    #     model="command-a-03-2025",
    #     message=prompt
    # )
    # return response.text

    co = cohere.ClientV2("qr4pr7IfGpLfFzm10eyUTH7UrYClOh4snS8NhBgF")
    response = co.chat(
        model="command-a-03-2025", 
        messages=[{"role": "user", "content": "what is the blackhole ?"}]
    )
    anser = response.message.content[0].text
    print(anser)

    # co = cohere.ClientV2("qr4pr7IfGpLfFzm10eyUTH7UrYClOh4snS8NhBgF")
    # response = co.chat(
    #     model="command-a-03-2025", 
    #     messages=prompt
    # )
    # return response.text
    # print(response)
