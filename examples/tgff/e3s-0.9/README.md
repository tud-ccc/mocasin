The E3S benchmark suite was kindly provided by Robert Dick for redistribution
in Mocasin. Original source: http://ziyang.eecs.umich.edu/~dickrp/e3s/
Also see LICENSE.txt.

You can use a mocasin command like the following to iterate over all applications in the E3S suite:

```
pykpn generate_mapping \
      kpn=tgff_reader  \
      trace=tgff_reader \
      platform=exynos,haec,mppa_coolidge,multi_cluster \
      tgff={file:auto-indust-mocsyn.tgff,graph_name:TASK_GRAPH_0},{file:auto-indust-mocsyn.tgff,graph_name:TASK_GRAPH_1},{file:auto-indust-mocsyn.tgff,graph_name:TASK_GRAPH_2},{file:auto-indust-mocsyn.tgff,graph_name:TASK_GRAPH_3},{file:consumer-mocsyn.tgff,graph_name:TASK_GRAPH_0},{file:consumer-mocsyn.tgff,graph_name:TASK_GRAPH_1},{file:networking-mocsyn.tgff,graph_name:TASK_GRAPH_0},{file:networking-mocsyn.tgff,graph_name:TASK_GRAPH_1},{file:networking-mocsyn.tgff,graph_name:TASK_GRAPH_2},{file:networking-mocsyn.tgff,graph_name:TASK_GRAPH_3},{file:office-automation-mocsyn.tgff,graph_name:TASK_GRAPH_0},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_0},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_1},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_2},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_3},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_4},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_5},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_6},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_7},{file:telecom-mocsyn.tgff,graph_name:TASK_GRAPH_8}\
      mapper=genetic,tabu_search,simulated_annealing,random_walk,gradient_descent \
      representation=SimpleVector,MetricSpaceEmbedding,Symmetries,SymmetryEmbedding \
      mapper.random_seed=`seq -s, 1 10` \
      hydra.sweep.dir=multirun-metaheuristics-multiple-representations \
      log_level=ERROR \
      -m
```
