'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Jquery Validation
-----------------------------------------------*/

utils.$document.ready(() => {
  const forms = $('.form-validation');
  forms.length &&
    forms.each((index, value) => {
      const $this = $(value);
      const options = $.extend({}, $this.data('options'));

      $this.validate(options);
    });
});
