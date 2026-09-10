import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router";
import Badge from "../components/Badge";
import FilterDropdown from "../components/FilterDropdown";
import { listProjects, listTechTags, type Project } from "../lib/projectsApi";
import { PROJECT_TYPE_LABELS, PROJECT_TYPE_OPTIONS } from "../lib/projectTypes";
import { DEV_PROCESS_PHASE_LABELS, DEV_PROCESS_PHASE_OPTIONS } from "../lib/devProcessPhases";
import { formatPeriod } from "../lib/formatPeriod";
import ProjectCard from "../components/ProjectCard";

const PAGE_SIZE = 20;
const SEARCH_DEBOUNCE_MS = 300;
const VIEW_MODE_STORAGE_KEY = "projectListViewMode";

type Status = "loading" | "loaded" | "error";
type ViewMode = "list" | "card";

function readStoredViewMode(): ViewMode {
  try {
    const stored = window.localStorage.getItem(VIEW_MODE_STORAGE_KEY);
    return stored === "list" ? "list" : "card";
  } catch {
    return "card";
  }
}

/** Joins filter arrays with "," for the URL, splits them back when reading. */
function parseListParam(value: string | null): string[] {
  return value ? value.split(",").filter(Boolean) : [];
}

export function ProjectList() {
  const [searchParams, setSearchParams] = useSearchParams();

  const [items, setItems] = useState<Project[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(() => {
    const fromUrl = Number(searchParams.get("page"));
    return Number.isInteger(fromUrl) && fromUrl > 0 ? fromUrl : 1;
  });
  const [q, setQ] = useState(() => searchParams.get("q") ?? "");
  const [debouncedQ, setDebouncedQ] = useState(() => searchParams.get("q") ?? "");
  const [technology, setTechnology] = useState<string[]>(() =>
    parseListParam(searchParams.get("technology")),
  );
  const [projectType, setProjectType] = useState<string[]>(() =>
    parseListParam(searchParams.get("type")),
  );
  const [devProcessPhase, setDevProcessPhase] = useState<string[]>(() =>
    parseListParam(searchParams.get("phase")),
  );
  const [status, setStatus] = useState<Status>("loading");
  const [techOptions, setTechOptions] = useState<string[]>([]);
  const [viewMode, setViewMode] = useState<ViewMode>(readStoredViewMode);

  function changeViewMode(mode: ViewMode) {
    setViewMode(mode);
    try {
      window.localStorage.setItem(VIEW_MODE_STORAGE_KEY, mode);
    } catch {
      // localStorage unavailable (e.g. private mode) — ignore.
    }
  }

  // Debounce the search input by 300ms before triggering a new query.
  // Skip the page-reset on the first run (mount) so the page restored from
  // the URL (back from Detail) is not immediately reset to 1.
  const isFirstQEffectRef = { current: true } as { current: boolean };
  useEffect(() => {
    if (isFirstQEffectRef.current) {
      isFirstQEffectRef.current = false;
      setDebouncedQ(q);
      return;
    }
    const timer = setTimeout(() => {
      setDebouncedQ(q);
      setPage(1);
    }, SEARCH_DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [q]);

  // Sync the search/filter state to the URL (replace, not push) so that
  // navigating back from Detail restores the same view.
  useEffect(() => {
    const next = new URLSearchParams();
    if (q) next.set("q", q);
    if (page > 1) next.set("page", String(page));
    if (technology.length) next.set("technology", technology.join(","));
    if (projectType.length) next.set("type", projectType.join(","));
    if (devProcessPhase.length) next.set("phase", devProcessPhase.join(","));
    setSearchParams(next, { replace: true });
  }, [q, page, technology, projectType, devProcessPhase, setSearchParams]);

  useEffect(() => {
    listTechTags()
      .then(setTechOptions)
      .catch(() => setTechOptions([]));
  }, []);

  useEffect(() => {
    let cancelled = false;
    setStatus("loading");
    listProjects({
      page,
      page_size: PAGE_SIZE,
      q: debouncedQ || undefined,
      technology: technology.length ? technology : undefined,
      project_type: projectType.length ? projectType : undefined,
      dev_process_phase: devProcessPhase.length ? devProcessPhase : undefined,
    })
      .then((response) => {
        if (cancelled) return;
        setItems(response.items);
        setTotal(response.total);
        setStatus("loaded");
      })
      .catch(() => {
        if (!cancelled) setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, [page, debouncedQ, technology, projectType, devProcessPhase]);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  function handleTechnologyChange(selected: string[]) {
    setTechnology(selected);
    setPage(1);
  }

  function handleProjectTypeChange(selected: string[]) {
    setProjectType(selected);
    setPage(1);
  }

  function handleDevProcessPhaseChange(selected: string[]) {
    setDevProcessPhase(selected);
    setPage(1);
  }

  type FilterChip = { key: string; label: string; colorClass: string; onRemove: () => void };
  const chips: FilterChip[] = [];
  if (q) {
    chips.push({
      key: "q",
      label: `"${q}"`,
      colorClass: "filter-chip-search",
      onRemove: () => setQ(""),
    });
  }
  technology.forEach((tech) => {
    chips.push({
      key: `tech-${tech}`,
      label: tech,
      colorClass: "filter-chip-tech",
      onRemove: () => handleTechnologyChange(technology.filter((v) => v !== tech)),
    });
  });
  projectType.forEach((t) => {
    chips.push({
      key: `type-${t}`,
      label: PROJECT_TYPE_LABELS[t] ?? t,
      colorClass: "filter-chip-type",
      onRemove: () => handleProjectTypeChange(projectType.filter((v) => v !== t)),
    });
  });
  devProcessPhase.forEach((p) => {
    chips.push({
      key: `phase-${p}`,
      label: DEV_PROCESS_PHASE_LABELS[p] ?? p,
      colorClass: "filter-chip-phase",
      onRemove: () => handleDevProcessPhaseChange(devProcessPhase.filter((v) => v !== p)),
    });
  });

  function clearAllFilters() {
    setQ("");
    setTechnology([]);
    setProjectType([]);
    setDevProcessPhase([]);
    setPage(1);
  }

  return (
    <main className="app-page">
      <div className="page-header-row">
        <h1>プロジェクト</h1>
        <div className="page-header-actions">
          <Link to="/projects/new" className="button-primary">
            + 新規プロジェクト
          </Link>
        </div>
      </div>

      <div className="project-list-toolbar">
        <div className="search-input">
          <input
            type="search"
            value={q}
            onChange={(event) => setQ(event.target.value)}
            placeholder="顧客名・プロジェクト名・概要を検索..."
            aria-label="検索"
          />
        </div>
        <FilterDropdown
          label="技術"
          options={techOptions.map((t) => ({ value: t, label: t }))}
          value={technology}
          onChange={handleTechnologyChange}
        />
        <FilterDropdown
          label="種別"
          options={PROJECT_TYPE_OPTIONS.map(({ code, label }) => ({ value: code, label }))}
          value={projectType}
          onChange={handleProjectTypeChange}
        />
        <FilterDropdown
          label="開発工程"
          options={DEV_PROCESS_PHASE_OPTIONS.map(({ code, label }) => ({ value: code, label }))}
          value={devProcessPhase}
          onChange={handleDevProcessPhaseChange}
        />
        <div className="view-mode-toggle" role="group" aria-label="表示モード">
          <button
            type="button"
            className={viewMode === "list" ? "view-mode-button view-mode-active" : "view-mode-button"}
            onClick={() => changeViewMode("list")}
            aria-pressed={viewMode === "list"}
          >
            リスト
          </button>
          <button
            type="button"
            className={viewMode === "card" ? "view-mode-button view-mode-active" : "view-mode-button"}
            onClick={() => changeViewMode("card")}
            aria-pressed={viewMode === "card"}
          >
            カード
          </button>
        </div>
      </div>

      {chips.length > 0 && (
        <div className="filter-chips">
          {chips.map((chip) => (
            <span key={chip.key} className={`filter-chip ${chip.colorClass}`}>
              {chip.label}
              <button
                type="button"
                className="filter-chip-remove"
                onClick={chip.onRemove}
                aria-label={`${chip.label}を解除`}
              >
                ✕
              </button>
            </span>
          ))}
          <button type="button" className="filter-clear-all" onClick={clearAllFilters}>
            すべてクリア
          </button>
        </div>
      )}

      <div className="project-list-count">{total}件</div>

      {status === "error" && (
        <p className="toast-error" role="alert">
          プロジェクト一覧の取得に失敗しました
        </p>
      )}

      {status === "loading" && <p role="status">読み込み中...</p>}

      {status === "loaded" && total === 0 && <p>プロジェクトが見つかりません</p>}

      {status === "loaded" && total > 0 && viewMode === "card" && (
        <div className="project-card-grid">
          {items.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}

      {status === "loaded" && total > 0 && viewMode === "list" && (
        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th>顧客名</th>
                <th>プロジェクト名</th>
                <th>概要</th>
                <th>期間</th>
                <th>種別</th>
                <th>技術</th>
                <th>人数</th>
                <th>総人月</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {items.map((project) => (
                <tr key={project.id}>
                  <td>{project.customer_name}</td>
                  <td>{project.project_name}</td>
                  <td className="project-list-description">{project.description}</td>
                  <td>{formatPeriod(project)}</td>
                  <td>
                    {project.project_types.map((t) => (
                      <Badge key={t} variant="type">
                        {PROJECT_TYPE_LABELS[t] ?? t}
                      </Badge>
                    ))}
                  </td>
                  <td>
                    {project.technologies.map((tech) => (
                      <Badge key={tech} variant="tech">
                        {tech}
                      </Badge>
                    ))}
                  </td>
                  <td>{project.team_size ?? "—"}</td>
                  <td>{project.total_man_month ?? "—"}</td>
                  <td>
                    <Link
                      to={`/projects/${project.id}`}
                      className="row-action-link"
                      aria-label="詳細"
                    >
                      <svg viewBox="0 0 16 16" fill="none" aria-hidden="true">
                        <path
                          d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5Z"
                          stroke="currentColor"
                          strokeWidth="1.3"
                        />
                        <circle cx="8" cy="8" r="2" stroke="currentColor" strokeWidth="1.3" />
                      </svg>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {status === "loaded" && total > 0 && (
        <div className="project-list-pagination">
          <button
            type="button"
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page <= 1}
          >
            前へ
          </button>
          <span>
            {page} / {totalPages}
          </span>
          <button
            type="button"
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page >= totalPages}
          >
            次へ
          </button>
        </div>
      )}
    </main>
  );
}

export default ProjectList;
