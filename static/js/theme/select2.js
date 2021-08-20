'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Select2
-----------------------------------------------*/

utils.$document.ready(() => {
  const select2 = $('.selectpicker');
  select2.length &&
    select2.each((index, value) => {
      const $this = $(value);
      const options = $.extend({ theme: 'bootstrap4' }, $this.data('options'));
      $this.select2(options);
    });
});
