'use strict';

import utils from './Utils';
/*-----------------------------------------------
|   Animated progressbar
-----------------------------------------------*/
utils.$document.ready(() => {
  const toggle = $('#progress-toggle-animation');
  toggle.on('click', () =>
    $('#progress-toggle').toggleClass('progress-bar-animated')
  );
});
