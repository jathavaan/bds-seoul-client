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

export const VerticalBarchart = () => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
      >
        <XAxis dataKey="name" type="category" />
        <YAxis type="number" domain={[0, 100]} />
        <Tooltip />
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
          animationEasing="ease-out"
        />
      </BarChart>
    </ResponsiveContainer>
  );
};
