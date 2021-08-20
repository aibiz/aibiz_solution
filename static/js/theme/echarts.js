"use strict";

import utils from "./Utils";

/*-----------------------------------------------
|  Echarts
-----------------------------------------------*/

const getPosition = (pos, params, dom, rect, size) => ({
  top: pos[1] - size.contentSize[1] - 10,
  left: pos[0] - size.contentSize[0] / 2,
});

utils.$document.ready(() => {
  const Events = { CHANGE: "change" };
  const Selector = {
    ECHART_LINE_TOTAL_ORDER: ".echart-line-total-order",
    ECHART_BAR_WEEKLY_SALES: ".echart-bar-weekly-sales",
    ECHART_LINE_TOTAL_SALES: ".echart-line-total-sales",
    SELECT_MONTH: ".select-month",
    ECHART_BAR_TOP_PRODUCTS: ".echart-bar-top-products",
    ECHART_WORLD_MAP: ".echart-world-map",
    ECHART_DOUGHNUT: ".echart-doughnut",
  };

  //
  // ─── TOTAL ORDER CHART ──────────────────────────────────────────────────────────
  //

  const $echartLineTotalOrder = document.querySelector(
    Selector.ECHART_LINE_TOTAL_ORDER
  );
  if ($echartLineTotalOrder) {
    const $this = $($echartLineTotalOrder);

    // Get options from data attribute
    const userOptions = $this.data("options");
    const chart = window.echarts.init($echartLineTotalOrder);

    // Default options
    const defaultOptions = {
      tooltip: {
        triggerOn: "mousemove",
        trigger: "axis",
        padding: [7, 10],
        formatter: "{b0}: {c0}",
        backgroundColor: utils.grays.white,
        borderColor: utils.grays["300"],
        borderWidth: 1,
        transitionDuration: 0,
        position(pos, params, dom, rect, size) {
          return getPosition(pos, params, dom, rect, size);
        },
        textStyle: { color: utils.colors.dark },
      },
      xAxis: {
        type: "category",
        data: ["Week 4", "Week 5"],
        boundaryGap: false,
        splitLine: { show: false },
        axisLine: {
          show: false,
          lineStyle: {
            color: utils.grays["300"],
            type: "dashed",
          },
        },
        axisLabel: { show: false },
        axisTick: { show: false },
        axisPointer: { type: "none" },
      },
      yAxis: {
        type: "value",
        splitLine: { show: false },
        axisLine: { show: false },
        axisLabel: { show: false },
        axisTick: { show: false },
        axisPointer: { show: false },
      },
      series: [
        {
          type: "line",
          lineStyle: {
            color: utils.colors.primary,
            width: 3,
          },
          itemStyle: {
            color: utils.grays.white,
            borderColor: utils.colors.primary,
            borderWidth: 2,
          },
          hoverAnimation: true,
          data: [20, 130],
          connectNulls: true,
          smooth: 0.6,
          smoothMonotone: "x",
          symbol: "circle",
          symbolSize: 8,
          areaStyle: {
            color: {
              type: "linear",
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                {
                  offset: 0,
                  color: utils.rgbaColor(utils.colors.primary, 0.25),
                },
                {
                  offset: 1,
                  color: utils.rgbaColor(utils.colors.primary, 0),
                },
              ],
            },
          },
        },
      ],
      grid: { bottom: "2%", top: "0%", right: "10px", left: "10px" },
    };

    // Merge options using lodash
    const options = window._.merge(defaultOptions, userOptions);
    chart.setOption(options);
  }

  //
  // ─── WEEKLY SALES CHART ─────────────────────────────────────────────────────────
  //
  const $echartBarWeeklySales = document.querySelector(
    Selector.ECHART_BAR_WEEKLY_SALES
  );
  if ($echartBarWeeklySales) {
    const $this = $($echartBarWeeklySales);

    // Get options from data attribute
    const userOptions = $this.data("options");

    const data = [120, 200, 150, 80, 70, 110, 120];

    // Max value of data
    const yMax = Math.max(...data);

    const dataBackground = data.map(() => yMax);
    const chart = window.echarts.init($echartBarWeeklySales);

    // Default options
    const defaultOptions = {
      tooltip: {
        trigger: "axis",
        padding: [7, 10],
        formatter: "{b1}: {c1}",
        backgroundColor: utils.grays.white,
        borderColor: utils.grays["300"],
        borderWidth: 1,
        textStyle: { color: utils.colors.dark },
        transitionDuration: 0,
        position(pos, params, dom, rect, size) {
          return getPosition(pos, params, dom, rect, size);
        },
      },
      xAxis: {
        type: "category",
        data: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        boundaryGap: false,
        axisLine: { show: false },
        axisLabel: { show: false },
        axisTick: { show: false },
        axisPointer: { type: "none" },
      },
      yAxis: {
        type: "value",
        splitLine: { show: false },
        axisLine: { show: false },
        axisLabel: { show: false },
        axisTick: { show: false },
        axisPointer: { type: "none" },
      },
      series: [
        {
          type: "bar",
          barWidth: "5px",
          barGap: "-100%",
          itemStyle: {
            color: utils.grays["200"],
            barBorderRadius: 10,
          },
          data: dataBackground,
          animation: false,
          emphasis: { itemStyle: { color: utils.grays["200"] } },
        },
        {
          type: "bar",
          barWidth: "5px",
          itemStyle: {
            color: utils.colors.primary,
            barBorderRadius: 10,
          },
          data: data,
          emphasis: { itemStyle: { color: utils.colors.primary } },
          z: 10,
        },
      ],
      grid: { right: 5, left: 10, top: 0, bottom: 0 },
    };

    // Merge user options with lodash
    const options = window._.merge(defaultOptions, userOptions);
    chart.setOption(options);
  }

  //
  // ─── EHCART LINE TOTAL SALES ────────────────────────────────────────────────────────────────
  //

  const $echartsLineTotalSales = document.querySelector(
    Selector.ECHART_LINE_TOTAL_SALES
  );
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  function getFormatter(params) {
    const { name, value } = params[0];
    var date = new Date(name);
    return `${months[0]} ${date.getDate()}, ${value}`;
  }
  if ($echartsLineTotalSales) {
    const $this = $($echartsLineTotalSales);

    // Get options from data attribute
    const userOptions = $this.data("options");
    const chart = window.echarts.init($echartsLineTotalSales);
    const monthsnumber = [
      [60, 80, 60, 80, 65, 130, 120, 100, 30, 40, 30, 70],
      [100, 70, 80, 50, 120, 100, 130, 140, 90, 100, 40, 50],
      [80, 50, 60, 40, 60, 120, 100, 130, 60, 80, 50, 60],
      [70, 80, 100, 70, 90, 60, 80, 130, 40, 60, 50, 80],
      [90, 40, 80, 80, 100, 140, 100, 130, 90, 60, 70, 50],
      [80, 60, 80, 60, 40, 100, 120, 100, 30, 40, 30, 70],
      [20, 40, 20, 50, 70, 60, 110, 80, 90, 30, 50, 50],
      [60, 70, 30, 40, 80, 140, 80, 140, 120, 130, 100, 110],
      [90, 90, 40, 60, 40, 110, 90, 110, 60, 80, 60, 70],
      [50, 80, 50, 80, 50, 80, 120, 80, 50, 120, 110, 110],
      [60, 90, 60, 70, 40, 70, 100, 140, 30, 40, 30, 70],
      [20, 40, 20, 50, 30, 80, 120, 100, 30, 40, 30, 70],
    ];
    const defaultOptions = {
      color: utils.grays.white,
      tooltip: {
        trigger: "axis",
        padding: [7, 10],
        backgroundColor: utils.grays.white,
        borderColor: utils.grays["300"],
        borderWidth: 1,
        textStyle: { color: utils.colors.dark },
        formatter(params) {
          return getFormatter(params);
        },
        transitionDuration: 0,
        position(pos, params, dom, rect, size) {
          return getPosition(pos, params, dom, rect, size);
        },
      },
      xAxis: {
        type: "category",
        data: [
          "2019-01-05",
          "2019-01-06",
          "2019-01-07",
          "2019-01-08",
          "2019-01-09",
          "2019-01-10",
          "2019-01-11",
          "2019-01-12",
          "2019-01-13",
          "2019-01-14",
          "2019-01-15",
          "2019-01-16",
        ],
        boundaryGap: false,
        axisPointer: {
          lineStyle: {
            color: utils.grays["300"],
            type: "dashed",
          },
        },
        splitLine: { show: false },
        axisLine: {
          lineStyle: {
            // color: utils.grays['300'],
            color: utils.rgbaColor("#000", 0.01),
            type: "dashed",
          },
        },
        axisTick: { show: false },
        axisLabel: {
          color: utils.grays["400"],
          formatter: function (value) {
            var date = new Date(value);
            return `${months[date.getMonth()]} ${date.getDate()}`;
          },
          margin: 15,
        },
      },
      yAxis: {
        type: "value",
        axisPointer: { show: false },
        splitLine: {
          lineStyle: {
            color: utils.grays["300"],
            type: "dashed",
          },
        },
        boundaryGap: false,
        axisLabel: {
          show: true,
          color: utils.grays["400"],
          margin: 15,
        },
        axisTick: { show: false },
        axisLine: { show: false },
      },
      series: [
        {
          type: "line",
          data: monthsnumber[0],
          lineStyle: { color: utils.colors.primary },
          itemStyle: {
            borderColor: utils.colors.primary,
            borderWidth: 2,
          },
          symbol: "circle",
          symbolSize: 10,
          smooth: false,
          hoverAnimation: true,
          areaStyle: {
            color: {
              type: "linear",
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                {
                  offset: 0,
                  color: utils.rgbaColor(utils.colors.primary, 0.2),
                },
                {
                  offset: 1,
                  color: utils.rgbaColor(utils.colors.primary, 0),
                },
              ],
            },
          },
        },
      ],
      grid: { right: "28px", left: "40px", bottom: "15%", top: "5%" },
    };

    const options = window._.merge(defaultOptions, userOptions);
    chart.setOption(options);

    // Change chart options accordiong to the selected month
    utils.$document.on(Events.CHANGE, Selector.SELECT_MONTH, (e) => {
      const $field = $(e.target);
      const month = $field.val();
      const data = monthsnumber[month];

      chart.setOption({
        tooltip: {
          formatter: function (params) {
            const { name, value } = params[0];
            var date = new Date(name);
            return `${months[month]} ${date.getDate()}, ${value}`;
          },
        },
        xAxis: {
          axisLabel: {
            formatter: function (value) {
              var date = new Date(value);
              return `${months[$field.val()]} ${date.getDate()}`;
            },
            margin: 15,
          },
        },
        series: [{ data: data }],
      });
    });
  }

  //
  // ─── BAR CHART TOP PRODUCTS ──────────────────────────────────────────────────────────────────
  //
  const $echartBarTopProducts = document.querySelector(
    Selector.ECHART_BAR_TOP_PRODUCTS
  );

  if ($echartBarTopProducts) {
    const data = [
      ["product", "2019", "2018"],
      ["Boots4", 43, 85],
      ["Reign Pro", 83, 73],
      ["Slick", 86, 62],
      ["Falcon", 72, 53],
      ["Sparrow", 80, 50],
      ["Hideway", 50, 70],
      ["Freya", 80, 90],
      // ['Raven Pro', 60, 70],
      // ['Posh', 80, 70],
    ];
    const $this = $($echartBarTopProducts);
    const userOptions = $this.data("options");
    const chart = window.echarts.init($echartBarTopProducts);

    const defaultOptions = {
      color: [utils.colors.primary, utils.grays["300"]],
      dataset: { source: data },
      tooltip: {
        trigger: "item",
        padding: [7, 10],
        backgroundColor: utils.grays.white,
        borderColor: utils.grays["300"],
        borderWidth: 1,
        textStyle: { color: utils.colors.dark },
        transitionDuration: 0,
        position(pos, params, dom, rect, size) {
          return getPosition(pos, params, dom, rect, size);
        },
        formatter: function (params) {
          return `<div class="font-weight-semi-bold">${
            params.seriesName
          }</div><div class="fs--1 text-600"><strong>${params.name}:</strong> ${
            params.value[params.componentIndex + 1]
          }</div>`;
        },
      },
      legend: {
        data: ["2019", "2018"],
        left: "left",
        itemWidth: 10,
        itemHeight: 10,
        borderRadius: 0,
        icon: "circle",
        inactiveColor: utils.grays["500"],
        textStyle: { color: utils.grays["700"] },
      },
      xAxis: {
        type: "category",
        axisLabel: { color: utils.grays["400"] },
        axisLine: {
          lineStyle: {
            color: utils.grays["300"],
            type: "dashed",
          },
        },
        axisTick: false,
        boundaryGap: true,
      },
      yAxis: {
        axisPointer: { type: "none" },
        axisTick: "none",
        splitLine: {
          lineStyle: {
            color: utils.grays["300"],
            type: "dashed",
          },
        },
        axisLine: { show: false },
        axisLabel: { color: utils.grays["400"] },
      },
      series: [
        {
          type: "bar",
          barWidth: "12%",
          barGap: "30%",
          label: { normal: { show: false } },
          z: 10,
          itemStyle: {
            normal: {
              barBorderRadius: [10, 10, 0, 0],
              color: utils.colors.primary,
            },
          },
        },
        {
          type: "bar",
          barWidth: "12%",
          barGap: "30%",
          label: { normal: { show: false } },
          itemStyle: {
            normal: {
              barBorderRadius: [4, 4, 0, 0],
              color: utils.grays[300],
            },
          },
        },
      ],
      grid: { right: "0", left: "30px", bottom: "10%", top: "20%" },
    };

    const options = window._.merge(defaultOptions, userOptions);
    chart.setOption(options);
  }

  //
  // ─── PIE CHART ──────────────────────────────────────────────────────────────────
  //
  const $pieChartRevenue = document.querySelector(Selector.ECHART_DOUGHNUT);
  if ($pieChartRevenue) {
    const $this = $($pieChartRevenue);
    const userOptions = $this.data("options");
    const chart = window.echarts.init($pieChartRevenue);

    const defaultOptions = {
      color: [utils.colors.primary, utils.colors.info, utils.grays[300]],
      tooltip: {
        trigger: "item",
        padding: [7, 10],
        backgroundColor: utils.grays.white,
        textStyle: { color: utils.grays.black },
        transitionDuration: 0,
        borderColor: utils.grays["300"],
        borderWidth: 1,
        formatter: function (params) {
          return `<strong>${params.data.name}:</strong> ${params.percent}%`;
        },
      },
      position(pos, params, dom, rect, size) {
        return getPosition(pos, params, dom, rect, size);
      },
      legend: { show: false },
      series: [
        {
          type: "pie",
          radius: ["100%", "87%"],
          avoidLabelOverlap: false,
          hoverAnimation: false,
          itemStyle: {
            borderWidth: 2,
            borderColor: utils.grays.white,
          },
          label: {
            normal: {
              show: false,
              position: "center",
              textStyle: {
                fontSize: "20",
                fontWeight: "500",
                color: utils.grays["700"],
              },
            },
            emphasis: {
              show: false,
            },
          },
          labelLine: { normal: { show: false } },
          data: [
            { value: 5300000, name: "Samsung" },
            { value: 1900000, name: "Huawei" },
            { value: 2000000, name: "Apple" },
          ],
        },
      ],
    };

    const options = window._.merge(defaultOptions, userOptions);
    chart.setOption(options);
  }

  //
  // ─── ECHART FIX ON WINDOW RESIZE ────────────────────────────────────────────────
  //
  const $echarts = document.querySelectorAll("[data-echart-responsive]");
  window.onresize = () => {
    if (!!$echarts.length) {
      $.each($echarts, (item, value) => {
        if (!!$(value).data("echart-responsive")) {
          window.echarts.init(value).resize();
        }
      });
    }
  };
});
