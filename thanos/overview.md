## Thanos
Thanos leverages the Prometheus 2.0 storage format to cost-efficiently store historical metric data in any object storage while retaining fast query latencies. Additionally, it provides a global query view across all Prometheus installations and can merge data from Prometheus HA pairs on the fly.

Concretely the aims of the project are:

1. Global query view of metrics.
2. Unlimited retention of metrics.
3. High availability of components, including Prometheus.


Following the `KISS` and Unix philosophies, Thanos is made of a set of components with each filling a specific role.

KISS, an acronym for "keep it simple, stupid" or "keep it stupid simple". The KISS principle states that most systems work best if they are kept simple rather than made complicated; therefore, simplicity should be a key goal in design, and unnecessary complexity should be avoided

- Sidecar: connects to Prometheus, reads its data for query and/or uploads it to cloud storage.
- Store Gateway: serves metrics inside of a cloud storage bucket.
- Compactor: compacts, downsamples and applies retention on the data stored in cloud storage bucket.
- Receiver: receives data from Prometheus’ remote-write WAL, exposes it and/or upload it to cloud storage.
- Ruler/Rule: evaluates recording and alerting rules against data in Thanos for exposition and/or upload.
- Querier/Query: implements Prometheus’ v1 API to aggregate data from the underlying components.