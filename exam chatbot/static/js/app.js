let start = Date.now(); // Start timer when page loads or update this logic

function askAI() {
    // Optional: Reset timer for the specific question duration if needed
    // start = Date.now(); 

    const topicVal = document.getElementById("topic").value;
    const questionVal = document.getElementById("question").value;
    const marksVal = document.getElementById("marks").value;
    const answerBox = document.getElementById("answerBox");

    answerBox.innerText = "Thinking..."; // Show user something is happening

    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            topic: topicVal,
            question: questionVal,
            marks: marksVal,
            time: (Date.now() - start) / 1000
        })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Server Error");
        }
        return res.json();
    })
    .then(data => {
        answerBox.innerText = data.answer;
    })
    .catch(error => {
        console.error("Error:", error);
        answerBox.innerText = "Error: Could not get answer. Check console.";
    });
}
// ... rest of your code