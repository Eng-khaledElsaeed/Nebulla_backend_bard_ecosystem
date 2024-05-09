import os
from django.conf import settings
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.api_core.exceptions import ServiceUnavailable, RetryError
import time
import PIL.Image
from io import BytesIO

genai.configure(api_key=settings.PAML_API_KEY)

def get_response(prompt, image=None):
    max_retries = 3
    retry_delay = 5  # seconds
    
    model_name = 'gemini-pro'
    if image:
        model_name = 'gemini-pro-vision'
    
    model = genai.GenerativeModel(model_name)

    for attempt in range(max_retries):
        try:
            if image:
                # Process image here if needed
                image_bytes = image.read()
                # Open the image using PIL
                image_pil = PIL.Image.open(BytesIO(image_bytes))
                response = model.generate_content([prompt, image_pil],
               
                                                  )
            else:
                chat =  model.start_chat(history=[])
                response =  chat.send_message(prompt)
                #response = model.generate_content([prompt], generation_config=genai.types.GenerationConfig(
                #    candidate_count=1,
                #    top_p=0.6,
                #    top_k=5))
            # Check if the response is valid
            if response and hasattr(response, 'text') and hasattr(response, 'prompt_feedback'):
                # Check if response.text is empty or None
                if response.text:
                    return {"response": response.text, "response_feedback": response.prompt_feedback}
                else:
                    print("Response text is empty.")
                    return {"response": "", "response_feedback": ""}
        except (ServiceUnavailable, RetryError) as e:
            if attempt < max_retries - 1:
                print(f"Retry attempt {attempt + 1} due to error: {e}")
                time.sleep(retry_delay)
            else:
                print(f"All retry attempts failed. Error: {e}")
                raise


# Example usage:
# response = get_response("your_prompt_here")
