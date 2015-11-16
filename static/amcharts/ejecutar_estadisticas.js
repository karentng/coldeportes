$.getScript(base+"amcharts/amcharts.js", function(){
	$.getScript(base+"amcharts/themes/light.js", function() {
		$.getScript(base + "amcharts/pie.js", function () {
			$.getScript(base + "amcharts/serial.js", function () {
				$.getScript(base + "amcharts/exporting/amexport.js", function () {
					$.getScript(base + "amcharts/exporting/canvg.js", function () {
						$.getScript(base + "amcharts/exporting/rgbcolor.js", function () {
							$.getScript(base + "amcharts/exporting/filesaver.js", function () {
								$.getScript(base + "amcharts/estadisticas.js", function () {
									$.getScript(base + "js/d3.js", function () {
										$.getScript(base + "js/d3plus.js", function () {

											Reportes = Reportes();

											function graficar(nombreReporte) {
												for (i in visualizaciones) {
													var aux = parseInt(visualizaciones[i]);
													Reportes.crearGrafico(datos, parseInt(visualizaciones[i]), "chartdiv" + aux, nombreReporte);
												}
											}

											graficar(nombreReporte);

											//----------------------------------------------

											function cambiarDiv(num) {
												for (i in visualizaciones) {
													var aux = visualizaciones[i];
													$("#chartdiv" + aux).hide();
												}
												$("#chartdiv" + num).show();
											}

											$("#id_visualizacion").on("change", function () {
												cambiarDiv($(this).val());
											});
											$(document).ready(function () {
												cambiarDiv(visualizaciones[0]);

											});

											$(window).resize(function () {
												var div = document.getElementById("chartdiv4");
												realizarConsulta();
											});
										});
									});
								});
							});
						});
					});
				});
			});
		});
	});
});