$(document).ready ->

  $('#kpi-board').load('/websites/kpi')
  
  #
  # The metric stuff
  #
  doMetric = (e) ->
    $.post("/websites/set_metric", $(@).serialize()).done((data) ->
            drawBarNew()
        )
  $("#metric-left").change doMetric
  $("#metric-right").change doMetric
  
  $('input[name="seperation"]').change (e) ->
    $.post("/websites/set_seperation", $(@).serialize() ).done((data) ->
        drawBarNew()
    )
  
  #
  # Tabs
  #
  $('#charts-tabs a').click (e) ->
    $(@).tab('show')
    
    window.location.hash = '#!' + @.hash
    if $(@).attr('data-chart') == 'bar'
        $.post("/websites/set_seperation", 'seperation=aggregated' ).done((data) ->
          drawBarNew()
        )
  #
  # Filter
  #
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

  #
  # Init stuff
  #
  $('.chzn-select').chosen()
  loadSideBar()
  
  
    
