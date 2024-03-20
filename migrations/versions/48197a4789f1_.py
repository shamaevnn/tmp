"""

Revision ID: 48197a4789f1
Revises:
Create Date: 2024-03-20 14:06:15.243192

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "48197a4789f1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "events",
        sa.Column(
            "id", sa.String(), server_default=sa.text("gen_random_uuid()::varchar"), nullable=False
        ),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bets",
        sa.Column(
            "id", sa.String(), server_default=sa.text("gen_random_uuid()::varchar"), nullable=False
        ),
        sa.Column("amount", sa.DECIMAL(precision=2), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("event_id", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bets_event_id"), "bets", ["event_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_bets_event_id"), table_name="bets")
    op.drop_table("bets")
    op.drop_table("events")
    # ### end Alembic commands ###
