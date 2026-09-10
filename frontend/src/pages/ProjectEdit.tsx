import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router";
import ProjectForm, { type ProjectFormValues } from "../components/ProjectForm";
import {
  getProject,
  ProjectNotFoundError,
  updateProject,
  type Project,
  type ProjectCreateInput,
} from "../lib/projectsApi";

const SERVER_ERROR_MESSAGE = "プロジェクトの更新に失敗しました";

type Status = "loading" | "loaded" | "not-found" | "error";

function toFormValues(project: Project): Partial<ProjectFormValues> {
  return {
    customer_name: project.customer_name,
    project_name: project.project_name,
    description: project.description ?? "",
    start_date: project.start_date,
    is_ongoing: project.is_ongoing,
    end_date: project.end_date ?? "",
    team_size: project.team_size != null ? String(project.team_size) : "",
    total_man_month: project.total_man_month != null ? String(project.total_man_month) : "",
    source_note: project.source_note ?? "",
    technologies: project.technologies,
    project_types: project.project_types,
    industry: project.industry ?? "",
    outcome_note: project.outcome_note ?? "",
    dev_process_phases: (project.dev_process_phases ??
      []) as ProjectFormValues["dev_process_phases"],
    team_composition_note: project.team_composition_note ?? "",
  };
}

export function ProjectEdit() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [status, setStatus] = useState<Status>("loading");

  useEffect(() => {
    let cancelled = false;
    setStatus("loading");
    getProject(Number(id))
      .then((data) => {
        if (cancelled) return;
        setProject(data);
        setStatus("loaded");
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setStatus(err instanceof ProjectNotFoundError ? "not-found" : "error");
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  
  
  
  async function handleSubmit(input: ProjectCreateInput): Promise<Project> {
    return updateProject(Number(id), input);
  }

  
  function handleSuccess(updated: Project) {
    navigate(`/projects/${updated.id}`, {
      state: { successMessage: `「${updated.project_name}」を更新しました` },
    });
  }

  if (status === "loading") {
    return (
      <main className="app-page">
        <p role="status">読み込み中...</p>
      </main>
    );
  }

  if (status === "not-found") {
    return (
      <main className="app-page">
        <p>プロジェクトが見つかりません</p>
        <Link to="/projects">プロジェクト一覧へ戻る</Link>
      </main>
    );
  }

  if (status === "error" || !project) {
    return (
      <main className="app-page">
        <p className="toast-error" role="alert">
          プロジェクトの取得に失敗しました
        </p>
      </main>
    );
  }

  return (
    <main className="app-page">
      <h1>プロジェクトを編集</h1>
      <ProjectForm
        initialValues={toFormValues(project)}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}
        submitLabel="更新する"
        serverErrorMessage={SERVER_ERROR_MESSAGE}
        cancelTo={`/projects/${project.id}`}
      />
    </main>
  );
}

export default ProjectEdit;
