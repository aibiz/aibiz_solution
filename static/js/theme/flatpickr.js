'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Flatpickr
-----------------------------------------------*/

utils.$document.ready(() => {
  const datetimepicker = $('.datetimepicker');
  datetimepicker.length &&
    datetimepicker.each((index, value) => {
      const $this = $(value);
      const options = $.extend(
        {
          dateFormat: 'd/m/y',
          disableMobile: true,
        },
        $this.data('options')
      );
      $this.flatpickr(options);
    });
});
