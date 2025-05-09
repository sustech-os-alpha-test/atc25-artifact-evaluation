# Performance evaluation

## Running benchmarks

To execute benchmarks and get normalized results (Linux/Asterinas ratios for latency or Asterinas/Linux for bandwidth), including geometric means:

```shell
export BENCHMARK={bench_name} # lmbench|nginx|redis|sqlite
cd $BENCHMARK && ./run_all.sh
```

Results will be saved in `./result/{bench_name}/` containing:

- Raw outputs: Multiple `result_*.json` files
- Normalized summaries: Single `Ratio-summary.json` file

## Note on Redis and SQLite Results

The test scripts do not extract all Redis and SQLite benchmark data into `.json` files. Complete results are preserved in the `./results/{bench_name}` directory. Below are instructions for obtaining their full results:

**Redis:**

1. Find two CSV files (`all-*.csv`) in `./result/redis/` with this header format:

```text
"test","rps","avg_latency_ms","min_latency_ms","p50_latency_ms","p95_latency_ms","p99_latency_ms","max_latency_ms"
```

2. Use `stat` to identify results: Asterinas (earlier timestamp) and Linux (later timestamp).

**SQLite:**

Check `./result/sqlite/` for:

- `aster_output.txt` (Asterinas)
- `linux_output.txt` (Linux)
