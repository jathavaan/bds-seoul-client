import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { BarchartProps } from "../shared/types.ts";
import { Tooltip as CustomTooltip } from "./Tooptip.tsx";

export const VerticalBarchart = ({ recommendations }: BarchartProps) => {
  const data = recommendations.map((recommendation) => ({
    name: recommendation.time_interval,
    value1: recommendation.sum_recommended,
    value2: recommendation.sum_not_recommended,
  }));

  return (
    <ResponsiveContainer width="100%" height="50%">
      <BarChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
      >
        <XAxis dataKey="name" type="category" />
        <YAxis
          type="number"
          domain={[
            0,
            Math.max(
              ...recommendations.map((rec) =>
                Math.max(rec.sum_recommended, rec.sum_not_recommended),
              ),
            ),
          ]}
        />
        <Tooltip content={<CustomTooltip showPercentage={false} />} />
        <Bar
          dataKey="value1"
          stackId="a"
          fill="#1976d2"
          animationEasing="ease-in"
        />
        <Bar
          dataKey="value2"
          stackId="b"
          fill="#f50057"
          animationEasing="ease-in"
        />
      </BarChart>
    </ResponsiveContainer>
  );
};
