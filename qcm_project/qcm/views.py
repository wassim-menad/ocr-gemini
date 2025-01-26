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
 "Your task is to accurately identify the marked options for each question in a multiple-choice question (QCM) grid. You should prioritize a correct extraction above all other considerations."
  
"*Input:*"

"The input will be an image of a QCM grid. The format of the grid is as follows:"
"  * Questions are numbered sequentially on the left side (e.g., Q1, Q2, Q3... up to Q20). The question number will be located next to the horizontal row with answer boxes."
"  * Answers are arranged in 5 columns at the top, labeled A, B, C, D, and E."
"  * The answer for each question is indicated by a cross ('X') inside the corresponding column box. Only boxes with a cross should be considered selected. Empty boxes should be considered unselected."

"*Instructions:*"

"1. *Image Processing:* You should use your image processing capabilities to identify the grid, the question numbers, and the markings within it. You should prioritize the accurate extraction of marked answers."

"2. *Extraction Logic:*"
"    * For each question, identify which answer options (A, B, C, D, E) are marked with a cross (X). The first box of the horizontal row should be considered answer A, second box should be considered answer B, and so on."
"    * If a question number cannot be identified, then skip it."
"    * If an answer box is not clearly marked, then use the character '?' in the corresponding position on the output string."
"    * If no answers are marked for a question, output a single character '.' as the answer string for that question."

"3. *Output Format:* Provide the extracted answers in the following format:"
"    * Each answer should be on a new line."
"    * Each answer should start with the question number, followed by a space, followed by a hyphen, followed by another space, followed by a string of letters (A, B, C, D, E) representing the selected options, listed in order. If a box was not marked, the corresponding letter should not appear in the string. If a box was not clearly marked then it should be replaced by the '?' character."
"    * The output letters must be in the order of the columns (A, then B, then C, then D, then E)."
   
   "         '1': 'ABD'"  
   "         '2': 'C'"  
   "         '3': 'BCE'"  
   "         ..."  
   "         '40': 'D'"  
   "     }"  

"4. *No Conversational Text or Explanations:* Output only the extracted answers in the described format. Do not include any extra information or conversational text."

"5. *Error Handling:* If you cannot extract any answers from the image or cannot identify any markings, then output an empty string."

"*Example Input (Visual representation, actual image will be provided):*"


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
