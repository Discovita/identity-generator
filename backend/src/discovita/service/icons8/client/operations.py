"""Icons8 API operations."""

from typing import List
from urllib.parse import quote
from httpx import AsyncClient
from pydantic import AnyHttpUrl, TypeAdapter
from ..models import (
    FaceSwapRequest,
    FaceSwapResponse,
    ImageId,
    FaceTask,
    Icons8Error,
    GetBboxRequest,
    GetBboxResponse,
    Face,
)
from ..face_selection import select_primary_face
from .logging import log_response

def validate_url(url: str) -> AnyHttpUrl:
    """Validate URL string and return AnyHttpUrl object."""
    url_adapter = TypeAdapter(AnyHttpUrl)
    return url_adapter.validate_python(url)

async def get_landmarks(client: AsyncClient, api_key: str, urls: List[str]) -> GetBboxResponse:
    """Get face landmarks for the given image URLs."""
    parsed_urls = [validate_url(url) for url in urls]
    request = GetBboxRequest(urls=parsed_urls)
    
    response = await client.post(
        "/get_bbox",
        params={"token": api_key},
        json={"urls": [str(url) for url in parsed_urls]}
    )
    
    response_data = response.json()
    log_response(response, "Get landmarks")
    
    if response.status_code >= 400:
        raise Icons8Error(
            status_code=response.status_code,
            detail=response_data.get('error', 'Unknown error')
        )
        
    return GetBboxResponse.parse_obj(response_data)

async def swap_faces(client: AsyncClient, api_key: str, source_url: str, target_url: str) -> FaceSwapResponse:
    """Submit a face swap job to Icons8."""
    target_http_url = validate_url(target_url)
    source_http_url = validate_url(source_url)
    
    landmarks_response = await get_landmarks(client, api_key, [source_url, target_url])
    source_faces = next(img for img in landmarks_response.faces if img.img_url == source_http_url)
    target_faces = next(img for img in landmarks_response.faces if img.img_url == target_http_url)
    
    assert source_faces.faces, "No faces detected in source image"
    assert target_faces.faces, "No faces detected in target image"
    
    # Convert raw faces to Face objects for proper bbox handling
    source_face_objs = source_faces.get_face_objects()
    target_face_objs = target_faces.get_face_objects()
    
    # Select primary faces based on size
    primary_source_face = select_primary_face([face.bbox for face in source_face_objs])
    primary_target_face = select_primary_face([face.bbox for face in target_face_objs])
    
    # Find corresponding Face objects
    source_face = next(face for face in source_face_objs if face.bbox == primary_source_face)
    target_face = next(face for face in target_face_objs if face.bbox == primary_target_face)
    
    request = FaceSwapRequest(
        target_url=target_http_url,
        face_tasks=[FaceTask(
            source_url=source_http_url,
            source_landmarks=source_face.landmarks,
            target_landmarks=target_face.landmarks
        )]
    )
    
    response = await client.post(
        "/process_image",
        params={"token": api_key},
        json={
            "target_url": str(target_http_url),
            "face_tasks": [{
                "source_url": str(source_http_url),
                "source_landmarks": source_face.landmarks,
                "target_landmarks": target_face.landmarks
            }]
        }
    )
    
    response_data = response.json()
    log_response(response, "Face swap request")
    
    if response.status_code >= 400:
        raise Icons8Error(
            status_code=response.status_code,
            detail=response_data.get('error', 'Unknown error')
        )
        
    return FaceSwapResponse.parse_obj(response_data)

async def get_job_status(client: AsyncClient, api_key: str, job_id: ImageId) -> FaceSwapResponse:
    """Get the status of a face swap job."""
    response = await client.get(
        f"/process_image/{job_id}",
        params={"token": api_key}
    )
    
    response_data = response.json()
    log_response(response, "Job status check")
    
    if response.status_code >= 400:
        raise Icons8Error(
            status_code=response.status_code,
            detail=response_data.get('error', 'Unknown error')
        )
        
    return FaceSwapResponse.parse_obj(response_data)

async def list_jobs(client: AsyncClient, api_key: str) -> List[FaceSwapResponse]:
    """Get list of face swap jobs."""
    response = await client.get(
        "/process_images",
        params={"token": api_key}
    )
    
    log_response(response, "List jobs")
    data = response.json()
    return [FaceSwapResponse.parse_obj(img) for img in data["images"]]
