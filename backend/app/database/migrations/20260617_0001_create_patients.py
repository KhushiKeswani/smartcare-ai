"""create patients and medical history tables

Revision ID: 20260617_0001
Revises:
Create Date: 2026-06-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260617_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("patient_code", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", sa.String(length=32), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("emergency_contact", sa.String(length=255), nullable=True),
        sa.Column("blood_group", sa.String(length=8), nullable=True),
        sa.Column("insurance_provider", sa.String(length=120), nullable=True),
        sa.Column("insurance_number", sa.String(length=120), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("patient_code"),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_patients_email", "patients", ["email"])
    op.create_index("ix_patients_patient_code", "patients", ["patient_code"])
    op.create_index("ix_patients_phone", "patients", ["phone"])
    op.create_index("ix_patients_user_id", "patients", ["user_id"])

    op.create_table(
        "patient_medical_history",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("patient_id", sa.String(length=36), nullable=False),
        sa.Column("visit_date", sa.Date(), nullable=False),
        sa.Column("doctor_name", sa.String(length=160), nullable=False),
        sa.Column("department", sa.String(length=120), nullable=False),
        sa.Column("diagnosis", sa.String(length=255), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_patient_medical_history_patient_id",
        "patient_medical_history",
        ["patient_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_patient_medical_history_patient_id", table_name="patient_medical_history")
    op.drop_table("patient_medical_history")
    op.drop_index("ix_patients_user_id", table_name="patients")
    op.drop_index("ix_patients_phone", table_name="patients")
    op.drop_index("ix_patients_patient_code", table_name="patients")
    op.drop_index("ix_patients_email", table_name="patients")
    op.drop_table("patients")
