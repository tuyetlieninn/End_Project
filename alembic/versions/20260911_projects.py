"""Create the projects table.

Revision ID: 20260911_projects
Revises: 20260909_tech_tags
Create Date: 2026-09-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260911_projects"
down_revision: Union[str, Sequence[str], None] = "20260909_tech_tags"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("customer_name", sa.String(length=255), nullable=False),
        sa.Column("project_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_date", sa.String(length=10), nullable=False),
        sa.Column("end_date", sa.String(length=10), nullable=True),
        sa.Column("is_ongoing", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("team_size", sa.Integer(), nullable=True),
        sa.Column("total_man_month", sa.Float(), nullable=True),
        sa.Column("source_note", sa.Text(), nullable=True),
        sa.Column("industry", sa.String(length=255), nullable=True),
        sa.Column("outcome_note", sa.Text(), nullable=True),
        sa.Column("team_composition_note", sa.Text(), nullable=True),
        sa.Column("technologies_csv", sa.String(length=2000), nullable=False, server_default=""),
        sa.Column("project_types_csv", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("dev_process_phases_csv", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("projects")