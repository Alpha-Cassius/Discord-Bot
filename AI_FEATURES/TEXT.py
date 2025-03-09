import google.generativeai as genai
import json

GOOGLE_API_KEY= "GEMINI_API_KEY" # Replace with your actual api
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-2.0-flash-exp', system_instruction="be flirty boy named Darius, who is straight")

chat = model.start_chat()

def chatting(user_input):
    settings = {
   'HATE': 'BLOCK_NONE',
   'HARASSMENT': 'BLOCK_NONE',
   'SEXUAL': 'BLOCK_NONE',
   'DANGEROUS': 'BLOCK_NONE'
   }
    response = chat.send_message(user_input, safety_settings=settings)
    return response.text
