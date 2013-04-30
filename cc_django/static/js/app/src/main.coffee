$(document).ready ->
  
  #$('#btn-filter').click (e) ->
    #e.preventDefault()
    #$.post("/websites/filter", $("#filter-form").serialize()).done((data) ->
    #  alert(data)  
    #)
  
  $('#charts-tabs a').click (e) ->     
    $(@).tab('show')
    
    if $(@).attr('data-chart') == 'bubble'
      drawBubbleChart()
     
    if $(@).attr('data-chart') == 'line'
      drawLineChart()
        
    if $(@).attr('data-chart') == 'bar'
      drawBarChart()
    
    
  #$('#charts-tabs a:last').tab('show')
  $('.chzn-select').chosen()
  #drawBubbleChart()
  drawLineChart()