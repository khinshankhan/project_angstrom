var svg_height = document.getElementsByTagName("svg")[0].clientHeight;
var svg_width = document.getElementsByTagName("svg")[0].clientWidth;
var svg_id = document.getElementsByTagName("svg")[0].id;

var svg = d3.select("svg"),
    margin = {top: 10, right: 10, bottom: 50, left: 30},
    width = svg_width - margin.left - margin.right,
    height = svg_height - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var x = d3.scaleLinear().range([0, width]),
    y = d3.scaleLinear().range([height, 0]),
    z = d3.scaleOrdinal(d3.schemeCategory10);

var line = d3.line()
    .x(function(d) { return x(d[0]); })
    .y(function(d) { return y(d[1]); });

$.ajax({
    url: svg_id,
    success: function(result){
      result = JSON.parse(result);
      console.log(result);
      chart(result);
    }
});

var chart = function(teams) {

  x.domain(d3.extent(teams[0].values, function(d) { return parseInt(d[0])**(1+1/d[0])-d[0]*.2; }));

  y.domain([0,
            d3.max(teams, function(c) { return d3.max(c.values, function(d) { return parseInt(d[1]); }); })
  ]);

  z.domain(teams.map(function(c) { return c.id; }));

  g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
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
    .text("OPR");

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
