type MultilineTextProps = {
  value: string | null | undefined;
};

/** Renders a free-text value with its original line breaks preserved
 *  (via CSS `white-space: pre-wrap`). Shows an em-dash when empty. */
export function MultilineText({ value }: MultilineTextProps) {
  const trimmed = (value ?? "").trim();
  if (!trimmed) return <>—</>;

  return <span className="multiline-text">{trimmed}</span>;
}

export default MultilineText;
