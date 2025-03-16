"""Initial migration

Revision ID: 1
Revises: 
Create Date: 2025-03-16 23:02:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = '1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create files table
    op.create_table('files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('original_path', sa.String(), nullable=True),
        sa.Column('storage_path', sa.String(), nullable=True),
        sa.Column('file_type', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('error', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('embedding', Vector(1536), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_files_filename'), 'files', ['filename'], unique=False)
    op.create_index(op.f('ix_files_file_type'), 'files', ['file_type'], unique=False)
    op.create_index(op.f('ix_files_status'), 'files', ['status'], unique=False)
    op.create_index(op.f('ix_files_created_at'), 'files', ['created_at'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_files_created_at'), table_name='files')
    op.drop_index(op.f('ix_files_status'), table_name='files')
    op.drop_index(op.f('ix_files_file_type'), table_name='files')
    op.drop_index(op.f('ix_files_filename'), table_name='files')
    op.drop_table('files')
