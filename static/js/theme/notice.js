'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Cookie Notice
-----------------------------------------------*/
utils.$document.ready(() => {
  const Selector = {
    NOTICE: '.notice',
    DATA_TOGGLE_NOTICE: "[data-toggle='notice']",
  };
  const DataKeys = { OPTIONS: 'options' };
  const CookieNames = { COOKIE_NOTICE: 'cookieNotice' };
  const Events = {
    CLICK: 'click',
    HIDDEN_BS_TOAST: 'hidden.bs.toast',
  };

  const $notices = $(Selector.NOTICE);
  const defaultOptions = {
    autoShow: false,
    autoShowDelay: 0,
    showOnce: false,
    cookieExpireTime: 3600000,
  };

  $notices.each((index, value) => {
    const $this = $(value);
    const options = $.extend(defaultOptions, $this.data(DataKeys.OPTIONS));
    let cookieNotice;
    if (options.showOnce) {
      cookieNotice = utils.getCookie(CookieNames.COOKIE_NOTICE);
    }
    if (options.autoShow && cookieNotice === null) {
      setTimeout(() => $this.toast('show'), options.autoShowDelay);
    }
  });

  $(Selector.NOTICE).on(Events.HIDDEN_BS_TOAST, (e) => {
    const $this = $(e.currentTarget);
    const options = $.extend(defaultOptions, $this.data(DataKeys.OPTIONS));
    options.showOnce &&
      utils.setCookie(
        CookieNames.COOKIE_NOTICE,
        false,
        options.cookieExpireTime
      );
  });

  utils.$document.on(Events.CLICK, Selector.DATA_TOGGLE_NOTICE, (e) => {
    e.preventDefault();
    const $this = $(e.currentTarget);
    const $target = $($this.attr('href'));
    $target.hasClass('show') ? $target.toast('hide') : $target.toast('show');
  });
});
