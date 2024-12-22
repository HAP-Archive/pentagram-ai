import os
from datetime import datetime, timezone

import modal
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = modal.App("pentagram-ai")
DOCKER_IMAGE = (
    modal.Image.debian_slim()
    .pip_install([
        "fastapi[standard]",
        "torch",
        "transformers",
        "accelerate",
        "diffusers",
        "requests",
    ])
    .env({
        "HF_ACCESS_TOKEN": os.getenv("HF_ACCESS_TOKEN"),
        "HF_STABLE_DIFFUSION_MODEL": os.getenv("HF_STABLE_DIFFUSION_MODEL"),
        "HF_STABLE_DIFFUSION_MODEL_FLUX": os.getenv("HF_STABLE_DIFFUSION_MODEL_FLUX"),
    })
)

MODAL_GPU = "A10G"
NUM_INFERENCE_STEPS = 4
GUIDANCE_SCALE = 0.0
MINUTES = 60

with DOCKER_IMAGE.imports():
    import os
    import requests
    from io import BytesIO

    import torch
    from diffusers import (
        AutoPipelineForText2Image,
        FluxPipeline
    )
    from fastapi import Response, Query


@app.function(
    schedule=modal.Cron("*/5 * * * *")
)
def keep_image_alive():
    health_url = "https://hi-kue--pentagram-ai-modalclient-health-check.modal.run"
    generate_image_url = "https://hi-kue--pentagram-ai-modalclient-generate-image.modal.run"

    health_response = requests.get(health_url)
    print(f""""
    Endpoint: {health_url}
    Status: {health_response.json()["status"]}
    Message: {health_response.json()["message"]}
    Timestamp: {health_response.json()["timestamp"]}
    """)

    generate_image_response = requests.get(generate_image_url)
    print(f"""
    Endpoint: {generate_image_url}
    Response: {generate_image_response.json()}
    Timestamp: {generate_image_response.json()["timestamp"]}
    """)


@app.cls(
    image=DOCKER_IMAGE,
    gpu=MODAL_GPU,
    container_idle_timeout=20 * MINUTES,
    cpu=4
)
class ModalClient:
    @modal.build()
    @modal.enter()
    def load_weights_sdm_no_refiner(self):
        self.pipe = AutoPipelineForText2Image.from_pretrained(
            pretrained_model_or_path=os.environ["HF_STABLE_DIFFUSION_MODEL"],
            torch_dtype=torch.bfloat16,
            variant="fp16",
            use_auth_token=os.environ["HF_ACCESS_TOKEN"]
        )
        self.pipe.to("cuda")

    # @modal.build()
    # @modal.enter()
    # def load_weights_flux(self):
    #     self.pipe_flux = FluxPipeline.from_pretrained(
    #         pretrained_model_name_or_path=os.environ["HF_STABLE_DIFFUSION_MODEL_FLUX"],
    #         torch_dtype=torch.bfloat16,
    #         use_auth_token=os.environ["HF_ACCESS_TOKEN"]
    #     )
    #     self.pipe_flux.to("cuda")

    @modal.web_endpoint()
    def generate_image(self, prompt: str = Query(..., description="Prompt for Image Generation")):
        try:
            generated_image = self.pipe(
                prompt=prompt,
                num_inference_steps=NUM_INFERENCE_STEPS,
                guidance_scale=GUIDANCE_SCALE
            ).images[0]

            buffer = BytesIO()
            generated_image.save(buffer, format="JPEG")
            return Response(content=buffer.getvalue(), media_type="image/jpeg")

        except Exception as e:
            print(f"Error occurred while generating image: {str(e)}")
            raise e

    # @modal.web_endpoint()
    # def generate_flux_image(self, prompt: str = Query(..., description="Prompt for Image Generation")):
    #     try:
    #         generated_image = self.pipe_flux(
    #             prompt=prompt,
    #             num_inference_steps=NUM_INFERENCE_STEPS,
    #             guidance_scale=GUIDANCE_SCALE,
    #             max_sequence_length=256,
    #             generator=torch.Generator("cpu").manual_seed(0)
    #         ).images[0]
    #
    #         buffer = BytesIO()
    #         generated_image.save(buffer, format="JPEG")
    #         return Response(content=buffer.getvalue(), media_type="image/jpeg")
    #
    #     except Exception as e:
    #         print(f"Error occurred while generating image: {str(e)}")
    #         raise e

    @modal.web_endpoint()
    def health_check(self):
        return {
            "status": "OK",
            "message": "Server is alive and actively processing various requests.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
