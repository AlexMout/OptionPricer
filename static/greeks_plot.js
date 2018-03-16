
var WIDTH_IN_PERCENT_OF_PARENT = 100, HEIGHT_IN_PERCENT_OF_PARENT = 100;
var gd, gd2, plot;

//Function that produces all the charts in a single column
function graph_greeks_one_leg(X,list_Y,list_title){
	for(var i=0;i<2;i++){
		//Create a div for the 2 two graphs : 
		$("#greeks-div").append("<div id='grid" + i.toString() + "'></div>");

		//Select the new div created :
		var d3 = Plotly.d3;
		var ell = document.getElementById("grid" + i.toString());
		var gd3 = d3.select(ell)
	    .style({
	        width: WIDTH_IN_PERCENT_OF_PARENT + '%',
	        'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

	        height: HEIGHT_IN_PERCENT_OF_PARENT + '%',
	        'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + '%'
	    });

	    var trace = {
	    	x: X,
	    	y: list_Y[4*i],
	    	xaxis: 'x',
	    	yaxis: 'y',
	    	name:"Now",
	    	line:{color: 'rgba(86,148,230,0.8)'},
	    	type: 'scatter',
	    };
	    var trace2 = {
	    	x: X,
	    	y: list_Y[4*i+1],
	    	xaxis: 'x',
	    	yaxis: 'y',
	    	name:"Last Day",
	    	line:{color: 'rgba(86,148,230,0.8)'},
	    	type: 'scatter',
	    };
	    var trace3 = {
	    	x: X,
	    	y: list_Y[4*i+2],
	    	xaxis: 'x2',
	    	yaxis: 'y2',
	    	name:"Now",
	    	line:{color: 'rgba(242,42,258,0.8)'},
	    	type: 'scatter',
	    };
	    var trace4 = {
	    	x: X,
	    	y: list_Y[4*i+3],
	    	xaxis: 'x2',
	    	yaxis: 'y2',
	    	name:"Last Day",
	    	line:{color: 'rgba(242,42,258,0.8)'},
	    	type: 'scatter',
	    };
	    
	    var data = [trace,trace2,trace3,trace4];

        i = i==1 ? 2 : i;
	    var layout = {
	      showlegend:false,
	      xaxis: {
	      	titlefont: {
	      	    color: 'white'},
	      	 tickfont: {
	      	    color: 'white'},
	      },
	      xaxis2: {
	      	anchor: 'y2',
	      	titlefont: {
	      	    color: 'white'},
	      	 tickfont: {
	      	    color: 'white'},
	      },
	      yaxis: {
	      	domain: [0, 0.45],
	      	title:list_title[i],
	      	titlefont: {
	      	    color: 'white'},
	      	 tickfont: {
	      	    color: 'white'},
	      },
	      yaxis2: {
	      	domain: [0.55, 1],
	      	title:list_title[i+1],
	      	titlefont: {
	      	    color: 'white'},
	      	 tickfont: {
	      	    color: 'white'},
	      },
	      paper_bgcolor:'rgba(0,0,0,0)',
          plot_bgcolor:'rgba(0,0,0,0)',
	      margin:{
	        t: 0,
	        b: 40,
	        l: 80,
	        r: 80,
	      },
	    };

	    if (i==0){
	    	gd = gd3.node();
            plot = Plotly.plot(gd, data, layout, {showLink: false, displayModeBar: false});
            $(window).resize(function(){
		        Plotly.Plots.resize(gd);
		    });
	    }
	    else{
	    	gd2 = gd3.node();
            plot = Plotly.plot(gd2, data, layout, {showLink: false, displayModeBar: false});
            $(window).resize(function(){
		        Plotly.Plots.resize(gd2);
		    });
	    }
	}
}

