import type { Project } from "./projectsApi";

/** "YYYY-MM-DD 〜 YYYY-MM-DD", or "YYYY-MM-DD 〜 進行中" for ongoing projects. */
export function formatPeriod(project: Project): string {
  const start = project.start_date;
  if (project.is_ongoing) return `${start} 〜 進行中`;
  return project.end_date ? `${start} 〜 ${project.end_date}` : start;
}
