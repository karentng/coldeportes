if(typeof(options)=='undefined'){options=[]}
var table = $('#'+idTabla).DataTable({
    dom: 'TRC<"clear">lfrtip',
    tableTools: {
        "sSwfPath": base+"plugins/DataTables/swf/copy_csv_xls_pdf.swf",
        "aButtons": [
            {
                "sExtends": "copy",
                "mColumns": function(dtSettings){
                    var api = new $.fn.dataTable.Api(dtSettings);
                    if(opciones == true){
                    	return api.columns(":not(:last)").indexes().toArray();
                    }else{
                    	return api.columns().indexes().toArray();
                    }
                }
            },
            {
                "sExtends": "csv",
                "mColumns": function(dtSettings){
                    var api = new $.fn.dataTable.Api(dtSettings);
                    if(opciones == true){
                    	return api.columns(":not(:last)").indexes().toArray();
                    }else{
                    	return api.columns().indexes().toArray();
                    }
                }
            },
            {
                "sExtends": "xls",
                "mColumns": function(dtSettings){
                    var api = new $.fn.dataTable.Api(dtSettings);
                    if(opciones == true){
                    	return api.columns(":not(:last)").indexes().toArray();
                    }else{
                    	return api.columns().indexes().toArray();
                    }
                }
            },
            {
                "sExtends": "pdf",
                "mColumns": function(dtSettings){
                    var api = new $.fn.dataTable.Api(dtSettings);
                    if(opciones == true){
                    	return api.columns(":not(:last)").indexes().toArray();
                    }else{
                    	return api.columns().indexes().toArray();
                    }
                }
            },
            {
                "sExtends": "print",
                "mColumns": function(dtSettings){
                    var api = new $.fn.dataTable.Api(dtSettings);
                    if(opciones == true){
                    	return api.columns(":not(:last)").indexes().toArray();
                    }else{
                    	return api.columns().indexes().toArray();
                    }
                }
            },
        ]
    },
    "columnDefs": options,
});