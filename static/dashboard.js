var d3 = Plotly.d3;
var WIDTH_IN_PERCENT_OF_PARENT = 80,
    HEIGHT_IN_PERCENT_OF_PARENT = 100;

var colors = ['#ff7f0e','#1f77b4'];

function plot_payoff(X,Y,titles){

var ell = document.getElementById("plot-payoff")
var gd3 = d3.select(ell)
    .style({
        width: WIDTH_IN_PERCENT_OF_PARENT + '%',
        'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

        height: HEIGHT_IN_PERCENT_OF_PARENT + '%',
        'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + '%'
    });

var gd = gd3.node();

var data = [];
var index = 0;
for(i=0;i<Y.length;i++){

    var trace = {
        x: X,
        y: Y[i],
        mode: 'lines',
        type: 'scatter',
        line:{color:colors[index]},
        name:titles[index],
        //name:"Today",
    };
    var trace2 = {
        x: X,
        y: Y[i+1],
        mode: 'lines',
        type: 'scatter',
        line:{color:colors[index]},
        name:titles[index] + " / Last Day",
        //name:"Last Day",
    };
    data.push(trace);
    data.push(trace2);
    i++;
    index++;
}

var layout = {
  margin:{
    t: 90,
    b: 90,
    l: 60,
    r: 20,
  },
  xaxis: {
    //title: 'Spot',
    titlefont: {
      color: 'white'
    },
    tickfont: {
      color: 'white'
    },
  },
  yaxis: {
    title: 'Profit & Loss',
    titlefont: {
      color: 'white'
    },
    tickfont: {
      color: 'white'
    },
  },
  paper_bgcolor:'rgba(0,0,0,0)',
  plot_bgcolor:'rgba(0,0,0,0)',
  title:"Profit & Loss",
  titlefont: {
      size: 18,
      color: 'white',
    },
  showlegend: true,
  legend: {"orientation": "h",font:{color:'white'}},
  hovermode: true
};

plot = Plotly.plot(gd, data, layout, {showLink: false, displayModeBar: false});

$(window).resize(function(){
    Plotly.Plots.resize(gd);
});
}
