import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  { name: "0-49", value1: 80, value2: 20 },
  { name: "50-99", value1: 60, value2: 40 },
  { name: "100-299", value1: 80, value2: 20 },
  { name: "300-499", value1: 30, value2: 70 },
  { name: "500+", value1: 60, value2: 40 },
];

export const HorizontalBarchart = () => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        layout="vertical"
        data={data}
        margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
      >
        <XAxis type="number" domain={[0, 100]} />
        <YAxis type="category" dataKey="name" />
        <Tooltip />
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
