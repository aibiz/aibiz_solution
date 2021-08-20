"use strict";

import utils from "./Utils";
/*-----------------------------------------------
|   Copy link
-----------------------------------------------*/
utils.$document.ready(() => {
  $("#copyLinkModal").on("shown.bs.modal", () => {
    $(".invitation-link")
      .focus()
      .select();
  });

  utils.$document.on("click", "[data-copy]", (e) => {
    const $this = $(e.currentTarget);
    const targetID = $this.data("copy");

    $(targetID)
      .focus()
      .select();
    document.execCommand("copy");
    $this
      .attr("title", "Copied!")
      .tooltip("_fixTitle")
      .tooltip("show")
      .attr("title", "Copy to clipboard")
      .tooltip("_fixTitle");
  });
});
