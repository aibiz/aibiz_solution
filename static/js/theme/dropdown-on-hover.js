'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Documentation and Component Navigation
-----------------------------------------------*/
utils.$document.ready(() => {
  const Selector = {
    NAVBAR_THEME_DROPDOWN: '.navbar-theme .dropdown',
    DROPDOWN_ON_HOVER: '.dropdown-on-hover',
    DATA_TOGGLE_DROPDOWN: '[data-toggle="dropdown"]',
    BODY: 'body',
  };

  const ClassName = {
    DROPDOWN_ON_HOVER: 'dropdown-on-hover',
  };

  const Event = {
    CLICK: 'click',
    MOUSE_LEAVE: 'mouseleave',
    MOUSE_EVENT: 'mouseenter mouseleave',
  };

  const $navbarDropdown = $(Selector.NAVBAR_THEME_DROPDOWN);

  !window.is.mobile()
    ? $navbarDropdown.addClass(ClassName.DROPDOWN_ON_HOVER)
    : $navbarDropdown.removeClass(ClassName.DROPDOWN_ON_HOVER);

  const toggleDropdown = (e) => {
    const $el = $(e.target);
    const dropdown = $el.closest(Selector.DROPDOWN_ON_HOVER);
    const btnDropdown = dropdown.find(Selector.DATA_TOGGLE_DROPDOWN);
    setTimeout(
      () => {
        let shouldOpen = e.type !== Event.CLICK && dropdown.is(':hover');

        shouldOpen
          ? btnDropdown.dropdown('show')
          : btnDropdown.dropdown('hide');
      },
      e.type === Event.MOUSE_LEAVE ? 100 : 0
    );
  };

  $(Selector.BODY).on(
    Event.MOUSE_EVENT,
    Selector.DROPDOWN_ON_HOVER,
    toggleDropdown
  );
});
