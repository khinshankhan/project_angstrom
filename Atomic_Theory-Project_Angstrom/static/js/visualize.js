var svg = d3.select("svg"),
    margin = {top: 20, right: 80, bottom: 50, left: 50},
    width = svg.attr("width") - margin.left - margin.right,
    height = svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var x = d3.scaleLinear().range([0, width]),
    y = d3.scaleLinear().range([height, 0]),
    z = d3.scaleOrdinal(d3.schemeCategory10);

var line = d3.line()
    .x(function(d) { return x(d.match); })
    .y(function(d) { return y(d.opr); });

d3.csv("static/data/data.csv", function(error, data) {
  if (error) throw error;

  var teams = data.columns.slice(1).map(function(id) {
    return {
      id: id,
      values: data.map(function(d) {
        return {match: d.match, opr: d[id]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return parseInt(d.match)**(1+1/d.match)-1; }));

  y.domain([0,
            d3.max(teams, function(c) { return d3.max(c.values, function(d) { return parseInt(d.opr); }); })
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
    .attr("transform", function(d) { return "translate(" + x(d.value.match) + "," + y(d.value.opr) + ")"; })
    .attr("x", 3)
    .attr("dy", "0.35em")
    .style("font", "10px sans-serif")
    .text(function(d) { return d.id; });

});
