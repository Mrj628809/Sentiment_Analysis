let sentimentPieChart = null;

function fetchAndDisplayResults() {
    const videoUrl = document.getElementById("videoUrl").value;
    fetch("/analyze_comments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ video_url: videoUrl })
    })
    .then(response => response.json())
    .then(data => {
        // displayResults(data.sentiment_scores);
        displayCounts(data.sentiment_counts);
    })
    .catch(error => console.error("Error:", error));
}

// function categorizeSentiment(SentimentScore) {
//     if (SentimentScore > 0) {
//         return "Positive";
//     } else if (SentimentScore < 0) {
//         return "Negative";
//     } else {
//         return "Neutral";
//     }
// }

// function displayResults(sentimentScores) {
//     const resultsContainer = document.getElementById("results");
//     resultsContainer.innerHTML = ""; // Clear previous results

//     sentimentScores.forEach(score => {
//         const category = categorizeSentiment(score.compound);
//         const sentimentDiv = document.createElement("div");
//         sentimentDiv.innerHTML = `Sentiment: ${category}`;
//         resultsContainer.appendChild(sentimentDiv);
//     });
// }

function initializeChart() {
    const ctx = document.getElementById("sentimentPieChart").getContext("2d");
    sentimentPieChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Positive", "Negative", "Neutral"],
            datasets: [{
                data: [0, 0, 0], // Initialize with zeros
                backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"],
                hoverBackgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function updateChart(sentimentCounts) {
    sentimentPieChart.data.datasets[0].data = [
        sentimentCounts["Positive"] || 0,
        sentimentCounts["Negative"] || 0,
        sentimentCounts["Neutral"] || 0
    ];
    sentimentPieChart.update();
}

function displayCounts(sentimentCounts) {
    const countsContainer = document.getElementById("counts");
    countsContainer.innerHTML = ""; // Clear previous counts

    Object.entries(sentimentCounts).forEach(([key, value]) => {
        const countDiv = document.createElement("div");
        countDiv.innerHTML = `${key}: ${value}`;
        countsContainer.appendChild(countDiv);
    });

    if (!sentimentPieChart) {
        initializeChart();
    }
    
    updateChart(sentimentCounts);
}
