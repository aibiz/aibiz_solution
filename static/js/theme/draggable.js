"use strict";

import utils from "./Utils";

/*-----------------------------------------------
|   Draggable
-----------------------------------------------*/

utils.$document.ready(() => {
  const Selectors = {
    BODY: "body",
    KANBAN_CONTAINER: ".kanban-container",
    KANBAN_ITEMS_CONTAINER: ".kanban-items-container",
    KANBAN_ITEM: ".kanban-item",
    KANBAN_COLLAPSE: "[data-collapse='kanban']",
    PS_RAILS: ".ps__rail-x, .ps__rail-y", // Perfect scrollbar rails in IE
  };

  const Events = {
    DRAG_START: "drag:start",
    DRAG_STOP: "drag:stop",
  };
  const columns = document.querySelectorAll(Selectors.KANBAN_ITEMS_CONTAINER);
  const container = document.querySelector(Selectors.KANBAN_CONTAINER);
  const scrollItems = $(Selectors.KANBAN_ITEMS_CONTAINER);
  const scrollableElements = [];
  scrollItems.each((index, item) => {
    scrollableElements[index] = item;
  });
  if (!!columns.length) {
    // Initialize Sortable
    const sortable = new window.Draggable.Sortable(columns, {
      draggable: Selectors.KANBAN_ITEM,
      delay: 200,
      mirror: {
        appendTo: Selectors.BODY,
        constrainDimensions: true,
      },
      scrollable: {
        draggable: Selectors.KANBAN_ITEM,
        scrollableElements: [...scrollableElements, container],
      },
    });

    // Hide form when drag start
    sortable.on(Events.DRAG_START, () => {
      $(Selectors.KANBAN_COLLAPSE).collapse("hide");
    });

    // Place forms and other contents bottom of the sortable container
    sortable.on(Events.DRAG_STOP, (e) => {
      const $this = $(e.data.source);
      const $itemContainer = $this.closest(Selectors.KANBAN_ITEMS_CONTAINER);
      const $collapse = $this
        .closest(Selectors.KANBAN_ITEMS_CONTAINER)
        .find(Selectors.KANBAN_COLLAPSE);

      $this.is(":last-child") && $itemContainer.append($collapse);

      // For IE
      if (window.is.ie()) {
        const $rails = $itemContainer.find(Selectors.PS_RAILS);
        $itemContainer.append($rails);
      }
    });
  }
});
