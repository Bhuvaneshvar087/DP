import google.generativeai as genai
import os

# Using your key
genai.configure(api_key="AIzaSyA_MZ2RD-DqZsRobfzULp2utByP8qe5H-c")

# We are using this because your screenshots prove YOU HAVE ACCESS to it.
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_exam_answer(question, marks):
    prompt = f"""
    You are an exam preparation assistant.
    Answer the following question strictly for {marks} marks.
    Use simple English, clear explanation, and exam-oriented format.

    Question: {question}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        print(f"AI ENGINE ERROR: {error_msg}")
        
        # If we hit the speed limit (429), tell the user nicely
        if "429" in error_msg:
            return "⚠️ Too Many Requests. Please wait 1-2 minutes and try again."
        
        return f"Error: {error_msg}"