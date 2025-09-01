let lastPrediction = "";
let sessionDetections = 0;
let confidenceSum = 0;

async function fetchPrediction() {
    try {
        const res = await fetch("/prediction");

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        console.log('Data received:', data);

        const pred = data.label || "Waiting for input...";
        const acc = data.accuracy ? (data.accuracy * 100).toFixed(1) + "%" : "-";
        const confidence = data.accuracy ? data.accuracy * 100 : 0;

        // Update UI elements
        const predElement = document.getElementById("prediction");
        const accElement = document.getElementById("accuracy");
        const confidenceFill = document.getElementById("confidence-fill");

        if (predElement) predElement.textContent = pred;
        if (accElement) accElement.textContent = acc;
        if (confidenceFill) confidenceFill.style.width = confidence + "%";

        // Add to history only if prediction changed and is not waiting
        if (pred !== "Waiting for input..." && pred !== "" && pred !== lastPrediction) {
            const historyBox = document.getElementById("history");
            if (historyBox) {
                const timestamp = new Date().toLocaleTimeString('en-US', {
                    hour12: false,
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
                historyBox.value += `[${timestamp}] ${pred} - Confidence: ${acc}\n`;
                historyBox.scrollTop = historyBox.scrollHeight;
                lastPrediction = pred;

                // Update statistics
                sessionDetections++;
                confidenceSum += confidence;
                updateStats();
            }
        }
    } catch (err) {
        console.error("Error fetching prediction:", err);
        const predElement = document.getElementById("prediction");
        if (predElement) predElement.textContent = "Connection Error";
    }
}

function updateStats() {
    const sessionCountEl = document.getElementById("session-count");
    const avgConfidenceEl = document.getElementById("avg-confidence");

    if (sessionCountEl) sessionCountEl.textContent = sessionDetections;
    if (avgConfidenceEl) {
        const avgConf = sessionDetections > 0 ? (confidenceSum / sessionDetections).toFixed(1) + "%" : "0%";
        avgConfidenceEl.textContent = avgConf;
    }
}

// Start fetching predictions when page loads
document.addEventListener('DOMContentLoaded', function () {
    console.log('Professional Sign Language Detection System initialized...');
    fetchPrediction();
    setInterval(fetchPrediction, 1000);
});

// Save functionality
document.getElementById("saveBtn").addEventListener("click", () => {
    const historyBox = document.getElementById("history");
    const text = historyBox ? historyBox.value : "";

    if (!text.trim()) {
        alert("No detection history to export!");
        return;
    }

    const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);

    const today = new Date();
    const dateStr = today.toISOString().split('T')[0];
    const timeStr = today.toTimeString().split(' ')[0].replace(/:/g, '-');

    link.download = `sign_detection_log_${dateStr}_${timeStr}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(link.href);
});

// Clear history functionality
document.getElementById("clearBtn").addEventListener("click", () => {
    const historyBox = document.getElementById("history");
    if (historyBox) {
        historyBox.value = "";
        sessionDetections = 0;
        confidenceSum = 0;
        updateStats();
    }
});