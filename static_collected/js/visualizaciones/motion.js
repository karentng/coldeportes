google.load("visualization", "1", {packages:["motionchart"]});
function motion($columnas,$datos,$div){
    google.setOnLoadCallback(drawChart);
    function drawChart(){
      var data = new google.visualization.DataTable();
      for (var i=0;i<$columnas.length;i++){
        $col = $columnas[i].split(':');
        data.addColumn($col[1],$col[0]);
      }
      //miro si el tipo de la segunda columna es date, si lo es debo de evaluar para obtener objetos Date
      if($columnas[1].split(':')[1]=='date'){
        for (var i=0;i<$datos.length;i++){
          $datos[i][1] = eval($datos[i][1]);
        }
      }
      data.addRows($datos);
      var options = {
        width: 900,
        height: 500
      };
      var chart = new google.visualization.MotionChart(document.getElementById($div));
      chart.draw(data, options);
    }
}

