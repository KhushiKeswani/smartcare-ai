"""create doctors and doctor schedules tables

Revision ID: 20260626_0002
Revises: 20260617_0001
Create Date: 2026-06-26
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260626_0002"
down_revision: str | None = "20260617_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "doctors",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=True),
        sa.Column("doctor_code", sa.String(length=32), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("specialization", sa.String(length=120), nullable=False),
        sa.Column("department", sa.String(length=120), nullable=False),
        sa.Column("license_number", sa.String(length=80), nullable=False),
        sa.Column("consultation_fee", sa.Numeric(10, 2), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("doctor_code"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("license_number"),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_doctors_department", "doctors", ["department"])
    op.create_index("ix_doctors_doctor_code", "doctors", ["doctor_code"])
    op.create_index("ix_doctors_email", "doctors", ["email"])
    op.create_index("ix_doctors_is_available", "doctors", ["is_available"])
    op.create_index("ix_doctors_license_number", "doctors", ["license_number"])
    op.create_index("ix_doctors_phone", "doctors", ["phone"])
    op.create_index("ix_doctors_specialization", "doctors", ["specialization"])
    op.create_index("ix_doctors_status", "doctors", ["status"])
    op.create_index("ix_doctors_user_id", "doctors", ["user_id"])

    op.create_table(
        "doctor_schedules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("doctor_id", sa.String(length=36), nullable=False),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("slot_duration_minutes", sa.Integer(), nullable=False),
        sa.Column("max_patients", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["doctor_id"], ["doctors.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_doctor_schedules_day_of_week", "doctor_schedules", ["day_of_week"])
    op.create_index("ix_doctor_schedules_doctor_id", "doctor_schedules", ["doctor_id"])


def downgrade() -> None:
    op.drop_index("ix_doctor_schedules_doctor_id", table_name="doctor_schedules")
    op.drop_index("ix_doctor_schedules_day_of_week", table_name="doctor_schedules")
    op.drop_table("doctor_schedules")
    op.drop_index("ix_doctors_user_id", table_name="doctors")
    op.drop_index("ix_doctors_status", table_name="doctors")
    op.drop_index("ix_doctors_specialization", table_name="doctors")
    op.drop_index("ix_doctors_phone", table_name="doctors")
    op.drop_index("ix_doctors_license_number", table_name="doctors")
    op.drop_index("ix_doctors_is_available", table_name="doctors")
    op.drop_index("ix_doctors_email", table_name="doctors")
    op.drop_index("ix_doctors_doctor_code", table_name="doctors")
    op.drop_index("ix_doctors_department", table_name="doctors")
    op.drop_table("doctors")
