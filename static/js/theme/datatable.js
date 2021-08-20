'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Data table
-----------------------------------------------*/
utils.$document.ready(() => {
  const dataTables = $('.data-table');
  const customDataTable = (elem) => {
    elem.find('.pagination').addClass('pagination-sm');
  };
  dataTables.length &&
    dataTables.each((index, value) => {
      const $this = $(value);
      const options = $.extend(
        {
          responsive: true,
          dom:
            "<'row mx-1'<'col-sm-12 col-md-6 px-3'l><'col-sm-12 col-md-6 px-3'f>>" +
            "<'table-responsive'tr>" +
            "<'row mx-1 align-items-center justify-content-center justify-content-md-between'<'col-auto mb-2 mb-sm-0'i><'col-auto'p>>",
        },
        $this.data('options')
      );
      $this.DataTable(options);
      const $wrpper = $this.closest('.dataTables_wrapper');
      customDataTable($wrpper);
      $this.on('draw.dt', () => customDataTable($wrpper));
    });
});
