// Generated by CoffeeScript 1.6.2
(function() {
  $(document).ready(function() {
    $('#charts-tabs a').click(function(e) {
      $(this).tab('show');
      if ($(this).attr('data-chart') === 'bubble') {
        drawBubbleChart();
      }
      if ($(this).attr('data-chart') === 'line') {
        drawLineChart();
      }
      if ($(this).attr('data-chart') === 'bar') {
        return drawBarChart();
      }
    });
    $('#sidebar').load('/websites/sidebar', function() {
      drawCalendar();
      return $('.chzn-select').chosen();
    });
    $('.chzn-select').chosen();
    return $('#kpi-board').load('/websites/kpi');
  });

}).call(this);
