$(document).ready ->
  $('#charts-tabs a').click (e) ->     
    $(@).tab('show')

  $('#charts-tabs a:last').tab('show');
