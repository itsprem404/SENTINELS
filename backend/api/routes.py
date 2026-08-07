from fastapi import APIRouter

router = APIRouter(prefix="/api/agent", tags=["Agent"])


@router.post("/init")
def initialize_agent():
    return {
        "agentId": "123"
    }


@router.get("/feed")
def get_feed():
    return {
        "posts": []
    }
