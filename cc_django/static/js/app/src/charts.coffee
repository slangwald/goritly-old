$(document).ready ->
  if $('#line-chart')
    lineData = [{"date":"2013-03-04","weeks":47,"detail":{"f":16,"d":16,"s":16}},{"date":"2013-03-05","weeks":46,"detail":{"f":15,"d":15,"s":15}},{"date":"2013-03-06","weeks":42,"detail":{"f":14,"d":14,"s":14}},{"date":"2013-03-07","weeks":40,"detail":{"f":13,"d":13,"s":13}},{"date":"2013-03-08","weeks":36,"detail":{"f":12,"d":12,"s":12}},{"date":"2013-03-09","weeks":35,"detail":{"f":12,"d":12,"s":12}},{"date":"2013-03-10","weeks":39,"detail":{"f":13,"d":13,"s":13}},{"date":"2013-03-11","weeks":44,"detail":{"f":15,"d":15,"s":15}},{"date":"2013-03-12","weeks":44,"detail":{"f":15,"d":15,"s":15}},{"date":"2013-03-13","weeks":39,"detail":{"f":13,"d":13,"s":13}},{"date":"2013-03-14","weeks":34,"detail":{"f":11,"d":11,"s":11}},{"date":"2013-03-15","weeks":29,"detail":{"f":10,"d":10,"s":10}},{"date":"2013-03-16","weeks":40,"detail":{"f":13,"d":13,"s":13}},{"date":"2013-03-17","weeks":43,"detail":{"f":14,"d":14,"s":14}},{"date":"2013-03-18","weeks":47,"detail":{"f":16,"d":16,"s":16}},{"date":"2013-03-19","weeks":51,"detail":{"f":17,"d":17,"s":17}},{"date":"2013-03-20","weeks":50,"detail":{"f":17,"d":17,"s":17}},{"date":"2013-03-21","weeks":55,"detail":{"f":18,"d":18,"s":18}},{"date":"2013-03-22","weeks":55,"detail":{"f":18,"d":18,"s":18}},{"date":"2013-03-23","weeks":53,"detail":{"f":18,"d":18,"s":18}},{"date":"2013-03-24","weeks":48,"detail":{"f":16,"d":16,"s":16}},{"date":"2013-03-25","weeks":53,"detail":{"f":18,"d":18,"s":18}}]
    data = lineData
    margin = {top: 20, right: 20, bottom: 30, left: 50}
    width = 970 - margin.left - margin.right
    height = 500 - margin.top - margin.bottom
    
    parseDate = d3.time.format("%Y-%m-%d").parse;
    
    x = d3.time
          .scale()
          .range([0, width])
    y = d3.scale.linear()
          .range([height, 0])
    
    xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom")
          
    yAxis = d3.svg.axis()
          .scale(y)
          .orient("left")
          .tickSize(-width, 0, 0)
          .tickFormat((d, i) -> d + " wks. " if i > 0)
    
    area = d3.svg.area()
          .x( (d) -> x(parseDate(d.date)) )
          .y0(height)
          .y1( (d) -> y(d.weeks) )
          .interpolate("monotone")
    
    area2 = d3.svg.area()
          .x( (d) -> x(parseDate(d.date)) )
          .y0(height)
          .y1( (d) -> y(+d.weeks) )
    
    svg = d3.select("#line-chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        
    x.domain(d3.extent(data, (d) ->
      parseDate(d.date)
    ))
    
    y.domain([0, d3.max(data, (d) -> 
      + d.weeks
    )+20])
    
      
    formatTime = d3.time.format("%Y-%m-%d")
    
    div = d3.select("body").append("div").attr('class', 'tooltipD3')
    
    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    
    svg.append("path")
       .datum(data)
       .attr("class", "area")
       .attr("d", area)
    
    line = d3.svg.line()
      .x((d) -> x(parseDate(d.date)))
      .y((d) -> y(d.weeks))
      .interpolate("monotone")
     
    svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line)
    
    dots = svg.selectAll("dot")    
        .data(data)
        .enter().append("circle")
        .attr("class", "infodot")
        .attr("r", 8)
        .attr("cx", (d) -> x(parseDate(d.date)))
        .attr("cy", (d) -> y(d.weeks))
        .on("mouseover", (d) ->       
          pos = $(@).position()
          $(@).attr('class', 'infodot-active')
          
          div.style('display', 'block')
          div.html(
            formatTime(parseDate(d.date)) + 
            '<br/><b>Total: ' + d.weeks + ' </b>' +
            '<br/>Facebook: ' + d.detail.f + 
            '<br/>Display: ' + d.detail.d + 
            '<br/>SEM: ' + d.detail.s 
          )
          .style("left", (pos.left) + "px")
          .style("top", (pos.top + 20) + "px")
        )    
        .on("mouseout", (d) ->
          $(@).attr('class', 'infodot')
          div.style('display', 'none')
        )
        
    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)

    
    
    
      
    
