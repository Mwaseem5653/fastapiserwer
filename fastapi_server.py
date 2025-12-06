from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "FastAPI server is running on Render!"}

@app.get("/proxy")
async def proxy(accountNumber: str):
    api_url = "https://easyload.com.pk/dingconnect.php"
    params = {"action": "GetProviders", "accountNumber": accountNumber}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url, params=params)
            response.raise_for_status()
            return JSONResponse(content=response.json())
        except httpx.HTTPStatusError as e:
            return JSONResponse(
                content={"error": f"HTTP error occurred: {e.response.status_code}"},
                status_code=e.response.status_code
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": f"An error occurred while requesting {e.request.url!r}."},
                status_code=500
            )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
