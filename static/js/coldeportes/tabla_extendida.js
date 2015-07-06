/*
	Junio 18 / 2015
    Autor: Andrés Serna
    
    Proveer los atributos de la "Managed Table - Extension Combination" a la tabla elegida.

    Cargo los js necesarios para "Managed Table - Extension Combination", a través del id de la tabla, le agrego las propiedades

    :param id:   	 Id de la tabla
    :type id:    	 String
*/

$.getScript(base+"plugins/DataTables/js/jquery.dataTables.js", function(){
	$.getScript(base+"plugins/DataTables/js/dataTables.colReorder.js", function(){
		$.getScript(base+"plugins/DataTables/js/dataTables.colVis.js", function(){
			$.getScript(base+"plugins/DataTables/js/dataTables.keyTable.js", function(){
				$.getScript(base+"plugins/DataTables/js/dataTables.tableTools.js", function(){
					if (typeof url != 'undefined'){
						console.log("bien");
						$.getScript(base+"js/coldeportes/cargado_datos.js");
					}else{
						// Discutir si es necesario a futuro (es posible para casos pequeños)
						$.getScript(base+"js/coldeportes/cargado_normal.js");
					}
				});
			});
		});
	});
});