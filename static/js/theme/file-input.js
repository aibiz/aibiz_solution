"use strict";

import utils from "./Utils";
/*-----------------------------------------------
|   File Input
-----------------------------------------------*/
utils.$document.ready(() => {
  $(".custom-file-input").on("change", (e) => {
    const $this = $(e.currentTarget);
    const fileName = $this.val().split("\\").pop();
    $this.next(".custom-file-label").addClass("selected").html(fileName);
  });
});
