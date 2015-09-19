var colors = ["#FF0F00",
"#348FE2",
"#FF6600",
"#00ACAC",
"#727CB6",
"#B0DE09",
"#04D215",
"#0D8ECF",
"#0D52D1",
"#2A0CD0",
"#8A0CCF",
"#CD0D74",
"#754DEB",
"#DDDDDD",
"#999999",
"#333333",
"#000000"]

function arrayToJson(datos){
	var datos = ((datos).replace(/&(l|g|quo)t;/g, function(a,b){
	    return {
	        l   : '<',
	        g   : '>',
	        quo : '"'
	    }[b];
	}));
	datos = JSON.parse( datos );
	return datos;
}

function exportConfig(){
	return {
	    menuTop: "0px",
	    menuBottom: "auto",
	    menuLeft: "0px",
	    backgroundColor: "#efefef",
	    menuItemStyle: {
	        backgroundColor: '#EFEFEF',
	        rollOverBackgroundColor: '#DDDDDD'},
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