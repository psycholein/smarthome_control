var Highchart = {
  setup: function(data, ele) {
    if (data.length == 0) return;
    Highchart.timezone();
    var result = {};
    $.each(data, function(i, value) {
      if ($.inArray(value.typ, Highchart.temperature) >= 0) {
        if (!result[value.typ]) {
          result[value.typ] = {
            name: value.typ,
            yAxis: 0,
            tooltip: {
                valueSuffix: ' °C'
            },
            data: []
          };
        }
      } else if ($.inArray(value.typ, Highchart.humidity) >= 0) {
        if (!result[value.typ]) {
          result[value.typ] = {
            name: value.typ,
            type: 'column',
            yAxis: 1,
            tooltip: {
                valueSuffix: ' %'
            },
            data: []
          };
        }
      } else return;
      result[value.typ].data.push([Math.round(value.timestamp*1000), parseFloat(value.value)]);
    });

    var series = [];
    $.each(result, function(i, value) {
      series.push(value);
    });
    var chart = {
      series: series,
      title: { text: data[0].collection+' ('+data[0].category+')' }
    };
    ele.highcharts($.extend(Highchart.base, chart)).show();
  },

  temperature: ['temperature', 'measured-temp', 'desired-temp'],
  humidity: ['humidity'],
  base: {
    chart: {
      type: 'line'
    },
    xAxis: {
      type: 'datetime',
      dateTimeLabelFormats: {
        month: '%e. %b',
        year: '%b'
      },
      title: {
        text: 'Date'
      }
    },
    yAxis: [{
      title: {
        text: 'Temperature',
        style: { color: Highcharts.getOptions().colors[2] }
      },
      labels: {
        format: '{value}°C',
        style: { color: Highcharts.getOptions().colors[2] }
      },
      opposite: true
    }, {
      title: {
        text: 'Humidity',
        style: { color: Highcharts.getOptions().colors[0] }
      },
      labels: {
        format: '{value} %',
        style: { color: Highcharts.getOptions().colors[0] }
      }
    }],
    tooltip: {
      shared: true
    },
    series: []
  },

  timezone: function() {
    var d = new Date();
    var t = d.getTimezoneOffset();
    Highcharts.setOptions({
      global: {
        timezoneOffset: t
      }
    });
  }
};
