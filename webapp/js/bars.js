server_ip = ""
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var canvas = document.getElementById('umidade');
var ctx = canvas.getContext('2d');
var startingData = {
  labels: [],
  datasets: [{
    label: "Humidity",
    backgroundColor: "rgba(2,117,216,0.2)",
    borderColor: "rgba(2,117,216,1)",
    pointBackgroundColor: "rgba(2,117,216,1)",
    pointBorderColor: "#fff",
    pointHoverBackgroundColor: "#fff",
    pointHoverBorderColor: "rgba(2,117,216,1)",
    data: []
  }]
};
var latestLabel = null;

var myLineChart = new Chart(ctx, {
  type: 'line',
  data: startingData,
  options: {
    scales: {
      x: {
        time: {
          unit: 'month'
        },
        grid: {
          display: false
        },
        ticks: {
          maxTicksLimit: 6
        }
      },
      y: {
        ticks: {
          min: 0,
          max: 1,
          maxTicksLimit: 5,
          callback: function(value) {
            return (value * 100).toFixed(0) + '%';
          }
        },
        grid: {
          display: true
        }
      }
    },
    plugins: {
      legend: {
        display: false
      }
    },
    animation: {
      duration: 0
    }
  }
});

async function fetchApiData(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
}

async function update_line() {
  const rvalue = await fetchApiData('http://192.168.0.19:8000/get_humidity?all=true&separated=true');
  const values = rvalue.values.slice(-20);
  const labels = rvalue.labels.map(x => x.split(' ').slice(3).join(':')).slice(-20);
  const latestLabelIndex = labels.length - 1;

  if (latestLabel === null || labels[latestLabelIndex] !== latestLabel) {
    if (latestLabel === null) {
      // Initialize the chart with the first set of data
      myLineChart.data.labels = labels;
      myLineChart.data.datasets[0].data = values;
    } else {
      // Add new data to the chart
      myLineChart.data.labels.push(labels[latestLabelIndex]);
      myLineChart.data.datasets[0].data.push(values[latestLabelIndex]);
    }

    latestLabel = labels[latestLabelIndex];
    myLineChart.update();
  }
}

async function update_values() {
  const values = await fetchApiData('http://192.168.0.19:8000/get_humidity?index=-1&separated=true');
  document.getElementById("humidity_value").innerHTML = `${(values.values[0] * 100).toFixed(2)}%`;
}

setInterval(update_values, 500);
setInterval(update_line, 500);
