'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Draggable
-----------------------------------------------*/

utils.$document.ready(() => {
  const Selectors = {
    ADD_LIST_FORM: '#add-list-form',
    KANBAN_COLUMN: '.kanban-column',
    BTN_ADD_CARD: '.btn-add-card',
    KANBAN_ITEMS_CONTAINER: '.kanban-items-container',
    COLLAPSE: '.collapse',
    COLLAPSE_CLOSE: "[data-dismiss='collapse']",
    ADD_CARD: '.add-card',
    ADD_LIST: '.add-list',
    MODAL_ANCHOR: "[data-toggle='modal'] a",
    HIDE_ADD_CARD_FORM: '.hide-add-card-form',
  };

  const Events = {
    TOGGLE_BS_COLLAPSE: 'show.bs.collapse hide.bs.collapse',
    SHOWN_BS_COLLAPSE: 'shown.bs.collapse',
    CLICK: 'click',
  };

  const ClassNames = {
    FORM_ADDED: 'form-added',
    D_NONE: 'd-none',
  };

  // Hide button when Add list form is shown
  $(Selectors.ADD_LIST_FORM).on(Events.TOGGLE_BS_COLLAPSE, (e) => {
    const $this = $(e.currentTarget);
    $this.next().toggleClass(ClassNames.D_NONE);
  });

  // Show card add form and scroll to the bottom
  utils.$document.on(Events.CLICK, Selectors.BTN_ADD_CARD, (e) => {
    const $this = $(e.currentTarget);
    const $column = $this.closest(Selectors.KANBAN_COLUMN);
    const $container = $column.find(Selectors.KANBAN_ITEMS_CONTAINER);
    const scrollHeight = $container[0].scrollHeight;
    $column.addClass(ClassNames.FORM_ADDED);
    $container.scrollTop(scrollHeight);
    $container.find(Selectors.ADD_CARD).focus();
  });

  // Hide card add form
  utils.$document.on(Events.CLICK, Selectors.HIDE_ADD_CARD_FORM, (e) => {
    const $this = $(e.currentTarget);
    const $column = $this.closest(Selectors.KANBAN_COLUMN);
    $column.removeClass(ClassNames.FORM_ADDED);
  });

  // Focus add list form on form shown
  $(Selectors.ADD_LIST_FORM).on(Events.SHOWN_BS_COLLAPSE, (e) => {
    const $this = $(e.currentTarget);
    $this.find(Selectors.ADD_LIST).focus();
  });

  utils.$document.on(Events.CLICK, Selectors.MODAL_ANCHOR, (e) => {
    e.stopPropagation();
  });

  // Close collapse when corresponding close button is clicked
  utils.$document.on(Events.CLICK, Selectors.COLLAPSE_CLOSE, (e) => {
    const $this = $(e.currentTarget);
    $this.closest(Selectors.COLLAPSE).collapse('hide');
  });
});
