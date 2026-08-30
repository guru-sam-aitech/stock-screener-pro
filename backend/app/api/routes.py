from fastapi import APIRouter

router = APIRouter()

@router.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# TODO: Add stock screener endpoints
# @router.get("/api/v1/screener")
# async def screen_stocks(...):
#     pass

# TODO: Add company endpoints
# @router.get("/api/v1/company/{symbol}")
# async def get_company(symbol: str):
#     pass
