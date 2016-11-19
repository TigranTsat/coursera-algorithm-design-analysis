package tigran

import org.slf4j.LoggerFactory
import org.slf4j.Logger
import java.io.InputStream


object Algo {
   private final val logger:Logger = LoggerFactory.getLogger(getClass().getName());
   
   def main(args: Array[String]) {
      run_tests();
      run_task();
    }
   
   def run_task() {
     val scc_stream:InputStream = getClass.getClassLoader.getResourceAsStream("SCC.txt")
     if (scc_stream == null) {
       logger.error("scc_stream is null")
     }
     val graph_input = io.Source.fromInputStream(scc_stream).mkString
     logger.info("File read")
     var edges = get_edges(graph_input);
     logger.debug("Edges: {} total", edges.length);
     val graph1:Graph = new Graph(edges)
     var answer1 = graph1.scc();
     logger.info("scc completed. Result = {}", answer1);
   }
   
   def validate_answer(actual: String, expected: String) {
     if (actual.equals(expected) == false) {
       logger.error("Mismatch between '{}' and '{}'", Array[AnyRef](actual, expected))
       throw new RuntimeException
     }
   }
   
   def run_tests() {
     val graph1_edges_str:String = """
        1 4
        2 8
        3 6
        4 7
        5 2
        6 9
        7 1
        8 5
        8 6
        9 7
        9 3
      """
     var edges = get_edges(graph1_edges_str);
     logger.debug("Edges: {}", edges);
     val graph1:Graph = new Graph(edges)
     logger.debug("Graph as adjacency lists: {}", graph1.adjacency_lists_stringify());
     graph1.dfs(1);
     logger.info("dfs completed");
     var answer1 = graph1.scc();
     logger.info("scc completed");
      //Answer: 3,3,3,0,0
     validate_answer(answer1, "3,3,3,0,0")
     
     
     val graph2_edges_str = """
      1 2
      2 3
      2 4
      2 5
      3 6
      4 5
      4 7
      5 2
      5 6
      5 7
      6 3
      6 8
      7 8
      7 10
      8 7
      9 7
      10 9
      10 11
      11 12
      12 10
        """
     edges = get_edges(graph2_edges_str);
     logger.debug("Edges: {}", edges);
     val graph2:Graph = new Graph(edges)
     logger.debug("Graph as adjacency lists: {}", graph2.adjacency_lists_stringify());
     graph2.dfs(1);
     logger.info("dfs completed");
     var answer2 = graph2.scc();
     logger.info("scc completed");
     // 6,3,2,1,0
     validate_answer(answer2, "6,3,2,1,0")
   }

   def get_edges(edges: String):Array[(Int, Int)] = {
     var rows = edges.split("\n");
     var result = new Array[(Int, Int)](rows.length);
     var i = 0;
     for (row:String <- rows) {
       val split_row = row.trim().split(" ");
       logger.trace("split_row = {}", split_row);
       if (split_row.length == 2) {
         val n1 = Integer.parseInt(split_row(0));
         val n2 = Integer.parseInt(split_row(1));
  
         var pair = new Tuple2(n1, n2)
         logger.trace("Pair = {}", pair);
         result(i) = pair;
         i += 1;
       }
     }
     return result.slice(0, i);
   }
}