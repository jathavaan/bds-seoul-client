import type { TooltipProps } from "recharts";
import type {
  NameType,
  ValueType,
} from "recharts/types/component/DefaultTooltipContent";

export const Tooltip = ({
  active,
  payload,
  label,
  showPercentage,
}: TooltipProps<ValueType, NameType> & { showPercentage: boolean }) => {
  if (active && payload && payload.length) {
    return (
      <div
        style={{
          color: "#000",
          background: "#fff",
          padding: "10px",
          border: "1px solid #ccc",
        }}
      >
        <p>
          <b>Playtime: {label} hours</b>
        </p>
        <p style={{ color: "#1976d2" }}>
          Recommended:{" "}
          {showPercentage
            ? `${(payload[0].value as number)?.toFixed(2)}%`
            : Math.round(payload[0].value as number)}
        </p>
        <p style={{ color: "#f50057" }}>
          Not Recommended:{" "}
          {showPercentage
            ? `${(payload[1].value as number)?.toFixed(2)}%`
            : Math.round(payload[1].value as number)}
        </p>
      </div>
    );
  }

  return null;
};
