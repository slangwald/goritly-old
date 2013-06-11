$(document).ready ->

  #
  # The metric stuff
  #
  
  loadKpiBoard = () ->
    $('#kpi-board-content').html('<img src="/static/loading.gif" />')
    $('#kpi-board-content').load('/websites/kpi')
  loadKpiBoard()
  redrawWithOptions = () ->
    $.post("/websites/set_bar_options", $('#bar-chart-options').serialize()).done((data) ->
        drawBarNew()
    )
  
  doMetric = (e) ->
    $.post("/websites/set_metric", $(@).serialize()).done((data) ->
            drawBarNew()
            drawBubbleChart()
        )
  $("#omni-metric-left").change doMetric
  $("#omni-metric-right").change doMetric
  
  $("#bubble-metric-left").change doMetric
  $("#bubble-metric-right").change doMetric
  $("#bubble-metric-size").change doMetric

  $('select[name="omni-seperation"]').change (e) ->
    $.post("/websites/set_seperation", $(@).serialize() ).done((data) ->
        drawBarNew()
    )
  $('select[name="kpi-seperation"]').change (e) ->
    $.post("/websites/set_seperation", $(@).serialize() ).done((data) ->
        loadKpiBoard()
    )
  $('select[name="bubble-seperation"]').change (e) ->
    $.post("/websites/set_seperation", $(@).serialize() ).done((data) ->
        drawBubbleChart()
    )
    
  
  $('input[name="omni-days"]').keypress (e) ->
    if (e.which == 13)
      $.post("/websites/set_days", $(@).serialize() ).done((data) ->
          drawBarNew()
      )
      return false
  $('input[name="kpi-days"]').keypress (e) ->
    if (e.which == 13)
      $.post("/websites/set_days", $(@).serialize() ).done((data) ->
          loadKpiBoard()
      )
      return false
  $('input[name="bubble-days"]').keypress (e) ->
    if (e.which == 13)
      $.post("/websites/set_days", $(@).serialize() ).done((data) ->
          drawBubbleChart()
      )
      return false
      
      
  
  $('*[data-toggle="tooltip"]').tooltip()
  $("#timerange-value").hide()
  changeTimeRange = (e) ->
    el = @
    val = $(el).val()
    if val is 'today'
      $("#timerange-value").hide()
    else
      $("#timerange-value").show()
      $("#timerange-value").focus()
    redrawWithOptions()
    
  
  
      
  
  $('#timerange-unit').change changeTimeRange
  $('#timerange-value').blur redrawWithOptions
  
  #
  # Tabs
  #
  $('#charts-tabs a').click (e) ->
    $(@).tab('show')
    
    window.location.hash = '#!' + @.hash
    if $(@).attr('data-chart') == 'bar'
      drawBarNew()
    if $(@).attr('data-chart') == 'bubble'
      drawBubbleChart()  
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
            loadKpiBoard()
            drawBarNew()
        )
    )

  #
  # Init stuff
  #
  $('.chzn-select').chosen()
  loadSideBar()
  
  
    
