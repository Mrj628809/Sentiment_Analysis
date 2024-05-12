function fetchAndDisplayResults() {
    const videoUrl = document.getElementById("videoUrl").value;
    document.getElementById("loader").hidden = false;

    fetch("/analyze_comments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ video_url: videoUrl })
    })
    .then(response => response.json())
    .then(data => {
        displayCounts(data.sentiment_counts);
        displayLineChart(data.sentiment_over_time);
    })
    .catch(error => console.error("Error:", error))
    .finally(() => {
        document.getElementById("loader").hidden = true;
    });
}

function initializeChart() {
    const doughnutCtx = document.getElementById("sentimentDoughnutChart").getContext("2d");
    sentimentDoughnutChart = new Chart(doughnutCtx, {
        type: "doughnut",
        data: {
            labels: ["Positive", "Negative", "Neutral"],
            datasets: [{
                data: [0, 0, 0], 
                backgroundColor: ["#3699C8", "#8ABDD5", "#81D5FD"],
                hoverBackgroundColor: ["#3699C8", "#8ABDD5", "#81D5FD"]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    const barCtx = document.getElementById("sentimentBarChart").getContext("2d");
    sentimentBarChart = new Chart(barCtx, {
        type: "bar",
        data: {
            labels: ["Positive", "Negative", "Neutral"],
            datasets: [{
                data: [0, 0, 0], 
                backgroundColor: ["#3699C8", "#8ABDD5", "#81D5FD"],
                hoverBackgroundColor: ["#3699C8", "#8ABDD5", "#81D5FD"],
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

    const lineCtx = document.getElementById("sentimentLineChart").getContext("2d");
    sentimentLineChart = new Chart(lineCtx, {
        type: "line",
        data: {
            labels: [], 
            datasets: [{
                label: "Sentiment Over Time",
                data: [], 
                borderColor: "#3699C8",
                backgroundColor: "transparent",
                pointRadius: 1,
                pointHoverRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function updateChart(sentimentCounts) {
    sentimentDoughnutChart.data.datasets[0].data = [
        sentimentCounts["Positive"] || 0,
        sentimentCounts["Negative"] || 0,
        sentimentCounts["Neutral"] || 0
    ];
    sentimentDoughnutChart.update();

    sentimentBarChart.data.datasets[0].data = [
        sentimentCounts["Positive"] || 0,
        sentimentCounts["Negative"] || 0,
        sentimentCounts["Neutral"] || 0
    ];
    sentimentBarChart.update();
}

function displayLineChart(sentimentOverTime) {
    sentimentOverTime.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    const timestamps = sentimentOverTime.map(entry => entry.timestamp);
    const sentiments = sentimentOverTime.map(entry => entry.sentiment);

    sentimentLineChart.data.labels = timestamps;
    sentimentLineChart.data.datasets[0].data = sentiments;
    sentimentLineChart.update();
}

function displayCounts(sentimentCounts) {    
    const countsContainer = document.getElementById("counts");
    countsContainer.innerHTML = ""; // Clear previous counts

    Object.entries(sentimentCounts).forEach(([key, value]) => {
        const countDiv = document.createElement("div");
        countDiv.innerHTML = `${key}: ${value}`;
        countsContainer.appendChild(countDiv);
    });

    if (!sentimentDoughnutChart) {
        initializeChart();
    }
    
    updateChart(sentimentCounts);
}

document.addEventListener('DOMContentLoaded', function () {
    initializeChart();
});
