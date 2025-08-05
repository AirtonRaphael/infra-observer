from fastapi import FastAPI, APIRouter, HTTPException, Request, Response
import httpx

from auth import validate_jwt

services = {
        'auth': '127.0.0.1:8081'
        }

app = FastAPI()
router = APIRouter()


async def forward_request(service_url: str, path: str, request: Request, user_payload: dict | None = None):
    url = f"http://{service_url}/{path}"
    headers = dict(request.headers)
    body = await request.body()

    # Injeta dados do usuário autenticado nos headers
    if user_payload:
        headers["x-user-id"] = user_payload.get("sub", "")
        headers["x-user-role"] = user_payload.get("role", "")

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            content=body,
            headers=headers,
            params=request.query_params
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type")
    )


@router.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    if service not in services:
        raise HTTPException(status_code=404, detail=f"Serviço '{service}' não encontrado")

    # Extrair o token do header Authorization
    user_payload = None

    auth_header = request.headers.get("authorization")
    if auth_header or auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ")[1]
        user_payload = validate_jwt(token)

    return await forward_request(services[service], path, request, user_payload=user_payload)


app.include_router(router)
