
function buildCharts(chartsData) {
    // гистограмма цен
    const priceHistogramCtx = document.getElementById('priceHistogram').getContext('2d');
    new Chart(priceHistogramCtx, {
        type: 'bar',
        data: {
            labels: chartsData.price_histogram.map(item => item.price_range),
            datasets: [{
                label: 'Количество товаров',
                data: chartsData.price_histogram.map(item => item.count),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // скидка и рейтинг
    const discountVsRatingCtx = document.getElementById('discountVsRating').getContext('2d');
    new Chart(discountVsRatingCtx, {
        type: 'line',
        data: {
            labels: chartsData.discount_vs_rating.map(item => item.discount),
            datasets: [{
                label: 'Рейтинг',
                data: chartsData.discount_vs_rating.map(item => item.rating),
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        
        ooptions: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Рейтинг'
                    },
                    min: 0.0,
                    max: 5.0,
                    ticks: {
                        stepSize: 0.1
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Скидка (%)'
                    },
                    min: 0,
                    suggestedMax: Math.max(...chartsData.discount_vs_rating.map(item => parseFloat(item.discount))) || 100
                }
            }
        }
    });
}

// инициализация графиков
document.addEventListener("DOMContentLoaded", function () {
    const chartsData = JSON.parse(document.getElementById('charts-data').textContent);
    buildCharts(chartsData);
});