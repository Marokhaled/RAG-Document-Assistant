import os
from typing import Dict, Any, Tuple, List
import httpx
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url

    def check_health(self) -> Tuple[bool, Dict[str, Any]]:
        """Query GET /health endpoint."""
        try:
            with httpx.Client(timeout=5.0) as client:
                res = client.get(f"{self.base_url}/health")
                if res.status_code == 200:
                    return True, res.json()
                return False, {"error": f"Backend returned status {res.status_code}"}
        except httpx.ConnectError:
            return False, {"error": f"Cannot connect to backend server at {self.base_url}. Is FastAPI running?"}
        except Exception as e:
            return False, {"error": str(e)}

    def send_query(self, question: str) -> Tuple[bool, Dict[str, Any]]:
        """Query POST /query endpoint."""
        try:
            with httpx.Client(timeout=60.0) as client:
                res = client.post(
                    f"{self.base_url}/query",
                    json={"question": question}
                )
                if res.status_code == 200:
                    return True, res.json()
                elif res.status_code == 422:
                    return False, {"error": "Invalid question format. Please enter a valid question."}
                else:
                    return False, {"error": f"Backend Error (HTTP {res.status_code}): {res.text}"}
        except httpx.ConnectError:
            return False, {"error": f"Unable to reach backend server at {self.base_url}. Please ensure the backend is running."}
        except httpx.ReadTimeout:
            return False, {"error": "Request timed out while waiting for LLM response. Please try again."}
        except Exception as e:
            return False, {"error": f"Unexpected error: {str(e)}"}


api_client = APIClient()
