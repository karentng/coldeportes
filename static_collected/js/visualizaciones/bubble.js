/*Permite dibujar un Bubble Chart
Parámetros: $datos: matriz donde están los datos, la primera fila es el nombre de las columnas*/
google.load("visualization", "1", {packages:["corechart"]});
function bubble($columnas, $datos, $titulo, $div){
google.setOnLoadCallback(drawSeriesChart);
function drawSeriesChart(){
    var data = new google.visualization.DataTable();
    for (var i=0;i<$columnas.length;i++){
        $col = $columnas[i].split(':');
        data.addColumn($col[1],$col[0]);
    }
    data.addRows($datos);
    var options = {
        title: $titulo,
        hAxis: {title: $datos[0][1]},
        vAxis: {title: $datos[0][2]},
        bubble: {textStyle: {fontSize: 11}}
    };

    var chart = new google.visualization.BubbleChart(document.getElementById($div));
    chart.draw(data, options);
}
}

