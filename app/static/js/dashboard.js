// SECUREVISION — Dashboard JS (Chart.js) — Light Theme

document.addEventListener('DOMContentLoaded', function() {
    if (typeof Chart === 'undefined') return;

    // Read chart data from embedded JSON block
    const dataEl = document.getElementById('chart-data');
    if (!dataEl) return;
    const chartData = JSON.parse(dataEl.textContent);
    const chartLabels = chartData.labels;
    const chartSuccess = chartData.success;
    const chartFailed = chartData.failed;
    const totalSuccess = chartData.totalSuccess;
    const totalFailed = chartData.totalFailed;

    // Auth Activity Chart
    const authCtx = document.getElementById('authChart');
    if (authCtx) {
        new Chart(authCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: chartLabels,
                datasets: [
                    {
                        label: 'Successful',
                        data: chartSuccess,
                        backgroundColor: 'rgba(107, 158, 107, 0.6)',
                        borderColor: 'rgba(107, 158, 107, 1)',
                        borderWidth: 1,
                        borderRadius: 6
                    },
                    {
                        label: 'Failed',
                        data: chartFailed,
                        backgroundColor: 'rgba(196, 112, 112, 0.6)',
                        borderColor: 'rgba(196, 112, 112, 1)',
                        borderWidth: 1,
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#5A5A5A', font: { family: 'Inter' } }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#8A8A8A' },
                        grid: { color: 'rgba(28, 28, 28, 0.06)' }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#8A8A8A', stepSize: 1 },
                        grid: { color: 'rgba(28, 28, 28, 0.06)' }
                    }
                }
            }
        });
    }

    // Status Distribution Chart
    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        new Chart(statusCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Successful', 'Failed'],
                datasets: [{
                    data: [totalSuccess, totalFailed],
                    backgroundColor: ['rgba(107, 158, 107, 0.7)', 'rgba(196, 112, 112, 0.7)'],
                    borderColor: ['rgba(107, 158, 107, 1)', 'rgba(196, 112, 112, 1)'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#5A5A5A', font: { family: 'Inter' }, padding: 16 }
                    }
                },
                cutout: '65%'
            }
        });
    }
});
