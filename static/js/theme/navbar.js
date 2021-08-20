'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Navbar
-----------------------------------------------*/

utils.$document.ready(() => {
  const { $window } = utils;
  let navDropShadowFlag = true;
  const ClassName = {
    SHOW: 'show',
    NAVBAR_GLASS_SHADOW: 'navbar-glass-shadow',
    NAVBAR_VERTICAL_COLLAPSED: 'navbar-vertical-collapsed',
    NAVBAR_VERTICAL_COLLAPSE_HOVER: 'navbar-vertical-collapsed-hover',
  };
  const Selector = {
    HTML: 'html',
    NAVBAR: '.navbar:not(.navbar-vertical)',
    NAVBAR_VERTICAL: '.navbar-vertical',
    NAVBAR_VERTICAL_TOGGLE: '.navbar-vertical-toggle',
    NAVBAR_VERTICAL_COLLAPSE: '#navbarVerticalCollapse',
    NAVBAR_VERTICAL_CONTENT: '.navbar-vertical-content',
    NAVBAR_VERTICAL_COLLAPSED: '.navbar-vertical-collapsed',
    NAVBAR_VERTICAL_DROPDOWN_NAV: '.navbar-vertical .navbar-collapse .nav',
    NAVBAR_VERTICAL_COLLAPSED_DROPDOWN_NAV:
      '.navbar-vertical-collapsed .navbar-vertical .navbar-collapse .nav',
    MAIN_CONTENT: '.main .content',
    NAVBAR_TOP: '.navbar-top',
    OWL_CAROUSEL: '.owl-carousel',
    ECHART_RESPONSIVE: '[data-echart-responsive]',
  };
  const Events = {
    LOAD_SCROLL: 'load scroll',
    SCROLL: 'scroll',
    CLICK: 'click',
    RESIZE: 'resize',
    SHOW_BS_COLLAPSE: 'show.bs.collapse',
    HIDDEN_BS_COLLAPSE: 'hidden.bs.collapse',
  };
  const $html = $(Selector.HTML);
  const $navbar = $(Selector.NAVBAR);
  const $navbarVerticalCollapse = $(Selector.NAVBAR_VERTICAL_COLLAPSE);
  const $navbarVerticalContent = $(Selector.NAVBAR_VERTICAL_CONTENT);
  const navbarVertical = $(Selector.NAVBAR_VERTICAL);
  const breakPoint = utils.getBreakpoint(navbarVertical);

  const setDropShadow = ($elem) => {
    if ($elem.scrollTop() > 0 && navDropShadowFlag) {
      $navbar.addClass(ClassName.NAVBAR_GLASS_SHADOW);
    } else {
      $navbar.removeClass(ClassName.NAVBAR_GLASS_SHADOW);
    }
  };
  $window.on(Events.LOAD_SCROLL, () => setDropShadow($window));
  $navbarVerticalContent.on('scroll', () => {
    if ($window.width() < breakPoint) {
      navDropShadowFlag = true;
      setDropShadow($navbarVerticalContent);
    }
  });
  $navbarVerticalCollapse.on(Events.SHOW_BS_COLLAPSE, () => {
    if ($window.width() < breakPoint) {
      navDropShadowFlag = false;
      setDropShadow($window);
    }
  });
  $navbarVerticalCollapse.on(Events.HIDDEN_BS_COLLAPSE, () => {
    if (
      $navbarVerticalCollapse.hasClass(ClassName.SHOW) &&
      $window.width() < breakPoint
    ) {
      navDropShadowFlag = false;
    } else {
      navDropShadowFlag = true;
    }
    setDropShadow($window);
  });

  // Expand or Collapse vertical navbar on mouse over and out
  $navbarVerticalCollapse.hover(
    (e) => {
      setTimeout(() => {
        if ($(e.currentTarget).is(':hover')) {
          $(Selector.NAVBAR_VERTICAL_COLLAPSED).addClass(
            ClassName.NAVBAR_VERTICAL_COLLAPSE_HOVER
          );
        }
      }, 100);
    },
    () => {
      $(Selector.NAVBAR_VERTICAL_COLLAPSED).removeClass(
        ClassName.NAVBAR_VERTICAL_COLLAPSE_HOVER
      );
    }
  );

  // Set navbar top width from content
  const setNavbarWidth = () => {
    const contentWidth = $(Selector.MAIN_CONTENT).width() + 30;
    $(Selector.NAVBAR_TOP).outerWidth(contentWidth);
  };

  // Toggle navbar vertical collapse on click
  utils.$document.on(Events.CLICK, Selector.NAVBAR_VERTICAL_TOGGLE, (e) => {
    // Set collapse state on localStorage
    const isNavbarVerticalCollapsed = JSON.parse(
      localStorage.getItem('isNavbarVerticalCollapsed')
    );
    localStorage.setItem(
      'isNavbarVerticalCollapsed',
      !isNavbarVerticalCollapsed
    );

    // Toggle class
    $html.toggleClass(ClassName.NAVBAR_VERTICAL_COLLAPSED);

    // Set navbar top width
    setNavbarWidth();

    // Refresh Echarts
    const $echarts = document.querySelectorAll(Selector.ECHART_RESPONSIVE);
    if (!!$echarts.length) {
      $.each($echarts, (item, value) => {
        if (!!$(value).data('echart-responsive')) {
          window.echarts.init(value).resize();
        }
      });
    }
    $(e.currentTarget).trigger('navbar.vertical.toggle');
  });

  // Set navbar top width on window resize
  $window.on(Events.RESIZE, () => {
    setNavbarWidth();
  });
});
