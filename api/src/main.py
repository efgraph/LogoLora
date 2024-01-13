import logging
import os
import random
import time
import torch
from diffusers import StableDiffusionPipeline
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse
from pathlib import Path

parent_dir_path = Path(__file__).parent.parent
static_path = os.path.join(parent_dir_path, 'static')
if not os.path.exists(static_path):
    os.makedirs(static_path)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

log.info('Load Stable Diffusion model')
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

pipe = pipe.to('cuda')
pipe.enable_attention_slicing()


class Payload(BaseModel):
    prompt: str
    num_images = 1
    height = 512
    width = 512
    seed: int | None = None
    num_steps = 40
    guidance_scale = 8.5


class Response(BaseModel):
    images: list[str]
    nsfw_content_detected: list[bool]
    prompt: str
    num_images: int
    height: int
    width: int
    seed: int
    num_steps: int
    guidance_scale: float


log.info('Start API')
log.info(parent_dir_path)
app = FastAPI(docs_url='/docs',
              openapi_url='/docs.json',
              default_response_class=ORJSONResponse)
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.post('/generate', response_model=Response, description='Runs logo generation with Stable Diffusion.')
def generate(payload: Payload, request: Request):
    try:
        log.info(f'Payload: {payload}')

        if payload.seed is None:
            payload.seed = random.randint(-999999999, 999999999)
        generator = torch.Generator('cuda').manual_seed(payload.seed)

        prompt = [payload.prompt] * payload.num_images

        log.info('Run generate')
        with torch.autocast('cuda'):
            result = pipe(
                prompt=prompt,
                height=payload.height,
                width=payload.width,
                num_inference_steps=payload.num_steps,
                guidance_scale=payload.guidance_scale,
                generator=generator
            )
        log.info('generate completed')

        images_urls = []
        for image in result.images:
            image_name = str(time.time()).replace('.', '') + '.png'
            image_path = os.path.join(static_path, image_name)
            image.save(image_path)
            image_url = request.url_for('static', path=image_name)
            images_urls.append(image_url.path)

        response = {'images': images_urls, 'nsfw_content_detected': result['nsfw_content_detected'],
                    'prompt': payload.prompt, 'num_images': payload.num_images, 'height': payload.height,
                    'width': payload.width, 'seed': payload.seed, 'num_steps': payload.num_steps,
                    'guidance_scale': payload.guidance_scale}

        return response

    except Exception as e:
        log.error(repr(e))
        raise HTTPException(status_code=500, detail=repr(e))
