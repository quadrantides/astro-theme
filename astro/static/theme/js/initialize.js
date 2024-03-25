var graph_element_id = 'wheel'

function initialize(div_id, graph, config) {

//	  save_new_selection(data['tropical_selection'])
//      save_new_theme(theme)
//
//      var planets = data['planets']
//      set_planets(planets);
//
//      var config = graphics['config']
//      config['scrollZoom'] = false
//      config['showAxisDragHandles'] = false
//      config['showAxisRangeEntryBoxes'] = false
////
//      var graph = graphics['tropical'];
//      alert(graph.data);
//      alert(graph.layout);
      Plotly.plot(div_id,
                  graph.data,
                  graph.layout || {},
                  config);

//      var graphDiv = document.getElementById(graph_element_id)
//
//      set_aspects_ids(graphDiv);
//
//      new_plot_event()

}
