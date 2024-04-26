const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['2020','2021', '2022', '2023', '2024'],
    datasets: [{
      label: '# of Votes',
      
      data: [0,100,200,300,400],
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

