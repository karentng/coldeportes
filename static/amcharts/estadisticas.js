var colores = ["#67b7dc", "#fdd400", "#84b761", "#cc4748", "#cd82ad", "#2f4074", "#448e4d", "#b7b83f", "#b9783f", "#b93e3d", "#913167"];

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


//FUNCIÓN AUXILIAR PARA VALIDAR EL NO_DATA EN LOS ARCHIVOS GENERADOS POR LA FUNCIÓN SUMAR_DATOS_INICIALES DE PYTHON
function valoresEnCero(datos){
    for(i=0;i<datos.length;i++){
        if(datos[i].valor){
            return false;
        }
    }
    return true;
}


AmCharts.checkEmptyData = function (chart) {
    console.log(valoresEnCero(chart.dataProvider));
    if ( 0 == chart.dataProvider.length || valoresEnCero(chart.dataProvider)) {
        // set min/max on the value axis
        try{
            chart.valueAxes[0].minimum = 0;
            chart.valueAxes[0].maximum = 100;
        }catch(e){

        }
        // add dummy data point
        var dataPoint = {
            dummyValue: 0
        };
        dataPoint[chart.categoryField] = '';
        chart.dataProvider = [dataPoint];
        
        // add label
        chart.addLabel(0, '50%', 'No hay datos para el reporte especificado', 'center', 19, "#00acac");
        
        // set opacity of the chart div
        chart.chartDiv.style.opacity = 0.75;
        
    }else{
        chart.allLabels = [];
    }
    chart.validateNow();
}


