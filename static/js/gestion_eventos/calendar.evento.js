/*   
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.4
Version: 1.7.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.7/admin/
*/

var handleCalendarDemo = function () {
	"use strict";
	var buttonSetting = {left: 'today prev,next ', center: 'title', right: 'month,agendaWeek,agendaDay'};
	var data = {};
	var revert;
	var date = new Date();
	var m = date.getMonth();
	var y = date.getFullYear();
	
	var calendar = $('#calendar').fullCalendar({
		header: buttonSetting,
        monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
        monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
        dayNames: ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado'],
        dayNamesShort: ['Dom','Lun','Mar','Mie','Jue','Vie','Sab'],
        buttonText: {
            today: 'Hoy',
            month: 'Mes',
            week: 'Semana',
            day: 'Día'
        },
		selectable: false,
		selectHelper: true,
		eventDrop:function( event, dayDelta, minuteDelta, allDay, revertFunc) {

			if(minuteDelta === 0){
				data = {delta_dias: dayDelta, id: event.act_id, csrfmiddlewaretoken: csrf};
			}else {
				data = {delta_dias: dayDelta, delta_minutos: minuteDelta, id: event.act_id, csrfmiddlewaretoken: csrf};
			}
			revert = revertFunc;
			$("#nuevo-dia > span").text(dayDelta + " días y "+ minuteDelta + " minutos.");
			$('#modal-confirmacion').modal("show");
		},
		eventDurationEditable : false,
		eventRender: function(event, element, calEvent) {
				var mediaObject = (event.media) ? event.media : '';
				var description = (event.description) ? event.description : '';
            element.find(".fc-event-title").after($("<span class=\"fc-event-icons\"></span>").html(mediaObject));
            element.find(".fc-event-title").append('<small>'+ description +'</small>');
        },
		editable: editableCal,
		events: calendarEvents
	});
	
	/* initialize the external events
	-----------------------------------------------------------------
	$('#external-events .external-event').each(function() {
		var eventObject = {
			title: $.trim($(this).attr('data-title')),
			className: $(this).attr('data-bg'),
			media: $(this).attr('data-media'),
			description: $(this).attr('data-desc')
		};
		
		$(this).data('eventObject', eventObject);
		
		$(this).draggable({
			zIndex: 999,
			revert: true,
			revertDuration: 0
		});
	});*/
	$('#modal-confirmacion').on('click', '.btn-ok', function(e) {

		var $modalDiv = $(e.delegateTarget);

		$modalDiv.addClass('loading');
		$.post(urlDrop, data, function(datam){
			$modalDiv.modal('hide').removeClass('loading');

			setTimeout(function() {
				toastr.options = {
					"closeButton": true,
					"progressBar": true,
					"showEasing": "swing"
				};
				toastr["success"]("Actividad actualizada exitosamente");
			},500);
		}).fail(function(datam){
			setTimeout(function() {
				toastr.options = {
					"closeButton": true,
					"progressBar": true,
					"showEasing": "swing"
				};
				toastr["success"]("Actividad actualizada exitosamente");
			},500);
		});
	});
	$('#modal-confirmacion').on('click', '.btn-not', function(e) {
		revert();
	});
	$(".external-event i").click(function(){
		var diaAct = $(this).attr("data-date");
		var goDate = new Date(diaAct);
		var anio = goDate.getFullYear();
		var mes = goDate.getMonth();
		$("#calendar").fullCalendar('gotoDate', anio, mes);
	});
};


var Calendar = function () {
	"use strict";
    return {
        //main function
        init: function () {
            handleCalendarDemo();
        }
    };
}();