//function that makes all the charts in two distincts columns
function graph_greeks_plot(X,list_Y,list_title){
	
	var count_grid = 1;

	//4 charts for each grid : 
	var nb_grid = Math.trunc(list_Y.length / 8);

	while(count_grid<=nb_grid){
		//Create a div that will receive the grid of 4 charts and put it inside a greek div
		$("#greeks-div").append("<div id='grid" + count_grid.toString() + "'></div>");

		//Select the new div created :
		var d3 = Plotly.d3;
		var ell = document.getElementById("grid" + count_grid.toString());
		var gd3 = d3.select(ell)
	    .style({
	        width: WIDTH_IN_PERCENT_OF_PARENT + '%',
	        'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

	        height: HEIGHT_IN_PERCENT_OF_PARENT + '%',
	        'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + '%'
	    });

	    var fourPlots = [];
	    var trace = {
	      x: X,
	      y: list_Y[8*(count_grid-1)],
	      xaxis: 'x',
	      yaxis: 'y',
	      //name:list_title[4*(count_grid-1)],
	      name:"Now",
	      line:{color:'rgba(86,148,230,0.8)'},
	      type: 'scatter'
	    };
	    fourPlots.push(trace);
	    var trace = {
	      x: X,
	      y: list_Y[8*(count_grid-1)+1],
	      xaxis: 'x',
	      yaxis: 'y',
	      //name:list_title[4*(count_grid-1)] + " / Last Day",
	      name:"Last Day",
	      line:{color:'rgba(86,148,230,0.8)'},
	      type: 'scatter'
	    };
	    fourPlots.push(trace);

        var graph_count = 2;
	    for(var i=2 ; i<8 ; i++){
	        var color = graph_count % 2 == 1 ? 'rgba(86,148,230,0.8)' : 'rgba(242,42,258,0.8)';
			var trace = {
			  x: X,
			  y: list_Y[8*(count_grid-1)+i],
			  xaxis: 'x' + (graph_count).toString(),
			  yaxis: 'y' + (graph_count).toString(),
			  //name: list_title[4*(count_grid-1)+graph_count-1],
			  name: "Now",
			  line:{color:color},
			  type: 'scatter',
			};
			fourPlots.push(trace);
			var trace = {
			  x: X,
			  y: list_Y[8*(count_grid-1)+i+1],
			  xaxis: 'x' + (graph_count).toString(),
			  yaxis: 'y' + (graph_count).toString(),
			  //name: list_title[4*(count_grid-1)+graph_count-1] + " / Last Day",
			  name: 'Last Day',
			  line:{color:color},
			  type: 'scatter',
			};
			fourPlots.push(trace);
			i++;
			graph_count++;
		}

		var layout_two_cols = {
			  xaxis: {
			     domain: [0,0.45],
			     titlefont: {
			        color: 'white'},
			     tickfont: {
			        color: 'white'},
			     },
			  yaxis: {
			     domain: [0,0.45],
			     title:list_title[4*(count_grid-1)],
			     titlefont: {
			        color: 'white'},
			     tickfont: {
			        color: 'white'},
			     },
			  xaxis2: {
			     domain: [0.55, 1],
			     titlefont: {
			        color: 'white'},
			     tickfont: {
			        color: 'white'},
			     },
			  yaxis2: {
			    domain: [0, 0.45],
			    title:list_title[4*(count_grid-1)+1],
			    anchor: 'x2',
			    titlefont: {
			        color: 'white'},
			     tickfont: {
			        color: 'white'},
			  },
			  xaxis3: {
			    domain: [0, 0.45],
			    anchor: 'y3',
			    titlefont: {
			        color: 'white'},
			     tickfont: {
			        color: 'white'},
			  },
			  yaxis3: {
			    domain: [0.55, 1],
			    title:list_title[4*(count_grid-1)+2],
			    titlefont: {
			        color: 'white'},
			     tickfont: {
			        color: 'white'},
			  },
			  xaxis4: {
			    domain: [0.55, 1],
			    anchor: 'y4',
			    titlefont: {
			        color: 'white'},
			     tickfont: {
			        color: 'white'},
			  },
			  yaxis4: {
			    domain: [0.55, 1],
			    title:list_title[4*(count_grid-1)+3],
			    anchor: 'x4',
			    titlefont: {
			        color: 'white'},
			     tickfont: {
			        color: 'white'},
			  },
			  showlegend:false,
			  paper_bgcolor:'rgba(0,0,0,0)',
              plot_bgcolor:'rgba(0,0,0,0)',
			  margin:{
			    t: 15,
			    b: 30,
			    l: 60,
			    r: 50,
			  },
			};

        //add resize event to modify the size of the grid :
		if (count_grid == 1)
		{
            gd = gd3.node();
            plot = Plotly.plot(gd, fourPlots, layout_two_cols, {showLink: false, displayModeBar: false});
            $(window).resize(function(){
		        Plotly.Plots.resize(gd);
		    });
		}
	    else
	    {
            gd2 = gd3.node();
            plot = Plotly.plot(gd2, fourPlots, layout_two_cols, {showLink: false, displayModeBar: false});
            $(window).resize(function(){
		        Plotly.Plots.resize(gd2);
		    });
	    }
		count_grid++;
	}
}