'use strict';

import utils from './Utils';

// /*-----------------------------------------------
// |   Full Calendar
// -----------------------------------------------*/
const { merge } = window._;

const renderCalendar = (el, option) => {
  const options = merge(
    {
      themeSystem: 'bootstrap',
      initialView: 'dayGridMonth',
      editable: true,
      direction: $('html').attr('dir'),
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay',
      },
      buttonText: {
        month: 'Month',
        week: 'Week',
        day: 'Day',
      },
    },
    option
  );

  const calendar =
    window.FullCalendar && new window.FullCalendar.Calendar(el, options);
  calendar.render();
  $('.navbar-vertical-toggle').on('navbar.vertical.toggle', () =>
    calendar.updateSize()
  );
  return calendar;
};
utils.$document.ready(() => {
  const calendars = $('[data-calendar]');
  if (calendars.length) {
    calendars.each((index, calendar) => {
      renderCalendar(calendar, JSON.parse(calendar.dataset['calendar']));
    });
  }
  window.FontAwesome.config.autoReplaceSvg = 'nest';
});

export default renderCalendar;
