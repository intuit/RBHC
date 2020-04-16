var treeData = [];
// ************** Generate the dropdown menu adn i	 *****************
var filename,options;
var data=[] ;


var select = d3.select('.list')
       .append('select')
         .attr('class','select')
         .on('change',onchange)

d3.json("models.txt", function(error, list) {
      data=list
      data.unshift("Chose model")
      options = select
          .selectAll('option')
          .data(data).enter()
          .append('option')
          .text(function (d) { return d; });
});

function onchange() {
  selectValue = d3.select('select').property('value')
  filename=selectValue+".json"
  d3.select('svg').remove();
  d3.json(filename, function(error, treedata) {
    root = treedata[0];
    width=root['width']*300
    height=root['height']*240
    tree = d3.layout.tree()
       .size([width, height])
    svg = d3.select("body").append("svg")
       	.attr("width", width + margin.right + margin.left)
       	.attr("height", height + margin.top + margin.bottom)
         .append("g")
       	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    root.x0 = width / 2
    root.y0 = 0;
    update(root);
    });
  d3.select('body')
  .append('p')

  };


// ************** Generate the tree diagram	 *****************
var margin = {top: 40, right: 120, bottom: 20, left: 260},
	width =500 - margin.right - margin.left,
	height = 200 - margin.top - margin.bottom;
var i = 0,
	duration = 750,
	root;
var nodeWidth = 10;
var nodeHeight = 300;
var horizontalSeparationBetweenNodes = 128;
var verticalSeparationBetweenNodes = 16;
var tree;
var svg;

var diagonal = d3.svg.diagonal()
	.projection(function(d) { return [d.x, d.y]; });


d3.select(self.frameElement).style("height", "500px");
function update(source) {
  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
	  links = tree.links(nodes);
  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 200; });

  // Update the nodes…
  var node = svg.selectAll("g.node")
	  .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append("g")
	  .attr("class", "node")
	  .attr("transform", function(d) { return "translate(" + source.x0 + "," + source.y0 + ")"; })
	  .on("click", click);

  nodeEnter.append("circle")
	  .attr("r", 1e-6)
    .style("stroke", function(d) { return d.alert_color; })
	  .style("fill", function(d) { return d._children ? d.alert_color : "#fff"; });

  function wordwrap2(text) {
     var lines=text.split(",")
     return lines
  }
  nodeEnter.append("text")
	  .attr("text-anchor","start")
    .each(function (d) {
       if (d.desc!=undefined) {
          var lines = wordwrap2(d.desc)
          for (var i = 0; i < lines.length; i++) {
             d3.select(this).append("tspan")
             .attr("x",13)
           .attr("dy",20)
                  .text(lines[i])
           }
        }
      })
	  .style("fill-opacity", 1e-6);



  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
	  .duration(duration)
	  .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  nodeUpdate.select("circle")
	  .attr("r", function(d) { return (18)})
    .style("stroke", function(d) { return d.alert_color; })
	  .style("fill", function(d) { return d._children ? d.alert_color : "#fff"; });

  nodeUpdate.select("text")
	  .style("fill-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
	  .duration(duration)
	  .attr("transform", function(d) { return "translate(" + source.x + "," + source.y + ")"; })
	  .remove();

  nodeExit.select("circle")
	  .attr("r", 1e-6);

  nodeExit.select("text")
	  .style("fill-opacity", 1e-6);

  // Update the links…
  var link = svg.selectAll("path.link")
	  .data(links, function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("path", "g")
	  .attr("class", "link")
    .style("stroke", function(d) { return d.target.line_color; })
	  .attr("d", function(d) {
		var o = {x: source.x0, y: source.y0};
		return diagonal({source: o, target: o});
	  });

  // Transition links to their new position.
  link.transition()
	  .duration(duration)
	  .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
	  .duration(duration)
	  .attr("d", function(d) {
		var o = {x: source.x, y: source.y};
		return diagonal({source: o, target: o});
	  })
	  .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
	d.x0 = d.x;
	d.y0 = d.y;
  });
}

// Toggle children on click.
function click(d) {
  if (d.children) {
	d._children = d.children;
	d.children = null;
  } else {
	d.children = d._children;
	d._children = null;
  }
  update(d);
}
