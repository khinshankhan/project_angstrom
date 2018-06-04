document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.carousel');
  console.log(elems);
  var instances = M.Carousel.init(elems, {
    fullWidth: true
  });

  var instance = instances[0];
  var next_button = document.getElementById("next_button");
  var prev_button = document.getElementById("prev_button");

  next_button.addEventListener("click", function() {
    instance.next();
  });

  prev_button.addEventListener("click", function() {
    instance.prev();
  });

  for (var i = 0; i < document.getElementsByTagName("svg").length; i++) {

    let svgDOM = document.getElementsByTagName("svg")[i];
    let svg_id = svgDOM.id;

    let svg = d3.select(svgDOM);

    $.ajax({
      url: svg_id,
      success: function(result){
        result = JSON.parse(result);
        if (result['data'][0].values.length > 0 && result['data'][0].values[0][1] != null) {
          chart(result['data'], svgDOM, svg, result['name']);
        } else {
          show_default(svgDOM, svg);
        }
      }
    });
  }
});

var chart = function(teams, svgDOM, svg, name) {

  var svg_height = svgDOM.clientHeight;
  var svg_width = svgDOM.clientWidth;
  var svg_id = svgDOM.id;

  var margin = {top: 10, right: 10, bottom: 50, left: 35},
      width = svg_width - margin.left - margin.right,
      height = svg_height - margin.top - margin.bottom,
      g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var x = d3.scaleLinear().range([0, width]),
      y = d3.scaleLinear().range([height, 0]),
      z = d3.scaleOrdinal(d3.schemeCategory10);

  var line = d3.line()
      .x(function(d) { return x(d[0]); })
      .y(function(d) { return y(d[1]); });

  x.domain(d3.extent(teams[0].values, function(d) { return parseInt(d[0])**(1+1/d[0])-d[0]*.2; }));

  y.domain([0,
            d3.max(teams, function(c) { return d3.max(c.values, function(d) { return parseFloat(d[1]) * 1.1; }); })
           ]);

  z.domain(teams.map(function(c) { return c.id; }));

  g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).ticks(teams[0].values.length))
    .append("text")
    .attr("transform", "translate(" + width/2 + ",0)")
    .attr("y", 30)
    .attr("dy", "0.71em")
    .attr("fill", "#000")
    .text("Match");

  g.append("g")
    .attr("class", "axis axis--y")
    .call(d3.axisLeft(y))
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", "0.71em")
    .attr("fill", "#000")
    .text(name);

  var team = g.selectAll(".team")
      .data(teams)
      .enter().append("g")
      .attr("class", "team");

  team.append("path")
    .attr("class", "line")
    .attr("d", function(d) { return line(d.values); })
    .style("stroke", function(d) { return z(d.id); });

  team.append("text")
    .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
    .attr("transform", function(d) { return "translate(" + x(d.value[0]) + "," + y(d.value[1]) + ")"; })
    .attr("x", 3)
    .attr("dy", "0.35em")
    .style("font", "10px sans-serif")
    .text(function(d) { return d.id; });
}

var show_default = function(svgDOM, svg) {

  var svg_height = svgDOM.clientHeight;
  var svg_width = svgDOM.clientWidth;

  var margin = {top: 10, right: 10, bottom: 50, left: 30},
      width = svg_width - margin.left - margin.right,
      height = svg_height - margin.top - margin.bottom;

  svg.append("text")
    .attr("x", margin.left)
    .attr("y", margin.top)
    .text("No graph could be drawn from the available data.");
}
