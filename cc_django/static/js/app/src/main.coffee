$(document).ready ->
  
  $('#charts-tabs a').click (e) ->     
    $(@).tab('show')
    
    window.location.hash = '#!' + @.hash
    if $(@).attr('data-chart') == 'bar'
      drawBarNew()
    
  loadSideBar = () ->
    $('#sidebar').load('/websites/sidebar', () -> 
      drawCalendar()
      $('.chzn-select').chosen()
      $('#btn-filter').click (e) ->
        e.preventDefault()
        $.post("/websites/filter", $("#filter-form").serialize()).done((data) ->
            $('#kpi-board').load('/websites/kpi')
            drawBarNew()
        )
    )
  loadSideBar()
  $('.chzn-select').chosen()
  $('#kpi-board').load('/websites/kpi')
  
  $('#mark').change((e) ->
    $.post("/websites/mark", $("#mark").serialize()).done((data) ->
      #drawLineChart()
    )
  )
  
    
