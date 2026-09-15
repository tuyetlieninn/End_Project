"""update project model spec 61"""

revision = 'ef66ec8a31b9'
down_revision = '59e5ec314e02'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('projects', sa.Column('customer_name', sa.String(255), nullable=False))
    op.add_column('projects', sa.Column('project_name', sa.String(255), nullable=False))
    op.add_column('projects', sa.Column('is_ongoing', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('projects', sa.Column('team_size', sa.Integer(), nullable=False))
    op.add_column('projects', sa.Column('total_man_month', sa.Integer(), nullable=False))
    op.add_column('projects', sa.Column('source_note', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('industry', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('outcome_note', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('team_composition_note', sa.String(), nullable=True))

    op.add_column('projects', sa.Column('technologies_csv', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('project_types_csv', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('dev_process_phases_csv', sa.String(), nullable=True))

    op.add_column('projects', sa.Column('created_by', sa.Integer(), nullable=False))


def downgrade():
    op.drop_column('projects', 'customer_name')
    op.drop_column('projects', 'project_name')
    op.drop_column('projects', 'is_ongoing')
    op.drop_column('projects', 'team_size')
    op.drop_column('projects', 'total_man_month')
    op.drop_column('projects', 'source_note')
    op.drop_column('projects', 'industry')
    op.drop_column('projects', 'outcome_note')
    op.drop_column('projects', 'team_composition_note')

    op.drop_column('projects', 'technologies_csv')
    op.drop_column('projects', 'project_types_csv')
    op.drop_column('projects', 'dev_process_phases_csv')

    op.drop_column('projects', 'created_by')
