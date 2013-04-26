$(document).ready ->
  $('#charts-tabs a').click (e) ->     
    $(@).tab('show')
    
    if $(@).attr('data-chart') == 'bubble'
      drawBubbleChart()
    
  #$('#charts-tabs a:last').tab('show')
  $('.chzn-select').chosen()
  drawBubbleChart()