function ClaseReportes(){
    /* Generar las gráficas */
    function generarComparativa(datos, nombreDiv, nombreGrafica){
        chart = new AmCharts.AmSerialChart(AmCharts.themes.light);
        chart.theme = AmCharts.themes.light;
        chart.dataProvider = datos;
        chart.categoryField = "descripcion";
        chart.startDuration = 0.5;
        chart.balloon.color = "#000000";
        chart.titles = [{
            "text": nombreGrafica,
            "size": 16
        }];
    
        // AXES
        // category
        var categoryAxis = chart.categoryAxis;
        categoryAxis.fillAlpha = 1;
        categoryAxis.fillColor = "#FAFAFA";
        categoryAxis.gridAlpha = 0;
        categoryAxis.axisAlpha = 0;
        categoryAxis.gridPosition = "start";
        categoryAxis.position = "bottom";
        categoryAxis.labelRotation = 45;
        categoryAxis.labelFunction =  function(label) {
                                      label = label.replace(/(.{5}[ ])/g, "$1\n");
                                      return label;
                                    }
    
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

        chart.exportConfig = exportConfig();
    
        // WRITE
        chart.write(nombreDiv);
        charts.push([chart, nombreDiv]);
    }
    function generarTorta(datos, nombreDiv, nombreGrafica){
        chart = new AmCharts.AmPieChart(AmCharts.themes.light);
        chart.theme = AmCharts.themes.light;
        chart.titles = [{
            "text": nombreGrafica,
            "size": 16
        }];
        chart.dataProvider = datos;
        chart.titleField = "descripcion";
        chart.valueField = "valor";
        chart.outlineColor = "#FFFFFF";
        chart.innerRadius = "60%";
        chart.labelRadius = 15;
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

    function generarComparativaVertical(datos, nombreDiv, nombreGrafica){
        chart = new AmCharts.AmSerialChart(AmCharts.themes.light);
        chart.theme = AmCharts.themes.light;
        chart.dataProvider = datos;
        chart.titles = [{
            "text": nombreGrafica,
            "size": 16
        }];
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

    //Función para generar un gráfico de cilindro 3D
    function generarGraficoCilindros(datos, nombreDiv, nombreGrafica){
        chart = new AmCharts.AmSerialChart(AmCharts.themes.light);
        chart.theme = AmCharts.themes.light;
        chart.dataProvider = datos;
        chart.titles = [{
            "text": nombreGrafica,
            "size": 16
        }];
        chart.depth3D = 40;
        chart.angle = 30;

        chart.categoryField = "descripcion";
        chart.startDuration = 2;
        chart.plotAreaBorderColor = "#DADADA";
        chart.plotAreaBorderAlpha = 1;

        // AXES
        // Category
        var categoryAxis = chart.categoryAxis;
        categoryAxis.gridPosition = "start";
        categoryAxis.gridAlpha = 0;
        categoryAxis.axisAlpha = 0;
        categoryAxis.labelRotation = 45;
        categoryAxis.labelFunction =  function(label) {
                                      label = label.replace(/(.{5}[ ])/g, "$1\n");
                                      return label;
                                    }

        // Value
        var valueAxis = new AmCharts.ValueAxis();
        valueAxis.axisAlpha = 0;
        valueAxis.gridAlpha = 0;
        valueAxis.position = "left";
        chart.addValueAxis(valueAxis);

        // GRAPHS
        // first graph
        var graph1 = new AmCharts.AmGraph();
        graph1.type = "column";
        graph1.title = nombreGrafica;
        graph1.valueField = "valor";
        graph1.balloonText = "<b>[[category]]</b>: ([[value]])";
        graph1.lineAlpha = 0.1;
        graph1.fillAlphas = 0.85;
        graph1.colorField = "color";
        graph1.topRadius = 1;
        chart.addGraph(graph1);

        chart.creditsPosition = "top-right";

        chart.exportConfig = exportConfig();

        // WRITE
        chart.write(nombreDiv);
        charts.push([chart, nombreDiv]);
    }

    //Función para generar un gráfico de cono 3D
    function generarGraficoCono(datos, nombreDiv, nombreGrafica){
        chart = new AmCharts.AmFunnelChart(AmCharts.themes.light);
        chart.theme = AmCharts.themes.light;
        chart.dataProvider = datos;
        chart.titles = [{
            "text": nombreGrafica,
            "size": 16
        }];
        chart.valueField = "valor";
        chart.titleField = "descripcion";
        chart.marginRight = 240;
        chart.marginLeft = 50;
        chart.startX = -500;
        chart.depth3D = 100;
        chart.angle = 40;
        chart.outlineAlpha = 1;
        chart.outlineColor = "#FFFFFF";
        chart.outlineThickness = 2;
        chart.labelPosition = "right";
        chart.balloonText = "<b>[[descripcion]]</b>: [[valor]]";
        chart.exportConfig = exportConfig();

        // WRITE
        chart.write(nombreDiv);
        charts.push([chart, nombreDiv]);
    }

    //Función para generar un gráfico de radar
    function generarGraficoRadar(datos, nombreDiv, nombreGrafica){
        chart = new AmCharts.AmRadarChart(AmCharts.themes.light);
        chart.theme = AmCharts.themes.light;
        chart.dataProvider = datos;
        chart.titles = [{
            "text": nombreGrafica,
            "size": 16
        }];

        // Value
        var valueAxis = new AmCharts.ValueAxis();
        valueAxis.axisAlpha = 0;
        valueAxis.axisTitleOffset = 20;
        valueAxis.minimum = 0;
        chart.addValueAxis(valueAxis);
        chart.exportConfig = exportConfig();

        // GRAPHS
        // first graph
        var graph1 = new AmCharts.AmGraph();
        graph1.valueField = "valor";
        graph1.balloonText = "<b>[[category]]</b>: ([[value]])";
        graph1.bullet = "round";
        chart.addGraph(graph1);

        chart.categoryField = "descripcion"

        // WRITE
        chart.write(nombreDiv);
        charts.push([chart, nombreDiv]);
    }

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
    function torta(resultado, nombreDiv, nombreGrafica){
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
        if (AmCharts.isReady){
            generarTorta(datos, nombreDiv, nombreGrafica);
        }else{
            AmCharts.ready(generarTorta(datos, nombreDiv, nombreGrafica));
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
            generarComparativa(datos, nombreDiv, nombreGrafica);
        }else{
            AmCharts.ready(generarComparativa(datos, nombreDiv, nombreGrafica));
        }
    }

    function comparativaVertical(resultado, nombreDiv, nombreGrafica){
        var chart2;
        var datos = [];
        var cont = 0;
        for (i in resultado){
            var aux = resultado[i];
            datos.push(
                {
                    'descripcion': i,
                    'valor': aux,
                    'color': colores[Math.floor(Math.random()*(colores.length+1))],
                }
            );
            cont += 1;
        }

        if (AmCharts.isReady){
            generarComparativaVertical(datos, nombreDiv, nombreGrafica);
        }else{
            AmCharts.ready(generarComparativaVertical(datos, nombreDiv, nombreGrafica));
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

    function cilindros(resultado, nombreDiv,nombreGrafica){
        var datos = [];
        for (i in resultado){
            var aux = resultado[i];
            datos.push(
                {
                    'descripcion': i,
                    'valor': aux,
                    'color': colores[Math.floor(Math.random()*(colores.length+1))]
                }
            );
        }

        if (AmCharts.isReady){
            generarGraficoCilindros(datos, nombreDiv, nombreGrafica);
        }else{
            AmCharts.ready(generarGraficoCilindros(datos, nombreDiv, nombreGrafica));
        }
    }

    function cono(resultado, nombreDiv, nombreGrafica){
        var datos = [];
        for (i in resultado){
            var aux = resultado[i];
            datos.push(
                {
                    'descripcion': i,
                    'valor': aux
                }
            );
        }

        if (AmCharts.isReady){
            generarGraficoCono(datos, nombreDiv, nombreGrafica);
        }else{
            AmCharts.ready(generarGraficoCono(datos, nombreDiv, nombreGrafica));
        }
    }

    function radar(resultado, nombreDiv, nombreGrafica){
        var datos = [];
        for (i in resultado){
            var aux = resultado[i];
            datos.push(
                {
                    'descripcion': i,
                    'valor': aux
                }
            );
        }

        if (AmCharts.isReady){
            generarGraficoRadar(datos, nombreDiv, nombreGrafica);
        }else{
            AmCharts.ready(generarGraficoRadar(datos, nombreDiv, nombreGrafica));
        }
    }


    return {
        crearGrafico: function(resultado, grafico, nombreDiv, nombreGrafica){
            //resultado = obtenerResultado(resultado);
            switch(grafico){
                case 1:
                    torta(resultado, nombreDiv, nombreGrafica);
                    break;
                case 2:
                    comparativa(resultado, nombreDiv, nombreGrafica);
                    break;
                case 3:
                    comparativaVertical(resultado, nombreDiv, nombreGrafica);
                    break;
                case 4:
                    //treeMap(resultado, nombreDiv, true);
                    ZoomableTreeMap(resultado, nombreDiv, true);
                    break;
                case 5:
                    cilindros(resultado, nombreDiv, nombreGrafica);
                    break;
                case 6:
                    cono(resultado, nombreDiv, nombreGrafica);
                    break;
                case 7:
                    radar(resultado, nombreDiv, nombreGrafica);
                    break;
            }
            AmCharts.checkEmptyData(charts[charts.length-1][0]);
        },

        modificarDatos: function(datos, nombreNuevoReporte){
            var nuevosDatos = [];
            var cont = 0;
            for (i in datos){
                var aux = datos[i];
                nuevosDatos.push(
                    {
                        'descripcion': i,
                        'valor': aux,
                        'color': colores[Math.floor(Math.random()*(colores.length+1))]
                    }
                );
                cont += 1;
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
                    chartSeleccionado.titles = [{
                        "text": nombreNuevoReporte,
                        "size": 16
                    }];
                    chartSeleccionado.validateData();
                    chartSeleccionado.animateAgain();
                    AmCharts.checkEmptyData(chartSeleccionado);
                }
            }
        },

        obtenerResultadoDeJson: function(r){
            return obtenerResultado(r);
        }
    }
}