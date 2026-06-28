export const percent = (value?: number | null) => {
  if (value === null || value === undefined || Number.isNaN(value)) return "-";
  const numeric = value <= 1 ? value * 100 : value;
  return `${numeric.toFixed(1)}%`;
};

export const gpa = (value?: number | null) => {
  if (value === null || value === undefined || Number.isNaN(value)) return "-";
  return `${value.toFixed(2)}/10`;
};

export const titleCase = (value: string) =>
  value
    .replace(/_/g, " ")
    .replace(/\w\S*/g, (text) => text.charAt(0).toUpperCase() + text.slice(1).toLowerCase());

export const compact = (value?: string | number | null) => {
  if (value === null || value === undefined || value === "") return "-";
  return String(value);
};
