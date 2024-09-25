import httpx
from fastapi import HTTPException

class XquareClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client(base_url=self.base_url)

    def xquare_user(self, account_id: str, password: str) -> dict:
        try:
            response = self.client.post("/user-data", json={"account_id": account_id, "password": password})
            response.raise_for_status()  
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
