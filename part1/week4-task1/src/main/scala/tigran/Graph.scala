

package tigran

import scala.collection.mutable.HashMap
import scala.collection.mutable.ArrayBuffer

import org.slf4j.Logger
import org.slf4j.LoggerFactory

class Graph {
  private final val logger: Logger = LoggerFactory.getLogger(getClass().getName());

  var edges: Array[Int] = _;
  var adjacency_lists: Array[ArrayBuffer[Int]] = _;
  var reverse_adjacency_lists: Array[ArrayBuffer[Int]] = _;
  var seen_nodes: Array[Boolean] = _;
  var max_nodes: Int = -1;
  var t: Int = 0;
  var s: Integer = null;
  var finishing_times: Array[Int] = _;
  var reversed_finishing_times: Array[Int] = _;
  var leaders: Array[Int] = _;

  def this(edges: Array[(Int, Int)]) {
    this()
    for (edge: Tuple2[Int, Int] <- edges) {
      var max_edge = math.max(edge._1, edge._2);
      max_nodes = math.max(max_nodes, max_edge);
    }
    var nodes_list: Array[Boolean] = Array.fill[Boolean](max_nodes)(false);
    for (edge: Tuple2[Int, Int] <- edges) {
      nodes_list(edge._1 - 1) = true;
      nodes_list(edge._2 - 1) = true;
    }
    for (i <- 0 until this.max_nodes) {
      if (nodes_list(i) == false) {
        logger.error("Missing link for node: {}", i + 1);
        throw new RuntimeException;
      }
    }
    logger.info("Graph was created. Total nodes {} starting from 1", max_nodes)
    adjacency_lists = new Array[ArrayBuffer[Int]](max_nodes);
    reverse_adjacency_lists = new Array[ArrayBuffer[Int]](max_nodes);
    for (i: Int <- 0 until max_nodes) {
      val init_size = 3;
      adjacency_lists(i) = new ArrayBuffer(init_size);
      reverse_adjacency_lists(i) = new ArrayBuffer(init_size);
    }
    for (edge: Tuple2[Int, Int] <- edges) {
      val (from_node, to_node) = (edge._1, edge._2);
      if (adjacency_lists(from_node - 1).contains(to_node - 1) == false) {
        adjacency_lists(from_node - 1).append(to_node - 1);
      }
      if (reverse_adjacency_lists(to_node - 1).contains(from_node - 1) == false) {
        reverse_adjacency_lists(to_node - 1).append(from_node - 1);
      }
    }

    reset_seen_nodes();
    reset_scc();
  }

  def reset_seen_nodes() {
    seen_nodes = Array.fill(this.max_nodes)(false);
  }

  def reset_scc() {
    this.t = 0;
    this.s = null;
  }

  def adjacency_lists_stringify(): String = {
    return adjacency_lists_stringify(adjacency_lists);
  }

  def adjacency_lists_stringify(adj_list: Array[ArrayBuffer[Int]]): String = {
    val str_builder = new StringBuilder();
    str_builder.append("{")
    for (i <- 0 until adj_list.length) {
      str_builder.append(i + 1).append(" => [");
      val node_adjacency_list: ArrayBuffer[Int] = adj_list(i);
      for (to_node: Int <- node_adjacency_list) {
        str_builder.append(to_node + 1).append(",");
      }
      str_builder.append("]\n");
    }
    str_builder.append("{")
    return str_builder.toString();
  }

  def dfs(start_node: Int) {
    _dfs(start_node - 1);

  }
  /**
   * start_node - node from which we start search (it's value - 1)
   */
  private def _dfs(start_node: Int) {
    if (seen_nodes(start_node) == false) {
      seen_nodes(start_node) = true;
      for (node_to: Int <- adjacency_lists(start_node)) {
        //        logger.debug("Processing node {} from node: {}", node_to + 1, start_node + 1);
        _dfs(node_to);
      }
    }
  }

  private def _dfs_scc(adj_list: Array[ArrayBuffer[Int]], i: Int, do_times: Boolean) {
    if (seen_nodes(i)) {
      return ;
    }
    seen_nodes(i) = true;
    leaders(i) = this.s;
    for (node_to: Int <- adj_list(i)) {
      //      logger.debug("Processing node {} from node: {}", node_to + 1, i + 1);
      _dfs_scc(adj_list, node_to, do_times);
    }
    t += 1
    if (do_times) {
      finishing_times(i) = t - 1;
      reversed_finishing_times(t - 1) = i;
    }
  }

  private def dfs_loop_01(adj_list: Array[ArrayBuffer[Int]]) {
    for (i: Int <- this.max_nodes - 1 to 0 by -1) {
      if (seen_nodes(i) == false) {
        s = i;
        _dfs_scc(adj_list, i, true);
      }
    }
  }

  private def dfs_loop_02(adj_list: Array[ArrayBuffer[Int]]) {
    for (i: Int <- this.max_nodes - 1 to 0 by -1) {
      var node_to_explore = reversed_finishing_times(i);
      if (seen_nodes(node_to_explore) == false) {
        s = node_to_explore;
        _dfs_scc(adj_list, node_to_explore, false);
      }
    }
  }

  def scc():String = {
    this.synchronized {
      reset_seen_nodes();
      finishing_times = Array.fill(this.max_nodes)(-1);
      reversed_finishing_times = Array.fill(this.max_nodes)(-1);
      leaders = Array.fill(this.max_nodes)(-1);
      dfs_loop_01(this.reverse_adjacency_lists);
//      logger.info("Finishing times: {}", this.finishing_times);
//      logger.info("Reversed_finishing_times: {}", this.reversed_finishing_times);
      reset_seen_nodes();
      dfs_loop_02(this.adjacency_lists);
//      logger.info("Leaders: {}", this.leaders)
//      logger.info("leaders_stringify = {}", leaders_stringify())
      logger.info("leaders_stringify_answer = {}", leaders_stringify_answer())
      return this.leaders_stringify_answer();
    }
  }

  private def leaders_stringify(): String = {
    val str_bld: StringBuilder = new StringBuilder();
    str_bld.append("{");
    for (i: Int <- this.max_nodes - 1 to 0 by -1) {
      str_bld.append(i + 1).append(" -> ").append(leaders(i) + 1).append("\n");
    }
    str_bld.append("}");
    return str_bld.toString();
  }

  private def leaders_stringify_answer(): String = {
    val scc: HashMap[Int, Int] = new HashMap[Int, Int]();
    for (i: Int <- this.max_nodes - 1 to 0 by -1) {
      scc.update(leaders(i), scc.getOrElse(leaders(i), 0) + 1);
    }
    //    logger.debug("scc = {}", scc)
    val scc_by_n_of_elements = scc.values.toSeq.sorted(Ordering[Int].reverse)
    var top5:List[Int] = scc_by_n_of_elements.take(5).toList;
    top5 = top5.padTo(5, 0);
    logger.debug("top5 = {}", top5);

    return top5.mkString(",");
  }
}