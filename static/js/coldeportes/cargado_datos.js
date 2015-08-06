$.fn.dataTable.pipeline = function ( opts ) {
// Configuration options
var conf = $.extend( {
    pages: 5,     // number of pages to cache
    url: '',      // script url
    data: null,   // function or object with parameters to send to the server
                  // matching how `ajax.data` works in DataTables
    method: 'GET' // Ajax HTTP method
}, opts );

// Private variables for storing the cache
var cacheLower = -1;
var cacheUpper = null;
var cacheLastRequest = null;
var cacheLastJson = null;

return function ( request, drawCallback, settings ) {
    var ajax          = false;
    var requestStart  = request.start;
    var drawStart     = request.start;
    var requestLength = request.length;
    var requestEnd    = requestStart + requestLength;

    if ( settings.clearCache ) {
        // API requested that the cache be cleared
        ajax = true;
        settings.clearCache = false;
    }
    else if ( cacheLower < 0 || requestStart < cacheLower || requestEnd > cacheUpper ) {
        // outside cached data - need to make a request
        ajax = true;
    }
    else if ( JSON.stringify( request.order )   !== JSON.stringify( cacheLastRequest.order ) ||
              JSON.stringify( request.columns ) !== JSON.stringify( cacheLastRequest.columns ) ||
              JSON.stringify( request.search )  !== JSON.stringify( cacheLastRequest.search )
    ) {
        // properties changed (ordering, columns, searching)
        ajax = true;
    }

    // Store the request for checking next time around
    cacheLastRequest = $.extend( true, {}, request );

    if ( ajax ) {
        // Need data from the server
        if ( requestStart < cacheLower ) {
            requestStart = requestStart - (requestLength*(conf.pages-1));

            if ( requestStart < 0 ) {
                requestStart = 0;
            }
        }

        cacheLower = requestStart;
        cacheUpper = requestStart + (requestLength * conf.pages);

        request.start = requestStart;
        request.length = requestLength*conf.pages;

        // Provide the same `data` options as DataTables.
        if ( $.isFunction ( conf.data ) ) {
            // As a function it is executed with the data object as an arg
            // for manipulation. If an object is returned, it is used as the
            // data object to submit
            var d = conf.data( request );
            if ( d ) {
                $.extend( request, d );
            }
        }
        else if ( $.isPlainObject( conf.data ) ) {
            // As an object, the data given extends the default
            $.extend( request, conf.data );
        }

        settings.jqXHR = $.ajax( {
            "type":     conf.method,
            "url":      conf.url,
            "data":     request,
            "dataType": "json",
            "cache":    false,
            "success":  function ( json ) {
                atributos = json.nombreDeColumnas
                json = json.datos
                
                for (i in atributos){
                    $('#'+idTabla+' tr:eq(0) th:eq('+i+')').text(atributos[i]);
                }

                cacheLastJson = $.extend(true, {}, json);

                if ( cacheLower != drawStart ) {
                    json.data.splice( 0, drawStart-cacheLower );
                }
                json.data.splice( requestLength, json.data.length );

                drawCallback( json );
            }
        } );
    }
    else {
        json = $.extend( true, {}, cacheLastJson );
        json.draw = request.draw; // Update the echo for each response
        json.data.splice( 0, requestStart-cacheLower );
        json.data.splice( requestLength, json.data.length );

        drawCallback(json);
    }
}
};

// Register an API method that will empty the pipelined data, forcing an Ajax
// fetch on the next draw (i.e. `table.clearPipeline().draw()`)
$.fn.dataTable.Api.register( 'clearPipeline()', function () {
return this.iterator( 'table', function ( settings ) {
    settings.clearCache = true;
} );
} );


$.ajax( {
"type":     'GET',
"url":      url,
"dataType": "json",
"cache":    false,
"success":  function ( json ) {
	var columnas = [];
	for (i in json.columnas){
		var aux = json.columnas[i];
		columnas.push({"title": aux, "targets": parseInt(i), "orderable": true});
	}
	if (opciones){
		columnas.push({"title": "Opciones", "targets": columnas.length, "orderable": true});
	}

    $('#'+idTabla).dataTable({
        "responsive": true,
        "pagingType": "simple_numbers",
        "pageLength": 10,
        "columnDefs": columnas,
        "language": {
            "paginate": {
                "previous": '<i class="fa fa-angle-left"></i>',
                "next": '<i class="fa fa-angle-right"></i>'
            }
        },
        serverSide: true,
        processing: true,
        ajax: $.fn.dataTable.pipeline({
            url: json.url,
            pages: 7 // number of pages to cache
        }),

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
                    },
                    "sButtonClass": "btn",
                    "sButtonText": "<i class='fa fa-copy bigger-110 pink'></i> Copiar",
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
                    },
                    "sButtonClass": "btn",
                    "sButtonText": "<i class='fa fa-file-text-o bigger-110 green'></i> CSV"
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
                    },
                    "sButtonClass": "btn",
                    "sButtonText": "<i class='fa fa-file-excel-o bigger-110 green'></i> XLS"
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
                    },
                    "sButtonClass": "btn",
                    "sButtonText": "<i class='fa fa-file-pdf-o bigger-110 red'></i> PDF"
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
                    },
                    "sButtonClass": "btn",
                    "sButtonText": "<i class='fa fa-print bigger-110 grey'></i> Imprimir",
                },
            ],
        },
    });
}
} );