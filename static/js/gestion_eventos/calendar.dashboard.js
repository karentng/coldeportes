/**
 * Created by juandgc on 16/03/16.
 */
var handleScheduleCalendar = function() {
    var monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    var dayNames = ["D", "L", "M", "M", "J", "V", "S"];

    var events = calendarEvents;
    console.log(events);
    var calendarTarget = $('#schedule-calendar');
    $(calendarTarget).calendar({
        months: monthNames,
        days: dayNames,
        events: events,
        popover_options:{
            placement: 'top',
            html: true
        }
    });
    $(calendarTarget).find('td.event').each(function() {
        var backgroundColor = $(this).css('background-color');
        $(this).removeAttr('style');
        $(this).find('a').css('background-color', backgroundColor);
    });
    $(calendarTarget).find('.icon-arrow-left, .icon-arrow-right').parent().on('click', function() {
        $(calendarTarget).find('td.event').each(function() {
            var backgroundColor = $(this).css('background-color');
            $(this).removeAttr('style');
            $(this).find('a').css('background-color', backgroundColor);
        });
    });
};


var Dashboard = function () {
	"use strict";
    return {
        //main function
        init: function () {
            handleScheduleCalendar();
        }
    };
}();