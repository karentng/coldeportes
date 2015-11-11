var colores = [
    "#FF0F00",
    "#FF6600",
    "#FF9E01",
    "#FCD202",
    "#F8FF01",
    "#B0DE09",
    "#04D215",
    "#0D8ECF",
    "#0D52D1",
    "#2A0CD0",
];

var charts = []; // [chart, nombreDiv]

function tamanoAmcharts(){
    for (i in charts){
        try{
            charts[i][0].invalidateSize();
        }catch(err){
            // Es el tree map
        }
    }
}

$(".nav a").on("shown.bs.tab", function () {
    tamanoAmcharts();
});

function Reportes(){
    /* Generar las gráficas */
    function generarComparativa(datos, nombreDiv){
        chart = new AmCharts.AmSerialChart();
        chart.dataProvider = datos;
        chart.categoryField = "descripcion";
        chart.startDuration = 0.5;
        chart.balloon.color = "#000000";
    
        // AXES
        // category
        var categoryAxis = chart.categoryAxis;
        categoryAxis.fillAlpha = 1;
        categoryAxis.fillColor = "#FAFAFA";
        categoryAxis.gridAlpha = 0;
        categoryAxis.axisAlpha = 0;
        categoryAxis.gridPosition = "start";
        categoryAxis.position = "bottom";
    
        // value
        var valueAxis = new AmCharts.ValueAxis();
        valueAxis.title = "Cantidad";
        valueAxis.dashLength = 5;
        valueAxis.axisAlpha = 0;
        valueAxis.minimum = 0;
        valueAxis.integersOnly = true;
        valueAxis.gridCount = 10;
        valueAxis.reversed = false; // this line makes the value axis reversed

        chart.addValueAxis(valueAxis);
    
        // Germany graph
        var graph = new AmCharts.AmGraph();
        graph.valueField = "valor";
        graph.balloonText = "[[category]] ([[value]])";
        graph.bullet = "round";
        chart.addGraph(graph);
        
        // CURSOR
        var chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chartCursor.zoomable = false;
        chartCursor.cursorAlpha = 0;
        chart.addChartCursor(chartCursor);                
    
        // LEGEND
        var legend = new AmCharts.AmLegend();
        legend.useGraphSettings = true;
        chart.addLegend(legend);

        chart.exportConfig = exportConfig();
    
        // WRITE
        chart.write(nombreDiv);
        charts.push([chart, nombreDiv]);
    }
    function generarTorta(datos, nombreDiv){
        chart = new AmCharts.AmPieChart();
        chart.dataProvider = datos;
        chart.titleField = "descripcion";
        chart.valueField = "valor";
        chart.outlineColor = "#FFFFFF";
        chart.innerRadius = "60%";
        chart.outlineAlpha = 0.8;
        chart.outlineThickness = 2;
        chart.balloonText = "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>";
        // this makes the chart 3D
        chart.depth3D = 15;
        chart.angle = 30;
        chart.exportConfig = exportConfig();

        // WRITE
        chart.write(nombreDiv);
        charts.push([chart, nombreDiv]);
    }

    function generarComparativaVertical(datos, nombreDiv){
        chart = new AmCharts.AmSerialChart();
        chart.dataProvider = datos;
        
        chart.depth3D = 20;
        chart.angle = 30;
        chart.rotate = true;

        chart.categoryField = "descripcion";
        chart.startDuration = 1;
        chart.plotAreaBorderColor = "#DADADA";
        chart.plotAreaBorderAlpha = 1;
        // this single line makes the chart a bar chart
        chart.rotate = true;

        // AXES
        // Category
        var categoryAxis = chart.categoryAxis;
        categoryAxis.gridPosition = "start";
        categoryAxis.gridAlpha = 0.1;
        categoryAxis.axisAlpha = 0;

        // Value
        var valueAxis = new AmCharts.ValueAxis();
        valueAxis.axisAlpha = 0;
        valueAxis.gridAlpha = 0.1;
        valueAxis.position = "top";
        chart.addValueAxis(valueAxis);

        // GRAPHS
        // first graph
        var graph1 = new AmCharts.AmGraph();
        graph1.type = "column";
        graph1.title = "Descripción";
        graph1.valueField = "valor";
        graph1.balloonText = "[[category]] ([[value]])";
        graph1.lineAlpha = 0;
        graph1.fillAlphas = 1;
        graph1.colorField = "color";
        chart.addGraph(graph1);

        // LEGEND
        var legend = new AmCharts.AmLegend();
        chart.addLegend(legend);

        chart.creditsPosition = "top-right";

        chart.exportConfig = exportConfig();

        // WRITE
        chart.write(nombreDiv);
        charts.push([chart, nombreDiv]);
    }

    /* Tree Map */
    function ZoomableTreeMap(datos, nombreDiv, agregar) {
        var $container = $('#'+nombreDiv),
            w = $("#contenido").width(),
            h = 500, //$("#contenido").height(),
            x = d3.scale.linear().range([0, w]),
            y = d3.scale.linear().range([0, h]),
            root,
            node;
        var opacity = 1;

        var treemap = d3.layout.treemap()
            .round(false)
            .size([w, h])
            .sticky(true)
            .value(function (d) {
                return d.size;
            });

            var svg = d3.select('#'+nombreDiv).append("div")
            .attr('id', 'my-svg-div')
            .attr("class", "chart")
            .style("width", w + "px")
            .style("height", h + "px")
            .append("svg:svg")
            .attr("width", w)
            .attr("height", h)
            .append("svg:g")
            .attr("transform", "translate(.5,.5)");
            
            var data = {
                "name": "Tree Map",
                "children": []
            };
            for (i in datos){
                var aux = datos[i];
                data['children'].push({
                    "name": aux[0],
                    "children": [{
                        "name": i,
                        "size": aux,
                    }]
                    
                });
            }

            node = root = data;

            var nodes = treemap.nodes(root)
                .filter(function (d) {
                    return !d.children;
                });

            function codname(d){
                if(d.name=="Other") return codname(d.parent)+" - other";
                return d.name;
            }
            var cell = svg.selectAll("g")
                .data(nodes)
                .enter().append("svg:g")
                .attr("class", "cell")
                .attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")";
                })
                .on("click", function (d) {
                    return zoom(node === d.parent ? root : d.parent);
                });



            cell.append("svg:rect")
                .attr("width", function (d) {

                    return d.dx - 1;
                })
                .attr("height", function (d) {
                    return d.dy - 1;
                })
                .style({
                    "fill": "#6b6ecf", "opacity": function (d) {
                        opacity -= 0.09;
                        return (opacity);
                    }
                });

            cell.append("svg:text")
                .attr("x", function (d) {
                    return d.dx / 2;
                })
                .attr("y", function (d) {
                    return d.dy / 2;
                })

                .attr("text-anchor", "middle")
                .text(function (d) {
                    return d.parent['name'];
                })
                .style("opacity", function (d) {
                    d.w = this.getComputedTextLength();
                    return d.dx > d.w ? 1 : 0;
                });

            d3.select(window).on("click", function () {
                zoom(root);
            });

            d3.select("select").on("change", function () {
                treemap.value(this.value === "size" ? size : count).nodes(root);
                zoom(node);
            });
        

        function size(d) {
            return d.size;
        }

        function count(d) {
            return 1;
        }

        function zoom(d) {
            var kx = w / d.dx, ky = h / d.dy;
            x.domain([d.x, d.x + d.dx]);
            y.domain([d.y, d.y + d.dy]);
            var nodeCurr = d;
            var t = svg.selectAll("g.cell").transition()
                            .duration(750)
                            .attr("transform", function (d) {
                                return "translate(" + x(d.x) + "," + y(d.y) + ")";
                            });

            t.select("rect")
                            .attr("width", function (d) {
                                return kx * d.dx - 1;
                            })
                            .attr("height", function (d) {
                                return ky * d.dy - 1;
                            })

            t.select("text")
                            .attr("x", function (d) {
                                return kx * d.dx / 2;
                            })
                            .attr("y", function (d) {
                                return ky * d.dy / 2;
                            })
                            .text(function (d) {
                                var text = nodeCurr.depth > 0 ? d.name : d.parent['name'];
                                return text;
                            })
                            .style("opacity", function (d) {
                                return kx * d.dx > d.w ? 1 : 0;
                            });

            node = d;
            d3.event.stopPropagation();
        }
        if(agregar){
            charts.push(["treeMap", nombreDiv]);    
        }
    }

    /* Fin Tree Map */

    var exportConfig = function(){
        return {
            menuTop: "0px",
            menuBottom: "auto",
            menuRight: "0px",
            backgroundColor: "#efefef",
            menuItemStyle: {
                backgroundColor: '#EFEFEF',
                rollOverBackgroundColor: '#DDDDDD'
            },
            menuItems: [{
                textAlign: 'center',
                icon: base+"amcharts/images/export.png",
                onclick: function() {
                },
                items: [{
                        title: 'JPG',
                        format: 'jpg'
                    }, {
                        title: 'PNG',
                        format: 'png'
                    }, {
                        title: 'SVG',
                        format: 'svg'
                    }]
            }]
        }
    }

    var obtenerResultado = function(r){
        var r = ((r).replace(/&(l|g|quo)t;/g, function(a,b){
            return {
                l   : '<',
                g   : '>',
                quo : '"'
            }[b];
        }));
        return JSON.parse(r);
    }

    // Gráficas
    function torta(resultado, nombreDiv){
        var datos = [];
        for (i in resultado){
            var aux = resultado[i];
            datos.push(
                {
                    'descripcion': i,
                    'valor': aux,
                }
            );
        }
        
        var chart;
        var legend;

        if (AmCharts.isReady){
            generarTorta(datos, nombreDiv);
        }else{
            AmCharts.ready(generarTorta(datos, nombreDiv));
        }
    }

    function comparativa(resultado, nombreDiv, nombreGrafica){
        var chart2;
        var datos = [];
        for (i in resultado){
            var aux = resultado[i];
            datos.push(
                {
                    'descripcion': i,
                    'valor': aux,
                }
            );
        }
            
        if (AmCharts.isReady){
            generarComparativa(datos, nombreDiv);
        }else{
            AmCharts.ready(generarComparativa(datos, nombreDiv));
        }
    }

    function comparativaVertical(resultado, nombreDiv){
        var chart2;
        var datos = [];
        for (i in resultado){
            var aux = resultado[i];
            datos.push(
                {
                    'descripcion': i,
                    'valor': aux,
                    'color': colores[aux%colores.length],
                }
            );
        }

        if (AmCharts.isReady){
            generarComparativaVertical(datos, nombreDiv);
        }else{
            AmCharts.ready(generarComparativaVertical(datos, nombreDiv));
        }
    }

    function treeMap(resultado, nombreDiv, agregar) {
        var datos = [];
        for (i in resultado) {
            var aux = resultado[i];
            datos.push({
                "name": i,
                "value": aux,
            });
        }

        d3plus.viz()
            .container("#" + nombreDiv)
            .data(datos)
            .type("tree_map")
            .id("name")
            .color("name")
            .size("value")
            .labels({"valign": "top",})
            .draw();

        if (agregar) {
            charts.push(["treeMap", nombreDiv]);
        }
    }


    return {
        crearGrafico: function(resultado, grafico, nombreDiv, nombreGrafica){
            //resultado = obtenerResultado(resultado);
            switch(grafico){
                case 1:
                    torta(resultado, nombreDiv);
                    break;
                case 2:
                    comparativa(resultado, nombreDiv, nombreGrafica);
                    break;
                case 3:
                    comparativaVertical(resultado, nombreDiv);
                    break;
                case 4:
                    //treeMap(resultado, nombreDiv, true);
                    ZoomableTreeMap(resultado, nombreDiv, true);
                    break;
            }
        },

        modificarDatos: function(datos){
            var nuevosDatos = [];
            for (i in datos){
                var aux = datos[i];
                nuevosDatos.push(
                    {
                        'descripcion': i,
                        'valor': aux,
                        'color': colores[aux%colores.length],
                    }
                );
            }
            
            for(i in charts){
                var chartSeleccionado = charts[i][0];
                var div = charts[i][1];

                if(chartSeleccionado == 'treeMap'){
                    //treeMap(datos, div, false);
                    $("#"+div).html("");
                    if(datos.length == 0){
                        $("#"+div).html("No hay datos disponibles");
                    }else{
                        ZoomableTreeMap(datos, div, false);
                    }
                }else{
                    chartSeleccionado.dataProvider = nuevosDatos;
                    chartSeleccionado.validateData();
                    chartSeleccionado.animateAgain();
                }
            }
        },

        obtenerResultadoDeJson: function(r){
            return obtenerResultado(r);
        }
    }
}