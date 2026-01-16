/**
 * UIDAI Dashboard - Interactive JavaScript
 * =========================================
 * Chart.js visualizations and interactivity
 */

// =============================================================================
// STATE DATA
// =============================================================================

const stateData = {
    labels: [
        'Meghalaya', 'Assam', 'Nagaland', 'Bihar', 'West Bengal',
        'Uttar Pradesh', 'Madhya Pradesh', 'Gujarat', 'Rajasthan', 'Sikkim',
        'Jharkhand', 'Jammu And Kashmir', 'Arunachal Pradesh', 'Telangana',
        'Mizoram', 'Haryana', 'Delhi', 'Odisha', 'Lakshadweep',
        'Himachal Pradesh', 'Tamil Nadu', 'Kerala'
    ],
    ifi: [1.6, 8.7, 9.4, 15.9, 17.0, 17.8, 17.8, 17.9, 19.6, 19.6,
        21.8, 24.4, 26.1, 25.8, 27.4, 28.5, 29.0, 29.1, 29.5, 31.2, 31.3, 31.4],
    clcr: [0.00, 0.05, 0.05, 0.02, 0.03, 0.03, 0.07, 0.05, 0.05, 0.03,
        0.03, 0.05, 0.05, 0.10, 0.18, 0.10, 0.07, 0.14, 0.60, 0.16, 0.16, 0.09],
    taes: [0.00, 0.08, 0.08, 0.57, 0.45, 0.32, 0.36, 0.12, 0.29, 0.18,
        0.30, 0.15, 0.44, 0.53, 0.47, 0.26, 0.50, 0.56, 0.62, 0.49, 0.49, 0.58],
    composite: [0.84, 0.85, 0.86, 0.95, 0.92, 0.90, 0.91, 0.86, 0.89, 0.87,
        0.89, 0.94, 0.92, 0.94, 0.93, 0.93, 0.93, 0.94, 0.95, 0.94, 0.93, 0.95],
    region: [
        'Northeast', 'Northeast', 'Northeast', 'East', 'East',
        'Central', 'Central', 'West', 'North', 'Northeast',
        'East', 'North', 'Northeast', 'South', 'Northeast',
        'North', 'North', 'East', 'South', 'North', 'South', 'South'
    ],
    risk: [
        'Critical', 'Critical', 'Critical', 'At Risk', 'At Risk',
        'At Risk', 'At Risk', 'At Risk', 'At Risk', 'At Risk',
        'Healthy', 'Healthy', 'Healthy', 'Healthy', 'Healthy',
        'Healthy', 'Healthy', 'Healthy', 'Healthy', 'Optimal', 'Optimal', 'Optimal'
    ]
};

// Volume data
const volumeData = {
    labels: ['Enrolments', 'Demo Updates', 'Bio Updates'],
    values: [4.8, 23.2, 35.6],
    colors: ['#1565C0', '#FFB300', '#43A047']
};

// Color schemes
const COLORS = {
    critical: '#E53935',
    atRisk: '#FFB300',
    healthy: '#43A047',
    optimal: '#1E88E5',
    primary: '#1565C0',
    secondary: '#7B1FA2',
    grid: '#E0E0E0'
};

// =============================================================================
// CHART INSTANCES
// =============================================================================

let ifiChart, volumeChart, clcrChart, taesChart, comparisonChart;

// =============================================================================
// CHART INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', function () {
    initializeCharts();
    animateKPIs();
});

function initializeCharts() {
    createIFIChart();
    createVolumeChart();
    createCLCRChart();
    createTAESChart();
    createComparisonChart();
}

