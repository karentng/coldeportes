if(typeof(options)=='undefined'){options=[]}
var columnas = function(dtSettings){
    var api = new $.fn.dataTable.Api(dtSettings);
    return api.columns(":not(:last)").indexes().toArray();
}
var table = $('#'+idTabla).DataTable({
    
    responsive: true,
    dom: 'TRC<"clear">lfrtip',
    tableTools: {
        "sSwfPath": base+"plugins/DataTables/swf/copy_csv_xls_pdf.swf",
        "aButtons": [
            {
                "sExtends": "copy",
                "mColumns": columnas,
                "sButtonClass": "btn",
                "sButtonText": "<i class='fa fa-copy bigger-110 pink'></i> Copiar",
            },
            {
                "sExtends": "xls",
                "sButtonClass": "btn",
                "mColumns": columnas,
                "sButtonText": "<i class='fa fa-file-excel-o bigger-110 green'></i> XLS"
            },
            {
                "sExtends": "pdf",
                "sButtonClass": "btn",
                "mColumns": columnas,
                "sButtonText": "<i class='fa fa-file-pdf-o bigger-110 red'></i> PDF"
            },
            {
                "sExtends": "print",
                "sButtonClass": "btn",
                "mColumns": columnas,
                "sButtonText": "<i class='fa fa-print bigger-110 grey'></i> Imprimir",
            },
        ]
    },
    "columnDefs": options,
});
