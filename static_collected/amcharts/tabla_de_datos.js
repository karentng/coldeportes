function TablaDeDatos(identificadorTabla, columnas, datosIniciales){
	var idTabla = "#"+identificadorTabla;
	var todasLasColumnas = columnas;
	var estado = 0;
	var generado = false;
	var datos = datosIniciales;

	function transformarDatos(datos){
		var datosTransformados = [];
        for(i in datos){
            datosTransformados.push([i, datos[i]]);
        }
        return datosTransformados;
	}

	function cambioDiv(nuevoEstado){
		estado = nuevoEstado;
		if(estado){ // presiono el de la tabla
			if(generado == false){
				actualizar();
				generado = true;
			}
		}
	}

	function actualizar(){
		var misColumnas = [];
		for(i in todasLasColumnas){
			misColumnas.push(
				{
					"sTitle": todasLasColumnas[i],
					"aTargets": [i],
				}
			);
		}
		setTimeout(function(){
			var tabla = $(idTabla).dataTable( {
	            "dom": 'TRC<"clear">lfrtip',
	            "bDestroy": true,
	            "aaData": datos,
	            "columns": misColumnas,
	            "tableTools": {
		            "sSwfPath": base+"plugins/DataTables/swf/copy_csv_xls_pdf.swf",
		            "aButtons": [
		                {
		                    "sExtends": "copy",
		                    "sButtonClass": "btn",
		                    "sButtonText": "<i class='fa fa-copy bigger-110 pink'></i> Copiar",
		                },
		                {
		                    "sExtends": "xls",
		                    "sButtonClass": "btn",
		                    "sButtonText": "<i class='fa fa-file-excel-o bigger-110 green'></i> XLS"
		                },
		                {
		                    "sExtends": "pdf",
		                    "sButtonClass": "btn",
		                    "sButtonText": "<i class='fa fa-file-pdf-o bigger-110 red'></i> PDF"
		                },
		                {
		                    "sExtends": "print",
		                    "sButtonClass": "btn",
		                    "sButtonText": "<i class='fa fa-print bigger-110 grey'></i> Imprimir",
		                },
		            ],
		        },
	        });
		}
		, 500);
	}

	return{
		actualizar: function(){
			actualizar();
		},
		transformarDatos: function(datos){
			trasformarDatos(datos);
		},
		cambioDiv: function(nuevoEstado){ // 1) es el de la tabla, 0) otro
			console.log(nuevoEstado);
			cambioDiv(nuevoEstado);
		},
		setDatos: function(data){ // OK
			datos = transformarDatos(data);
		},
		setColumnas: function(cols){ // OK
			todasLasColumnas = cols;
		},
		verificarActualizacion: function(){
			generado = false;
			if(estado == 1){
				cambioDiv(estado);
			}
		}
	}
}