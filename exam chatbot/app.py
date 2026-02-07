from flask import Flask, render_template, request, jsonify
import time
from ai_engine import generate_exam_answer
from analytics import update_performance, generate_report

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data["question"]
    topic = data["topic"]
    marks = data["marks"]
    time_taken = data["time"]

    answer = "Error: Could not generate response."
    
    # RETRY LOGIC: Try up to 3 times if we hit a rate limit
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Try to generate the answer
            answer = generate_exam_answer(question, marks)
            
            # If successful, break out of the loop
            break 
            
        except Exception as e:
            error_msg = str(e)
            # Check if the error is likely a Rate Limit (429)
            if "429" in error_msg or "Too Many Requests" in error_msg or "Quota" in error_msg:
                if attempt < max_retries - 1:
                    print(f"Rate limit hit. Waiting 20 seconds... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(20)  # Wait 20 seconds before retrying
                    continue
            
            # If it's a different error, or we ran out of retries, print it
            print(f"API Error: {error_msg}")
            answer = "⚠️ System is busy (Rate Limit). Please wait 1 minute and try again."
            break

    # Simple correctness heuristic (AI self-check)
    correct = len(answer) > 50  

    update_performance(topic, correct, time_taken)

    return jsonify({"answer": answer})

@app.route("/report")
def report():
    return jsonify(generate_report())

if __name__ == "__main__":
    app.run(debug=True)
