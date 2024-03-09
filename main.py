import requests
from bardapi import Bard
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from gemini import Gemini

app = FastAPI()

@app.get("/")
async def read_root():
  with open('index.html', 'r') as file:
    index_html_content = file.read()
  return HTMLResponse(content=index_html_content)

# Render API
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

# Gemini API
@app.post("/gemini")
async def gemini(question: str, cookie: str):
  cookies = {
    "__Secure-1PSID" : cookie
  }
  
  GeminiClient = Gemini(cookies=cookies)
  res = GeminiClient.generate_content(question)
  response = {"content": res.text}
  image_urls = []
  if res.web_images:
    for image in res.web_images:
      image_urls.append(image.url)
  
  if image_urls:
    response["images"] = image_urls

  return response

# ___________ #
if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8080)