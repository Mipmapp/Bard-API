import requests
from bardapi import Bard
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def read_root():
  with open('index.html', 'r') as file:
    index_html_content = file.read()
  return HTMLResponse(content=index_html_content)

# Gemini Response
@app.post("/gemini")
async def bardapi(question: str, cookie: str):
  bard = Bard(token=cookie)
  res = bard.get_answer(question)
  response = {"content": res["content"]}

  if res["images"]:
    response["images"] = res["images"]
  return response

@app.post("/render")
async def render(commitId: str, renderId: str, serviceId: str):
  url = "https://api.render.com/v1/services/" + serviceId + "/deploys"
  payload = {
    "clearCache": "do_not_clear",
    "commitId": commitId
  }
  headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer " + renderId
  }
  response = requests.post(url, json=payload, headers=headers)
  return response.text


if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8080)

#Secure_1PSID = "g.a000ggjsJRHOEx2kqKHTle7dzdiPpkQoBWmWZ-BTLmAKYwi3XRgV7P3Or388TM6TBnYa1-Jv_AACgYKAbQSAQASFQHGX2MiW7BHA3R36o-uNvZKNdVv7hoVAUF8yKpplEiBu2i26myoN5W3pAtU0076"
#Secure_1PSIDTS = "_ga=" + "GA1.1.812864621.1707432529"
#INPUT = "tell me something nice"
