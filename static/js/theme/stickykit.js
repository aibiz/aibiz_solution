"use strict";

import utils from "./Utils";

/*-----------------------------------------------
|   Sticky Kit
-----------------------------------------------*/
utils.$document.ready(() => {
  if (window.is.ie()) {
    const stickyKits = $(".sticky-kit");
    if (stickyKits.length) {
      stickyKits.each((index, value) => {
        const $this = $(value);
        const options = { ...$this.data("options") };
        $this.stick_in_parent(options);
      });
    }
  }
});
