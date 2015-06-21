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
					var table = $('#'+idTabla).DataTable({
				        dom: 'TRC<"clear">lfrtip',
				        tableTools: {
				            "sSwfPath": base+"plugins/DataTables/swf/copy_csv_xls_pdf.swf",
				            "aButtons": [
				                {
				                    "sExtends": "copy",
				                    "mColumns": function(dtSettings){
				                        var api = new $.fn.dataTable.Api(dtSettings);
				                        return api.columns(":not(:last)").indexes().toArray();
				                    }
				                },
				                {
				                    "sExtends": "csv",
				                    "mColumns": function(dtSettings){
				                        var api = new $.fn.dataTable.Api(dtSettings);
				                        return api.columns(":not(:last)").indexes().toArray();
				                    }
				                },
				                {
				                    "sExtends": "xls",
				                    "mColumns": function(dtSettings){
				                        var api = new $.fn.dataTable.Api(dtSettings);
				                        return api.columns(":not(:last)").indexes().toArray();
				                    }
				                },
				                {
				                    "sExtends": "pdf",
				                    "mColumns": function(dtSettings){
				                        var api = new $.fn.dataTable.Api(dtSettings);
				                        return api.columns(":not(:last)").indexes().toArray();
				                    }
				                },
				                {
				                    "sExtends": "print",
				                    "mColumns": function(dtSettings){
				                        var api = new $.fn.dataTable.Api(dtSettings);
				                        return api.columns(":not(:last)").indexes().toArray();
				                    }
				                },
				            ]
				        },
				        "columnDefs": options,
				    });
				});
			});
		});
	});
});