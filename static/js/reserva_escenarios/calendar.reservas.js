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
    var date = new Date();
    var m = date.getMonth();
    var y = date.getFullYear();
    
    var calendar = $('#calendar').fullCalendar({
        header: buttonSetting,
        monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
        monthNamesShort: ['Ene','Feb','Mar','Abr','Mayo','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
        dayNames: ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado'],
        dayNamesShort: ['Dom','Lun','Mar','Mie','Jue','Vie','Sab'],
        buttonText: {
            today: 'Hoy',
            month: 'Mes',
            week: 'Semana',
            day: 'Día'
        },
        timeFormat: 'H:mm',
        selectable: false,
        selectHelper: false,
        droppable: true,
        editable: true,
        drop: function(date, allDay) { // this function is called when something is dropped

            var nuevaReserva = $(this).data('eventObject');
            nuevaReserva.start = date;
            nuevaReserva.allDay = false;   
            data = {fecha_inicio: date, csrfmiddlewaretoken: csrf};         
            
            $('#calendar').fullCalendar('renderEvent', nuevaReserva, true);
            $(this).remove();
            
        },
        eventResize: function(event,dayDelta,minuteDelta,revertFunc) {

            if (event.end !== null)
            {
                data = {fecha_inicio: event.start, fecha_fin: event.end, csrfmiddlewaretoken: csrf};
                
            } else
            {
                data = {fecha_inicio: event.start, csrfmiddlewaretoken: csrf};
                
            }

        },
        eventDrop: function(event,dayDelta,minuteDelta,allDay,revertFunc) {
            if (event.end !== null)
            {
                data = {fecha_inicio: event.start, fecha_fin: event.end, csrfmiddlewaretoken: csrf};
                
            } else
            {
                data = {fecha_inicio: event.start, csrfmiddlewaretoken: csrf};
                
            }
            //revert = revertFunc;
            

        },
        eventRender: function(event, element, calEvent) {
                var mediaObject = (event.media) ? event.media : '';
                var description = (event.description) ? event.description : '';
            element.find(".fc-event-title").after($("<span class=\"fc-event-icons\"></span>").html(mediaObject));
            element.find(".fc-event-title").append('<small>'+ description +'</small>');
        },
        events: calendarEvents
    });
    
    /* initialize the external events
    -----------------------------------------------------------------*/
    $('#modal-confirmacion').on('click', '.btn-ok', function(e) {

        var $modalDiv = $(e.delegateTarget);

        $modalDiv.addClass('loading');

        $.post(urlAgendar, data, function(datam){

            $modalDiv.modal('hide').removeClass('loading');

            window.location.replace(urlRedirect);           
            
        }).fail(function(datam){
            
        });
    });

    $('#modal-confirmacion').on('click', '.btn-not', function(e) {
        revert();
    });

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