function createIFIChart() {
    const ctx = document.getElementById('ifiChart').getContext('2d');

    // Sort data by IFI score
    const sortedIndices = stateData.ifi.map((val, idx) => idx)
        .sort((a, b) => stateData.ifi[a] - stateData.ifi[b]);

    const sortedLabels = sortedIndices.map(i => stateData.labels[i]);
    const sortedIFI = sortedIndices.map(i => stateData.ifi[i]);
    const sortedColors = sortedIndices.map(i => getIFIColor(stateData.ifi[i]));

    ifiChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedLabels.slice(0, 15),
            datasets: [{
                label: 'IFI Score',
                data: sortedIFI.slice(0, 15),
                backgroundColor: sortedColors.slice(0, 15),
                borderColor: sortedColors.slice(0, 15),
                borderWidth: 0,
                borderRadius: 6,
                barThickness: 20
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `IFI: ${ctx.raw.toFixed(1)}`,
                        afterLabel: (ctx) => getRiskLabel(ctx.raw)
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 35,
                    grid: { color: COLORS.grid, drawBorder: false },
                    ticks: { font: { size: 11 } }
                },
                y: {
                    grid: { display: false },
                    ticks: { font: { size: 10, weight: '500' } }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            }
        }
    });

    // Add threshold line annotation
    addThresholdLine(ifiChart, 28.2, 'National Avg: 28.2', COLORS.critical);
}

