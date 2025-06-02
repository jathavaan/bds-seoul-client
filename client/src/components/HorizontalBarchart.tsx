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

export const HorizontalBarchart = ({ recommendations }: BarchartProps) => {
  const data = recommendations.map((recommendation) => {
    const total =
      recommendation.sum_recommended + recommendation.sum_not_recommended;
    return {
      name: recommendation.time_interval,
      value1: total > 0 ? (recommendation.sum_recommended / total) * 100 : 0,
      value2:
        total > 0 ? (recommendation.sum_not_recommended / total) * 100 : 0,
    };
  });

  return (
    <ResponsiveContainer width="100%" height="50%">
      <BarChart
        layout="vertical"
        data={data}
        margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
      >
        <XAxis type="number" domain={[0, 100]} />
        <YAxis type="category" dataKey="name" />
        <Tooltip content={<CustomTooltip showPercentage={true} />} />
        <Bar
          dataKey="value1"
          stackId="a"
          fill="#1976d2"
          animationBegin={0}
          animationDuration={800}
          animationEasing="ease-in"
        />
        <Bar
          dataKey="value2"
          stackId="a"
          fill="#f50057"
          animationBegin={800}
          animationDuration={800}
          animationEasing="ease-out"
        />
      </BarChart>
    </ResponsiveContainer>
  );
};
