/*   
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.4
Version: 1.7.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.7/admin/
*/

var handleCalendarDemo = function () {
	"use strict";
	
	var calendar = $('#calendar').fullCalendar({
		header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
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
        allDayText:"Todo el día",
        eventLimitText:"más",
        timeFormat: 'H:mm',
		editable: false,
        droppable: false, // this allows things to be dropped onto the calendar
        defaultDate: (new Date().getFullYear() + '-' + (new Date().getMonth()+1) + '-' + new Date().getDate()),
        eventLimit: true, // allow "more" link when too many events
		eventClick: function(calEvent, jsEvent, view) {
            //Redireccion a ver mas de evento
            var id =  calEvent.id;
            window.location.href = "ver-evento/"+id;
        },
		eventRender: function(event, element, calEvent) {
			var mediaObject = (event.media) ? event.media : '';
			var description = (event.description) ? event.description : '';
            element.find(".fc-event-title").after($("<span class=\"fc-event-icons\"></span>").html(mediaObject));
            element.find(".fc-event-title").append('<small>'+ description +'</small>');
			element.find(".fc-event-title").css('cursor','pointer');
        },
		events: calendarEvents
	});
    $(".external-event a").click(function(){
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