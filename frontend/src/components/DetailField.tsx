import type { ReactNode } from "react";

type DetailFieldProps = {
  label: string;
  children: ReactNode;
};

/** Read-only label + value row used inside a Detail section. */
export function DetailField({ label, children }: DetailFieldProps) {
  return (
    <div className="detail-field">
      <span className="detail-field-label">{label}</span>
      <div className="detail-field-value">{children}</div>
    </div>
  );
}

export default DetailField;