function createVolumeChart() {
    const ctx = document.getElementById('volumeChart').getContext('2d');

    volumeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: volumeData.labels,
            datasets: [{
                label: 'Volume (Millions)',
                data: volumeData.values,
                backgroundColor: volumeData.colors,
                borderWidth: 0,
                borderRadius: 8,
                barThickness: 80
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.raw.toFixed(1)}M records`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: COLORS.grid },
                    ticks: {
                        callback: (val) => val + 'M',
                        font: { size: 11 }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 12, weight: '600' } }
                }
            },
            animation: {
                duration: 1200,
                delay: (context) => context.dataIndex * 200
            }
        }
    });
}

function createCLCRChart() {
    const ctx = document.getElementById('clcrChart').getContext('2d');

    // Sort by CLCR (lowest first for gaps)
    const sortedIndices = stateData.clcr.map((val, idx) => idx)
        .sort((a, b) => stateData.clcr[a] - stateData.clcr[b]);

    const sortedLabels = sortedIndices.map(i => stateData.labels[i]).slice(0, 12);
    const sortedCLCR = sortedIndices.map(i => stateData.clcr[i]).slice(0, 12);
    const gaps = sortedCLCR.map(val => 1.0 - val);

    clcrChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedLabels,
            datasets: [{
                label: 'Gap from Target',
                data: gaps,
                backgroundColor: gaps.map(g => g > 0.8 ? COLORS.critical : g > 0.5 ? COLORS.atRisk : COLORS.healthy),
                borderWidth: 0,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'Gap from 1.0 CLCR Target (Lower = Better)',
                    font: { size: 11, weight: 'normal' },
                    color: '#616161'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1.1,
                    grid: { color: COLORS.grid },
                    ticks: {
                        callback: (val) => (val * 100).toFixed(0) + '%',
                        font: { size: 10 }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        font: { size: 9 },
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
}

function createTAESChart() {
    const ctx = document.getElementById('taesChart').getContext('2d');

    // Sort by TAES
    const sortedIndices = stateData.taes.map((val, idx) => idx)
        .sort((a, b) => stateData.taes[a] - stateData.taes[b]);

    const sortedLabels = sortedIndices.map(i => stateData.labels[i]).slice(0, 12);
    const sortedTAES = sortedIndices.map(i => stateData.taes[i]).slice(0, 12);

    taesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedLabels,
            datasets: [{
                label: 'TAES Score',
                data: sortedTAES,
                backgroundColor: sortedTAES.map(t => t < 0.3 ? COLORS.critical : t < 0.5 ? COLORS.atRisk : COLORS.healthy),
                borderWidth: 0,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: 0.7,
                            yMax: 0.7,
                            borderColor: COLORS.optimal,
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'Target: 0.70',
                                position: 'end'
                            }
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    grid: { color: COLORS.grid },
                    ticks: { font: { size: 10 } }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        font: { size: 9 },
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
}

function createComparisonChart() {
    const ctx = document.getElementById('comparisonChart').getContext('2d');

    comparisonChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['IFI', 'CLCR', 'TAES', 'Composite'],
            datasets: [
                {
                    label: 'Kerala',
                    data: [0.95, 0.09, 0.58, 0.95],
                    backgroundColor: 'rgba(67, 160, 71, 0.2)',
                    borderColor: COLORS.healthy,
                    borderWidth: 2,
                    pointBackgroundColor: COLORS.healthy
                },
                {
                    label: 'Meghalaya',
                    data: [0.05, 0.00, 0.00, 0.84],
                    backgroundColor: 'rgba(229, 57, 53, 0.2)',
                    borderColor: COLORS.critical,
                    borderWidth: 2,
                    pointBackgroundColor: COLORS.critical
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1,
                    ticks: { stepSize: 0.25 }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function getIFIColor(score) {
    if (score < 15) return COLORS.critical;
    if (score < 25) return COLORS.atRisk;
    if (score < 30) return COLORS.healthy;
    return COLORS.optimal;
}

function getRiskLabel(score) {
    if (score < 15) return 'Risk: 🔴 Critical';
    if (score < 25) return 'Risk: 🟡 At Risk';
    if (score < 30) return 'Risk: 🟢 Healthy';
    return 'Risk: 🔵 Optimal';
}

function addThresholdLine(chart, value, label, color) {
    const originalDraw = chart.draw;
    chart.draw = function () {
        originalDraw.apply(this, arguments);

        const ctx = this.ctx;
        const xAxis = this.scales.x;
        const yAxis = this.scales.y;

        const x = xAxis.getPixelForValue(value);

        ctx.save();
        ctx.beginPath();
        ctx.setLineDash([5, 5]);
        ctx.moveTo(x, yAxis.top);
        ctx.lineTo(x, yAxis.bottom);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = color;
        ctx.font = '11px Inter';
        ctx.textAlign = 'left';
        ctx.fillText(label, x + 5, yAxis.top + 15);

        ctx.restore();
    };
}

// =============================================================================
// ANIMATIONS
// =============================================================================

function animateKPIs() {
    animateValue('kpi-records', 0, 4.8, 1500, 'M+');
    animateValue('kpi-dbt', 0, 6000, 1500, '', '₹', ' Cr');
    animateValue('kpi-critical', 0, 8, 1000);
    animateValue('kpi-ifi', 0, 28.2, 1200, '', '', '', 1);
}

function animateValue(elementId, start, end, duration, suffix = '', prefix = '', postfix = '', decimals = 0) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Ease out quad
        const easeProgress = 1 - (1 - progress) * (1 - progress);

        const current = start + (end - start) * easeProgress;

        if (decimals > 0) {
            element.textContent = prefix + current.toFixed(decimals) + suffix + postfix;
        } else {
            element.textContent = prefix + Math.round(current).toLocaleString() + suffix + postfix;
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// =============================================================================
// INTERACTIVITY
// =============================================================================

function applyFilters() {
    const region = document.getElementById('region-filter').value;
    const risk = document.getElementById('risk-filter').value;
    const metric = document.getElementById('metric-filter').value;

    // Filter data
    let filteredIndices = stateData.labels.map((_, idx) => idx);

    if (region !== 'all') {
        const regionMap = {
            'north': 'North',
            'south': 'South',
            'east': 'East',
            'west': 'West',
            'northeast': 'Northeast',
            'central': 'Central'
        };
        filteredIndices = filteredIndices.filter(i =>
            stateData.region[i] === regionMap[region]
        );
    }

    if (risk !== 'all') {
        const riskMap = {
            'critical': 'Critical',
            'at-risk': 'At Risk',
            'healthy': 'Healthy',
            'optimal': 'Optimal'
        };
        filteredIndices = filteredIndices.filter(i =>
            stateData.risk[i] === riskMap[risk]
        );
    }

    // Update IFI chart with filtered data
    updateIFIChart(filteredIndices, metric);

    // Show feedback
    showFilterFeedback(filteredIndices.length);
}

function updateIFIChart(indices, metric) {
    const metricData = {
        'ifi': stateData.ifi,
        'clcr': stateData.clcr.map(v => v * 100), // Scale for visibility
        'taes': stateData.taes.map(v => v * 100),
        'composite': stateData.composite.map(v => v * 100)
    };

    const data = metricData[metric];
    const sortedIndices = indices.sort((a, b) => data[a] - data[b]);

    const newLabels = sortedIndices.map(i => stateData.labels[i]).slice(0, 15);
    const newData = sortedIndices.map(i => data[i]).slice(0, 15);
    const newColors = newData.map(v => getIFIColor(metric === 'ifi' ? v : v / 100 * 35));

    ifiChart.data.labels = newLabels;
    ifiChart.data.datasets[0].data = newData;
    ifiChart.data.datasets[0].backgroundColor = newColors;
    ifiChart.data.datasets[0].label = metric.toUpperCase() + ' Score';
    ifiChart.update('active');
}

function showFilterFeedback(count) {
    // Simple visual feedback
    const kpiCards = document.querySelectorAll('.kpi-card');
    kpiCards.forEach(card => {
        card.style.transition = 'transform 0.3s';
        card.style.transform = 'scale(0.98)';
        setTimeout(() => {
            card.style.transform = 'scale(1)';
        }, 150);
    });
}

function compareStates() {
    const state1 = document.getElementById('state1-select').value;
    const state2 = document.getElementById('state2-select').value;

    const stateNames = {
        'kerala': 'Kerala',
        'tamil-nadu': 'Tamil Nadu',
        'maharashtra': 'Maharashtra',
        'uttar-pradesh': 'Uttar Pradesh',
        'meghalaya': 'Meghalaya',
        'assam': 'Assam',
        'bihar': 'Bihar'
    };

    const getStateData = (stateName) => {
        const idx = stateData.labels.findIndex(l =>
            l.toLowerCase().replace(/ /g, '-') === stateName ||
            l.toLowerCase() === stateName.replace(/-/g, ' ')
        );

        if (idx === -1) {
            return [0.5, 0.5, 0.5, 0.5];
        }

        return [
            stateData.ifi[idx] / 35, // Normalize to 0-1
            stateData.clcr[idx],
            stateData.taes[idx],
            stateData.composite[idx]
        ];
    };

    comparisonChart.data.datasets[0].label = stateNames[state1] || state1;
    comparisonChart.data.datasets[0].data = getStateData(state1);

    comparisonChart.data.datasets[1].label = stateNames[state2] || state2;
    comparisonChart.data.datasets[1].data = getStateData(state2);

    comparisonChart.update();
}

function downloadChart(chartId) {
    const chart = document.getElementById(chartId);
    if (!chart) return;

    const link = document.createElement('a');
    link.download = chartId + '_chart.png';
    link.href = chart.toDataURL('image/png');
    link.click();
}

function toggleFullscreen(chartId) {
    const chartCard = document.getElementById(chartId).closest('.chart-card');
    if (!chartCard) return;

    if (!document.fullscreenElement) {
        chartCard.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

// =============================================================================
// DATA EXPORT
// =============================================================================

function exportData() {
    const csvContent = "data:text/csv;charset=utf-8," +
        "State,IFI,CLCR,TAES,Composite,Region,Risk\n" +
        stateData.labels.map((label, i) =>
            `${label},${stateData.ifi[i]},${stateData.clcr[i]},${stateData.taes[i]},${stateData.composite[i]},${stateData.region[i]},${stateData.risk[i]}`
        ).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "uidai_state_metrics.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Make exportData available globally
window.exportData = exportData;
