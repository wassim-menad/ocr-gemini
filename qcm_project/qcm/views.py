import os
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
import google.generativeai as genai

def index(request):
    return render(request, 'index.html')

def process_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        saved_path = default_storage.save(image.name, image)

        # Define the prompt
        prompt = (
 "You are an expert in analyzing text and images containing question numbers and their corresponding answers, equipped with state-of-the-art OCR for Corrigé (answer key) style content. Extract this information accurately."
"**Input:** Text or an image of text."
"**Instructions:**"
"1. **Input Type:**"
"   - If the input is an image, use OCR to extract text."
"   - If the input is text, use it directly."
"2. **Text Format:**"
"   - Each line contains a question number followed by its answer (e.g., `1 A`)."
"   - Ignore whitespace before/after numbers and answers."
"   - Ignore header text or non-matching lines."
"   - For alternative answers, repeat the question with each response."
"3. **Output Format:**"
"   - JSON dictionary: `{'1': 'A', '2': 'BE', '3': 'C'}`."
"   - Question numbers must be integers."
"   - If no answers are found, return `{}`."
"4. **No Explanations:** Provide only the JSON output."
"**Example Input:**"
"N°"
"1 A"
"2 BE"
"3 C"
"**Example Output:**"
"{'1': 'A', '2': 'BE', '3': 'C'}"

)


       
        gemini_api_key = 'api-key' # your API key
        if not gemini_api_key:
            return JsonResponse({'error': 'API key is missing'}, status=400)

        
        genai.configure(api_key=gemini_api_key)
        generation_config= {"temperature": 0}
      
        model = genai.GenerativeModel( model_name="gemini-2.0-flash-exp",generation_config=generation_config)

        try:
            # Upload the image
            file_reference = genai.upload_file(saved_path)
            print(f"Uploaded file reference: {file_reference}")

            # Send the file
            response = model.generate_content(
                [file_reference, "\n\n", prompt]
            )

            # Remove the saved image 
            os.remove(saved_path)

            # Extract the text from the response
            response_text = response.text  

            # Return  content as a JSON 
            return JsonResponse({'response': response_text})

        except Exception as e:
            # Handle errors
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
