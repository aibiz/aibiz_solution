"use strict";

import utils from "./Utils";

/*-----------------------------------------------
|   Navbar Top
-----------------------------------------------*/

utils.$document.ready(() => {
  const Selectors = {
    COLLAPSE: ".collapse",
    NAVBAR_NAV: ".navbar-nav",
    NAVBAR_TOP_COMBO: ".navbar-top-combo",
    NAVBAR_VERTICAL: ".navbar-vertical",
    NAVBAR_VERTICAL_DIVIDER: ".navbar-vertical-divider",
    NAVBAR_TOP_COMBO_COLLAPSE: ".navbar-top-combo .collapse",
    MOVEABLE_CONTENT: "[data-move-container]",
  };
  const CLASS_NAME = {
    FLEX_COLUMN: "flex-column",
  };
  const DATA_KEYS = {
    MOVE_TARGET: "move-target",
  };
  const $navbarTop = $(Selectors.NAVBAR_TOP_COMBO);
  const $navbarVertical = $(Selectors.NAVBAR_VERTICAL);
  const navbarTopBreakpoint = utils.getBreakpoint($navbarTop);
  const navbarVertcicalBreakpoint = utils.getBreakpoint($navbarVertical);

  const moveNavContent = (width) => {
    if (width < navbarTopBreakpoint) {
      const $navbarTopCollapse = $navbarTop.find(Selectors.COLLAPSE);
      let navbarTopContent = $navbarTopCollapse.html();
      if (navbarTopContent) {
        $navbarTopCollapse.html("");
        const divider =
          "<div class='navbar-vertical-divider'><hr class='navbar-vertical-hr' /></div>";
        navbarTopContent = `<div data-move-container>${divider}${navbarTopContent}</div>`;
        const targetID = $navbarTop.data(DATA_KEYS.MOVE_TARGET);
        $(navbarTopContent).insertAfter(targetID);

        navbarTopBreakpoint > navbarVertcicalBreakpoint &&
          $(Selectors.MOVEABLE_CONTENT)
            .find(Selectors.NAVBAR_NAV)
            .addClass(CLASS_NAME.FLEX_COLUMN);
      }
    } else {
      const $container = $(Selectors.MOVEABLE_CONTENT);
      const $navbarNav = $container.find(Selectors.NAVBAR_NAV);

      $navbarNav.hasClass(CLASS_NAME.FLEX_COLUMN) &&
        $navbarNav.removeClass(CLASS_NAME.FLEX_COLUMN);

      $container.find(Selectors.NAVBAR_VERTICAL_DIVIDER).remove();
      const content = $container.html();
      $container.remove();
      $(Selectors.NAVBAR_TOP_COMBO_COLLAPSE).html(content);
    }
  };
  moveNavContent(utils.$window.outerWidth());
  utils.$window.on("resize", () => {
    moveNavContent(utils.$window.outerWidth());
  });
});
