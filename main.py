import json
from bardapi import Bard
from gemini import GeminiClient
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def read_root():
  with open('index.html', 'r') as file:
    index_html_content = file.read()
  return HTMLResponse(content=index_html_content)


# Simple Message Response
@app.post("/bard", response_class=HTMLResponse)
async def gemini(input: str, cookie: str, cookieTS: str):
  client = GeminiClient(cookie, "_ga=" + cookieTS, proxy=None)
  await client.init(timeout=120)

  try:
    response = await client.generate_content(input)
    json_response = {
        "content":
        response.text,
        "images":
        [image.url for image in response.images] if response.images else None
    }
    return json.dumps(json_response, indent=2)

  except Exception as e:
    return f"Error: {e}"


@app.post("/gemini")
async def bardapi(question: str, cookie: str):
  bard = Bard(token=cookie)
  res = bard.get_answer(question)
  response = {"content": res["content"]}

  if res["images"]:
    response["images"] = res["images"]
  return response


if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8080)

#Secure_1PSID = "g.a000ggjsJRHOEx2kqKHTle7dzdiPpkQoBWmWZ-BTLmAKYwi3XRgV7P3Or388TM6TBnYa1-Jv_AACgYKAbQSAQASFQHGX2MiW7BHA3R36o-uNvZKNdVv7hoVAUF8yKpplEiBu2i26myoN5W3pAtU0076"
#Secure_1PSIDTS = "_ga=" + "GA1.1.812864621.1707432529"
#INPUT = "tell me something nice"
