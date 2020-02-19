var chart, chart1, chart2;
var control;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function control() {
    $.ajax({
        url: '/control_motor',
        success: function() {
            // call it again after one second
            setTimeout(control(), 8000);
        },
        cache: false
    });
}
function act_wheels() {
    $.ajax({
        url: '/act_wheels',
        success: function() {
            // call it again after one second
            setTimeout(control(), 100000);
        },
        cache: false
    });
}
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}
function requestData2() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart1.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart1.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestData, 10000);
        },
        cache: false
    });
}
function requestData3() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart2.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart2.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    control()
    act_wheels = act_wheels()
    if act_wheels[0] = 1{
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'data-container',
                defaultSeriesType: 'spline',
                events: {
                    load: requestData
                }
            },
            title: {
                text: 'Pressure"
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 20 * 1000
            },
            yAxis: {
                minPadding: 0.2,
                maxPadding: 0.2,
                title: {
                    text: 'Value',
                    margin: 80
                }
            },
            series: [{
                name: 'Random data',
                data: []
            }]
        });
    }
    if act_wheels[1] = 1
        chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'data-container2',
                defaultSeriesType: 'spline',
                events: {
                    load: requestData2
                }
            },
            title: {
                text: 'Live random data'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 20 * 1000
            },
            yAxis: {
                minPadding: 0.2,
                maxPadding: 0.2,
                title: {
                    text: 'Value',
                    margin: 80
                }
            },
            series: [{
                name: 'Random data',
                data: []
            }]
        });
    }
    if act_wheels[2] = 1
        chart2 = new Highcharts.Chart({
            chart: {
                renderTo: 'data-container3',
                defaultSeriesType: 'spline',
                events: {
                    load: requestData3
                }
            },
            title: {
                text: 'Pressure Reading'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 20 * 1000
            },
            yAxis: {
                minPadding: 0.2,
                maxPadding: 0.2,
                title: {
                    text: 'Value',
                    margin: 80
                }
            },
            series: [{
                name: 'Random data',
                data: []
            }]
        });
    }
});