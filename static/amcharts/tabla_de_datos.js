function TablaDeDatos(identificadorTabla){
	var idTabla = "#"+identificadorTabla;
	return{
		actualizar: function(datos, columnas){
			var misColumnas = [];
			for(i in columnas){
				misColumnas.push(
					{
						"sTitle": columnas[i],
						"aTargets": [i],
					}
				);
			}
			var tabla = $(idTabla).dataTable( {
                "dom": 'TRC<"clear">lfrtip',
                "bDestroy": true,
                "aaData": datos,
                "columns": misColumnas,
                "tableTools": {
                    "sSwfPath": base+"plugins/DataTables/swf/copy_csv_xls.swf",
                    
                },
            });
		},
		transformarDatos: function(datos){
			var datosTransformados = [];
	        for(i in datos){
	            datosTransformados.push([i, datos[i]]);
	        }
	        return datosTransformados;
		}
	}
}