import { foreignCall } from "./kuhul-bridge";

const kpi = foreignCall({
  host: "python",
  module: "numpy",
  symbol: "dot",
  args: [{ ref: "a" }, { ref: "b" }],
  out: "c"
});

// then you’d write KPI to disk, run python adapter, get result back.
