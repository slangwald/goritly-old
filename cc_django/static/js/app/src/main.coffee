$(document).ready ->
  
  $('#charts-tabs a').click (e) ->     
    $(@).tab('show')
    
    window.location.hash = '#!' + @.hash
    if $(@).attr('data-chart') == 'bubble'
      drawBubbleChart()
     
    if $(@).attr('data-chart') == 'line'
      drawLineChart()
        
    if $(@).attr('data-chart') == 'bar'
      drawBarChart()
    
    
  #$('#charts-tabs a:last').tab('show')
  #drawLineChart()
  loadSideBar = () ->
    $('#sidebar').load('/websites/sidebar', () -> 
      drawCalendar()
      $('.chzn-select').chosen()
      $('#btn-filter').click (e) ->
        e.preventDefault()
        $.post("/websites/filter", $("#filter-form").serialize()).done((data) ->
            
            $('#kpi-board').load('/websites/kpi')
            drawBubbleChart()
            drawLineChart()
            drawBarChart()
        )
    )
  loadSideBar()  
  $('.chzn-select').chosen()
  #drawBubbleChart()
  #drawBarChart()
  $('#kpi-board').load('/websites/kpi')
  
    
