'use strict';

import utils from '../Utils';
import events from './events';
import getTemplate from './template';
import renderCalendar from '../fullcalendar';

/*-----------------------------------------------
|   Calendar
-----------------------------------------------*/
utils.$document.ready(() => {
  const Selectors = {
    ADD_EVENT_FORM: '#addEventForm',
    ADD_EVENT_MODAL: '#addEvent',
    ACTIVE: '.active',
    CALENDAR: 'appCalendar',
    CALENDAR_TITLE: '.calendar-title',
    NAVBAR_VERTICAL_TOGGLE: '.navbar-vertical-toggle',
    EVENT_DETAILS_MODAL: '#eventDetails',
    EVENT_DETAILS_MODAL_CONTENT: '#eventDetails .modal-content',
    DATA_EVENT: '[data-event]',
    DATA_CALENDAR_VIEW: '[data-fc-view]',
    DATA_VIEW_TITLE: '[data-view-title]',
    INPUT_TITLE: '[name="title"]',
  };

  const Events = {
    CLICK: 'click',
    NAVBAR_VERTICAL_TOGGLE: 'navbar.vertical.toggle',
    SHOWN_BS_MODAL: 'shown.bs.modal',
    SUBMIT: 'submit',
  };

  const DataKeys = {
    EVENT: 'event',
  };

  const ClassNames = {
    ACTIVE: 'active',
  };

  const eventList = events.reduce(
    (acc, val) =>
      val.schedules ? acc.concat(val.schedules.concat(val)) : acc.concat(val),
    []
  );

  const updateTitle = (title) => $(Selectors.CALENDAR_TITLE).text(title);

  const calendarEl = document.getElementById(Selectors.CALENDAR);
  if (calendarEl) {
    const calendar = renderCalendar(calendarEl, {
      headerToolbar: false,
      dayMaxEvents: 2,
      height: 800,
      stickyHeaderDates: false,
      views: {
        week: {
          eventLimit: 3,
        },
      },
      eventTimeFormat: {
        hour: 'numeric',
        minute: '2-digit',
        omitZeroMinute: true,
        meridiem: true,
      },
      events: eventList,
      eventClick: (info) => {
        if (info.event.url) {
          window.open(info.event.url, '_blank');
          info.jsEvent.preventDefault();
        } else {
          const template = getTemplate(info);
          $(Selectors.EVENT_DETAILS_MODAL_CONTENT).html(template);
          $(Selectors.EVENT_DETAILS_MODAL).modal('show');
        }
      },
      dateClick(info) {
        $(Selectors.ADD_EVENT_MODAL).modal('show');
        /*eslint-disable-next-line*/
        const flatpickr = document.querySelector("#addEvent [name='startDate']")
          ._flatpickr;
        flatpickr.setDate([info.dateStr]);
      },
    });

    updateTitle(calendar.currentData.viewTitle);
    $(document).on(Events.CLICK, Selectors.DATA_EVENT, ({ currentTarget }) => {
      const type = $(currentTarget).data(DataKeys.EVENT);
      switch (type) {
        case 'prev':
          calendar.prev();
          updateTitle(calendar.currentData.viewTitle);
          break;
        case 'next':
          calendar.next();
          updateTitle(calendar.currentData.viewTitle);
          break;
        case 'today':
          calendar.today();
          updateTitle(calendar.currentData.viewTitle);
          break;
        default:
          calendar.today();
          updateTitle(calendar.currentData.viewTitle);
          break;
      }
    });

    $(document).on('click', Selectors.DATA_CALENDAR_VIEW, (e) => {
      e.preventDefault();
      const el = $(e.currentTarget);
      const text = el.text();
      el.parent().find('.active').removeClass(ClassNames.ACTIVE);
      el.addClass('active');
      $(Selectors.DATA_VIEW_TITLE).text(text);
      calendar.changeView(el.data('fc-view'));
      updateTitle(calendar.currentData.viewTitle);
    });

    document
      .querySelector(Selectors.ADD_EVENT_FORM)
      .addEventListener(Events.SUBMIT, (e) => {
        e.preventDefault();
        const {
          title,
          startDate,
          endDate,
          label,
          description,
          allDay,
        } = e.target;
        calendar.addEvent({
          title: title.value,
          start: startDate.value,
          end: endDate.value ? endDate.value : null,
          allDay: allDay.checked,
          className:
            allDay.checked && label.value ? `bg-soft-${label.value}` : '',
          description: description.value,
        });
        e.target.reset();
        $(Selectors.ADD_EVENT_MODAL).modal('hide');
      });
  }
  $(Selectors.ADD_EVENT_MODAL).on(
    Events.SHOWN_BS_MODAL,
    ({ currentTarget }) => {
      currentTarget.querySelector(Selectors.INPUT_TITLE).focus();
    }
  );
});
