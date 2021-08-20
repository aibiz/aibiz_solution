'use strict';

import utils from './Utils';

/* -------------------------------------------------------------------------- */
/*                             Autocomplete Search                            */
/* -------------------------------------------------------------------------- */

utils.$document.ready(() => {
  const Selectors = {
    DROPDOWN: '.dropdown',
    SEARCH_DISMISS: '[data-dismiss="search"]',
    DROPDOWN_TOGGLE: '[data-toggle="dropdown"]',
    SEARCH_BOX: '.search-box',
    SEARCH_INPUT: '.search-input',
    SEARCH_TOGGLE: '[data-toggle="search"]',
  };

  const Events = {
    CLICK: 'click',
    FOCUS: 'focus',
    SHOW_BS_DROPDOWN: 'show.bs.dropdown',
  };

  const $searchAreas = $(Selectors.SEARCH_BOX);

  const hideSearchSuggestion = (searchArea) => {
    const el = searchArea.querySelector(Selectors.SEARCH_TOGGLE);
    const dropdown = $(el).dropdown();
    dropdown?.dropdown('hide');
  };

  const hideAllSearchAreas = () => {
    $searchAreas.each((index, value) => hideSearchSuggestion(value));
  };

  $searchAreas.each((index, value) => {
    const input = value.querySelector(Selectors.SEARCH_INPUT);
    const btnDropdownClose = value.querySelector(Selectors.SEARCH_DISMISS);

    input.addEventListener(Events.FOCUS, () => {
      hideAllSearchAreas();
      const el = value.querySelector(Selectors.SEARCH_TOGGLE);
      const dropdown = $(el).dropdown();
      dropdown.dropdown('show');
    });

    document.addEventListener(Events.CLICK, ({ target }) => {
      !value.contains(target) && hideSearchSuggestion(value);
    });

    btnDropdownClose &&
      btnDropdownClose.addEventListener(Events.CLICK, () => {
        hideSearchSuggestion(value);
        input.value = '';
      });
  });

  $(Selectors.DROPDOWN).on(Events.SHOW_BS_DROPDOWN, () => hideAllSearchAreas());
});
