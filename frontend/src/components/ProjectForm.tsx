import { useState, type FormEvent } from "react";
import { Link } from "react-router";
import {
  listTechTags,
  type DevProcessPhaseCode,
  type Project,
  type ProjectCreateInput,
  type ProjectTypeCode,
} from "../lib/projectsApi";
import { PROJECT_TYPE_OPTIONS } from "../lib/projectTypes";
import { DEV_PROCESS_PHASE_OPTIONS } from "../lib/devProcessPhases";

export type ProjectFormValues = {
  customer_name: string;
  project_name: string;
  description: string;
  start_date: string;
  is_ongoing: boolean;
  end_date: string;
  team_size: string;
  total_man_month: string;
  source_note: string;
  technologies: string[];
  project_types: ProjectTypeCode[];
  industry: string;
  outcome_note: string;
  dev_process_phases: DevProcessPhaseCode[];
  team_composition_note: string;
};

const EMPTY_VALUES: ProjectFormValues = {
  customer_name: "",
  project_name: "",
  description: "",
  start_date: "",
  is_ongoing: false,
  end_date: "",
  team_size: "",
  total_man_month: "",
  source_note: "",
  technologies: [],
  project_types: [],
  industry: "",
  outcome_note: "",
  dev_process_phases: [],
  team_composition_note: "",
};

interface ProjectFormProps {
  initialValues?: Partial<ProjectFormValues>;
  onSubmit: (input: ProjectCreateInput) => Promise<Project>;
  onSuccess: (project: Project) => void;
  submitLabel: string;
  serverErrorMessage: string;
  cancelTo: string;
}

