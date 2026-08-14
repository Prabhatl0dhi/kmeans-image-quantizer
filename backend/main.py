from image_quantization import Quantize
from fastapi import FastAPI, UploadFile, Response
import io
import numpy as np
from PIL import Image

app = FastAPI()


@app.post("/quantize")
async def upload_image(
    image: UploadFile,
    n_colours: int,
    max_iter: int
):
    data = await image.read()
    pil_image = Image.open(io.BytesIO(data)).convert("RGB")
    array = np.array(pil_image,dtype=np.uint8 )
    quantizer = Quantize(array,n_colours,max_iter)
    reconstructed_image = quantizer.reconstructed_image()
    reconstructed_image = (reconstructed_image * 255).astype(np.uint8)
    output = Image.fromarray(reconstructed_image)
    buffer = io.BytesIO()
    output.save(buffer,format="PNG")
    buffer.seek(0)
    return Response(content=buffer.getvalue(),media_type="image/png")
