/**
 * Created by juandgc on 16/03/16.
 */
$(document).ready(function(){
    var chart;


    AmCharts.ready(function () {
        // SERIAL CHART
        chart = new AmCharts.AmSerialChart();
        chart.dataProvider = chartData;
        chart.categoryField = "titulo";
        // the following two lines makes chart 3D
        chart.depth3D = 20;
        chart.angle = 30;

        // AXES
        // category
        var categoryAxis = chart.categoryAxis;
        categoryAxis.labelRotation = 45;
        categoryAxis.gridPosition = "start";

        // value
        var valueAxis = new AmCharts.ValueAxis();
        valueAxis.title = "Cantidad Participantes";
        chart.addValueAxis(valueAxis);

        // GRAPH
        var graph = new AmCharts.AmGraph();
        graph.valueField = "valor";
        graph.colorField = "color";
        graph.balloonText = "<span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>";
        graph.type = "column";
        graph.lineAlpha = 0;
        graph.fillAlphas = 1;
        chart.addGraph(graph);

        // CURSOR
        var chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorAlpha = 0;
        chartCursor.zoomable = false;
        chartCursor.categoryBalloonEnabled = false;
        chart.addChartCursor(chartCursor);

        chart.creditsPosition = "top-right";

        // WRITE
        chart.write("chartdiv");
    });
});