export function ProjectForm({
  initialValues,
  onSubmit,
  onSuccess,
  submitLabel,
  serverErrorMessage,
  cancelTo,
}: ProjectFormProps) {
  const values = { ...EMPTY_VALUES, ...initialValues };

  const [customerName, setCustomerName] = useState(values.customer_name);
  const [projectName, setProjectName] = useState(values.project_name);
  const [description, setDescription] = useState(values.description);
  const [startDate, setStartDate] = useState(values.start_date);
  const [isOngoing, setIsOngoing] = useState(values.is_ongoing);
  const [endDate, setEndDate] = useState(values.end_date);
  const [teamSize, setTeamSize] = useState(values.team_size);
  const [totalManMonth, setTotalManMonth] = useState(values.total_man_month);
  const [sourceNote, setSourceNote] = useState(values.source_note);
  const [technologies, setTechnologies] = useState<string[]>(values.technologies);
  const [tagInput, setTagInput] = useState("");
  const [tagSuggestions, setTagSuggestions] = useState<string[]>([]);
  const [projectTypes, setProjectTypes] = useState<ProjectTypeCode[]>(values.project_types);
  const [industry, setIndustry] = useState(values.industry);
  const [outcomeNote, setOutcomeNote] = useState(values.outcome_note);
  const [devProcessPhases, setDevProcessPhases] = useState<DevProcessPhaseCode[]>(
    values.dev_process_phases,
  );
  const [teamCompositionNote, setTeamCompositionNote] = useState(values.team_composition_note);

  const [submitting, setSubmitting] = useState(false);
  const [touched, setTouched] = useState(false);
  const [serverError, setServerError] = useState<string | null>(null);

  const missingRequired = !customerName.trim() || !projectName.trim() || !startDate;
  const ongoingConflict = isOngoing && endDate !== "";
  const endBeforeStart = Boolean(endDate && startDate && endDate < startDate);
  // Same rules as the API (team_size >= 1 integer, total_man_month >= 0), shown next to the field
  // instead of a generic "failed" message after the request is rejected.
  const teamSizeInvalid =
    teamSize !== "" && !(Number.isInteger(Number(teamSize)) && Number(teamSize) >= 1);
  const manMonthInvalid =
    totalManMonth !== "" && !(Number.isFinite(Number(totalManMonth)) && Number(totalManMonth) >= 0);
  const canSubmit =
    !missingRequired && !ongoingConflict && !endBeforeStart && !teamSizeInvalid && !manMonthInvalid;

  function handleIsOngoingChange(checked: boolean) {
    setIsOngoing(checked);
    if (checked) setEndDate("");
  }

  function handleTagInputChange(value: string) {
    setTagInput(value);
    if (!value.trim()) {
      setTagSuggestions([]);
      return;
    }
    listTechTags(value)
      .then(setTagSuggestions)
      .catch(() => setTagSuggestions([]));
  }

  function addTag(tag: string) {
    // Technologies are stored comma-separated, so "C,C++" is added as two visible tags
    // instead of being split silently by the API.
    const newTags = tag
      .split(/[,、]/)
      .map((part) => part.trim().toLowerCase())
      .filter((part, index, parts) => part && parts.indexOf(part) === index)
      .filter((part) => !technologies.some((technology) => technology.toLowerCase() === part));
    if (newTags.length === 0) {
      return;
    }
    setTechnologies((prev) => [...prev, ...newTags]);
    setTagInput("");
    setTagSuggestions([]);
  }

  function removeTag(tag: string) {
    setTechnologies((prev) => prev.filter((t) => t !== tag));
  }

  function toggleProjectType(code: ProjectTypeCode) {
    setProjectTypes((prev) =>
      prev.includes(code) ? prev.filter((c) => c !== code) : [...prev, code],
    );
  }

  function toggleDevProcessPhase(code: DevProcessPhaseCode) {
    setDevProcessPhases((prev) =>
      prev.includes(code) ? prev.filter((c) => c !== code) : [...prev, code],
    );
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setTouched(true);
    if (!canSubmit) return;

    setSubmitting(true);
    setServerError(null);
    try {
      const project = await onSubmit({
        customer_name: customerName,
        project_name: projectName,
        description: description || null,
        start_date: startDate,
        end_date: isOngoing ? null : endDate || null,
        is_ongoing: isOngoing,
        team_size: teamSize ? Number(teamSize) : null,
        total_man_month: totalManMonth ? Number(totalManMonth) : null,
        source_note: sourceNote || null,
        technologies,
        project_types: projectTypes,
        industry: industry || null,
        outcome_note: outcomeNote || null,
        dev_process_phases: devProcessPhases,
        team_composition_note: teamCompositionNote || null,
      });

      onSuccess(project);
    } catch (err) {
      void err;
      setServerError(serverErrorMessage);
      setSubmitting(false);
    }
  }

  return (
    <div className="form-container">
      {serverError && (
        <p className="toast-error" role="alert">
          {serverError}
        </p>
      )}
      <form
        onSubmit={handleSubmit}
        onKeyDown={(event) => {
          if (event.key === "Enter" && event.target instanceof HTMLInputElement) {
            event.preventDefault();
          }
        }}
      >
        <section className="form-group-card">
          <h2 className="form-group-card-title">基本情報</h2>

          <div
            className={`input-field${touched && !customerName.trim() ? " input-field-error" : ""}`}
          >
            <label htmlFor="customer-name">
              顧客名 <span className="required-mark">*</span>
            </label>
            <input
              id="customer-name"
              value={customerName}
              onChange={(event) => setCustomerName(event.target.value)}
              disabled={submitting}
            />
            {touched && !customerName.trim() && (
              <p className="field-error-message" role="alert">
                顧客名は必須です
              </p>
            )}
          </div>

          <div
            className={`input-field${touched && !projectName.trim() ? " input-field-error" : ""}`}
          >
            <label htmlFor="project-name">
              プロジェクト名 <span className="required-mark">*</span>
            </label>
            <input
              id="project-name"
              value={projectName}
              onChange={(event) => setProjectName(event.target.value)}
              disabled={submitting}
            />
            {touched && !projectName.trim() && (
              <p className="field-error-message" role="alert">
                プロジェクト名は必須です
              </p>
            )}
          </div>

          <div className="input-field">
            <label htmlFor="description">概要</label>
            <textarea
              id="description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              disabled={submitting}
            />
          </div>

          <div className="input-field">
            <label htmlFor="industry">業種</label>
            <input
              id="industry"
              value={industry}
              onChange={(event) => setIndustry(event.target.value)}
              disabled={submitting}
            />
          </div>
        </section>

        <section className="form-group-card">
          <h2 className="form-group-card-title">期間・規模</h2>

          <div className={`input-field${touched && !startDate ? " input-field-error" : ""}`}>
            <label htmlFor="start-date">
              開始日 <span className="required-mark">*</span>
            </label>
            <input
              id="start-date"
              type="date"
              value={startDate}
              onChange={(event) => setStartDate(event.target.value)}
              disabled={submitting}
            />
            {touched && !startDate && (
              <p className="field-error-message" role="alert">
                開始日は必須です
              </p>
            )}
          </div>

          <div className="input-field">
            <label htmlFor="is-ongoing">
              <input
                id="is-ongoing"
                type="checkbox"
                checked={isOngoing}
                onChange={(event) => handleIsOngoingChange(event.target.checked)}
                disabled={submitting}
              />
              進行中
            </label>
          </div>

          <div
            className={`input-field${touched && (ongoingConflict || endBeforeStart) ? " input-field-error" : ""}`}
          >
            <label htmlFor="end-date">終了日</label>
            <input
              id="end-date"
              type="date"
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
              disabled={submitting || isOngoing}
            />
            {touched && ongoingConflict && (
              <p className="field-error-message" role="alert">
                進行中の場合、終了日は入力できません
              </p>
            )}
            {touched && endBeforeStart && (
              <p className="field-error-message" role="alert">
                終了日は開始日以降にしてください
              </p>
            )}
          </div>

          <div className="form-row">
            <div className={`input-field${touched && teamSizeInvalid ? " input-field-error" : ""}`}>
              <label htmlFor="team-size">人数</label>
              <div className="input-field-with-unit">
                <input
                  id="team-size"
                  type="number"
                  min={1}
                  step={1}
                  value={teamSize}
                  onChange={(event) => setTeamSize(event.target.value)}
                  disabled={submitting}
                />
                <span className="input-unit">名</span>
              </div>
              {touched && teamSizeInvalid && (
                <p className="field-error-message" role="alert">
                  人数は1以上の整数で入力してください
                </p>
              )}
            </div>

            <div className={`input-field${touched && manMonthInvalid ? " input-field-error" : ""}`}>
              <label htmlFor="total-man-month">総人月</label>
              <div className="input-field-with-unit">
                <input
                  id="total-man-month"
                  type="number"
                  min={0}
                  step="any"
                  value={totalManMonth}
                  onChange={(event) => setTotalManMonth(event.target.value)}
                  disabled={submitting}
                />
                <span className="input-unit">人月</span>
              </div>
              {touched && manMonthInvalid && (
                <p className="field-error-message" role="alert">
                  総人月は0以上の数値で入力してください
                </p>
              )}
            </div>
          </div>

          <div className="input-field">
            <label htmlFor="team-composition-note">チーム体制の詳細</label>
            <textarea
              id="team-composition-note"
              value={teamCompositionNote}
              onChange={(event) => setTeamCompositionNote(event.target.value)}
              disabled={submitting}
            />
          </div>
        </section>

        <section className="form-group-card">
          <h2 className="form-group-card-title">分類</h2>

          <div className="input-field">
            <label htmlFor="tech-input">技術</label>
            <div className="tech-input-wrapper">
              <input
                id="tech-input"
                placeholder="入力してEnterで追加（複数可）"
                maxLength={100}
                aria-describedby="tech-input-hint"
                value={tagInput}
                onChange={(event) => handleTagInputChange(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    event.preventDefault();
                    addTag(tagInput);
                  }
                }}
                disabled={submitting}
              />
              {tagSuggestions.length > 0 && (
                <ul className="tag-suggestions">
                  {tagSuggestions.map((suggestion) => (
                    <li key={suggestion}>
                      <button type="button" onClick={() => addTag(suggestion)}>
                        {suggestion}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <p id="tech-input-hint" className="input-hint">
              技術名を入力してEnterキーで追加できます。カンマ区切りで複数まとめて追加することもできます。
            </p>
            <ul className="tag-chip-list">
              {technologies.map((tag) => (
                <li key={tag}>
                  {tag}
                  <button type="button" onClick={() => removeTag(tag)} aria-label={`${tag}を削除`}>
                    ×
                  </button>
                </li>
              ))}
            </ul>
          </div>

          <fieldset disabled={submitting}>
            <legend>種別</legend>
            {PROJECT_TYPE_OPTIONS.map(({ code, label }) => (
              <label key={code}>
                <input
                  type="checkbox"
                  checked={projectTypes.includes(code)}
                  onChange={() => toggleProjectType(code)}
                />
                {label}
              </label>
            ))}
          </fieldset>

          <fieldset disabled={submitting}>
            <legend>開発工程</legend>
            {DEV_PROCESS_PHASE_OPTIONS.map(({ code, label }) => (
              <label key={code}>
                <input
                  type="checkbox"
                  checked={devProcessPhases.includes(code)}
                  onChange={() => toggleDevProcessPhase(code)}
                />
                {label}
              </label>
            ))}
          </fieldset>
        </section>

        <div className="input-field">
          <label htmlFor="outcome-note">成果・課題・解決策</label>
          <textarea
            id="outcome-note"
            value={outcomeNote}
            onChange={(event) => setOutcomeNote(event.target.value)}
            disabled={submitting}
          />
        </div>

        <div className="input-field">
          <label htmlFor="source-note">確認元メモ</label>
          <textarea
            id="source-note"
            value={sourceNote}
            onChange={(event) => setSourceNote(event.target.value)}
            disabled={submitting}
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="button-primary" disabled={submitting}>
            {submitLabel}
          </button>
          <Link to={cancelTo} className="button-secondary">
            キャンセル
          </Link>
        </div>
      </form>
    </div>
  );
}

export default ProjectForm;
