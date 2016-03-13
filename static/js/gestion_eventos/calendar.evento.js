/*   
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.4
Version: 1.7.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.7/admin/
*/

var handleCalendarDemo = function () {
	"use strict";
	var buttonSetting = {left: 'today prev,next ', center: 'title', right: 'month,agendaWeek,agendaDay'};
	var date = new Date();
	var m = date.getMonth();
	var y = date.getFullYear();
	
	var calendar = $('#calendar').fullCalendar({
		header: buttonSetting,
		selectable: true,
		selectHelper: true,
		droppable: true,
		drop: function(date, allDay) { // this function is called when something is dropped
		
			// retrieve the dropped element's stored Event Object
			var originalEventObject = $(this).data('eventObject');
			
			// we need to copy it, so that multiple events don't have a reference to the same object
			var copiedEventObject = $.extend({}, originalEventObject);
			
			// assign it the date that was reported
			copiedEventObject.start = date;
			console.log(date);
			copiedEventObject.allDay = allDay;
			
			// render the event on the calendar
			// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
			$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
			
			// is the "remove after drop" checkbox checked?
			if ($('#drop-remove').is(':checked')) {
				// if so, remove the element from the "Draggable Events" list
				$(this).remove();
			}
			
		},
		select: function(){
			return false;
		},
		eventDrop:function( event, dayDelta, minuteDelta, allDay, revertFunc) {
			var data = {};
			if(minuteDelta === 0){
				data = {delta_dias: dayDelta, id: event.act_id, csrfmiddlewaretoken: csrf};
			}else {
				data = {delta_dias: dayDelta, delta_minutos: minuteDelta, id: event.act_id, csrfmiddlewaretoken: csrf};
			}
			$.post(urlDrop, data, function(datam){
				alert(datam['status']+", "+datam["message"]);
			}).fail(function(datam){
				alert(datam['status']+", "+datam["message"]);
				revertFunc();
			});
		},
		eventResize : function( event, dayDelta, minuteDelta, revertFunc){
			revertFunc();
		},
		eventRender: function(event, element, calEvent) {
				var mediaObject = (event.media) ? event.media : '';
				var description = (event.description) ? event.description : '';
            element.find(".fc-event-title").after($("<span class=\"fc-event-icons\"></span>").html(mediaObject));
            element.find(".fc-event-title").append('<small>'+ description +'</small>');
        },
		editable: true,
		events: calendarEvents
	});
	
	/* initialize the external events
	-----------------------------------------------------------------*/
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