from diffusers import AutoPipelineForText2Image
import torch
import uuid

pipeline = AutoPipelineForText2Image.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16).to("cuda")
pipeline.load_lora_weights("logo_lora", weight_name="pytorch_lora_weights.safetensors")
prompt = "a logo of beauty salon"
image = pipeline(prompt).images[0]
image.save(f"image_{uuid.uuid4()}.png")