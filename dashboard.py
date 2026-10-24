
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

DB_PATH = "data.db"


def show_dashboard(user_id):
    st.title("📊 My Fitness Dashboard")
    st.write("Track your workout progress and consistency.")

    try:
        conn = sqlite3.connect(DB_PATH)

        df = pd.read_sql_query(
            """
            SELECT exercise_name, reps, sets, time, created_at
            FROM exercises
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            conn,
            params=(user_id,)
        )

        conn.close()

    except Exception as e:
        st.error(f"Could not load workout history: {e}")
        return

    if df.empty:
        st.info("No workouts recorded yet. Complete your first workout!")
        return

    df["reps"] = pd.to_numeric(df["reps"], errors="coerce").fillna(0)
    df["sets"] = pd.to_numeric(df["sets"], errors="coerce").fillna(0)
    df["created_at"] = pd.to_datetime(
        df["created_at"], errors="coerce"
    )

    df = df.dropna(subset=["created_at"])

    if df.empty:
        st.info("Workout dates are missing or invalid.")
        return

    total_reps = int(df["reps"].sum())
    total_sets = int(df["sets"].sum())
    total_sessions = len(df)

    st.subheader("Your Overall Progress")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Reps", total_reps)
    col2.metric("Total Sets", total_sets)
    col3.metric("Workout Records", total_sessions)

    st.divider()

    # Weekly progress
    st.subheader("Weekly Workout Progress")

    df["week"] = (
        df["created_at"].dt.to_period("W")
        .dt.start_time
    )

    weekly = (
        df.groupby("week", as_index=False)
        .agg(
            total_reps=("reps", "sum"),
            total_sets=("sets", "sum")
        )
    )

    fig = px.bar(
        weekly,
        x="week",
        y="total_reps",
        title="Reps Completed Each Week",
        labels={
            "week": "Week Starting",
            "total_reps": "Total Reps"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    # Exercise-wise progress
    st.subheader("Exercise-wise Performance")

    exercise_stats = (
        df.groupby("exercise_name", as_index=False)
        .agg(
            total_reps=("reps", "sum"),
            total_sets=("sets", "sum")
        )
    )

    fig2 = px.bar(
        exercise_stats,
        x="exercise_name",
        y="total_reps",
        color="exercise_name",
        title="Total Reps by Exercise"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Workout history
    st.subheader("Recent Workout History")

    st.dataframe(
        df[
            ["created_at", "exercise_name", "reps", "sets"]
        ].rename(columns={
            "created_at": "Date",
            "exercise_name": "Exercise",
            "reps": "Reps",
            "sets": "Sets"
        }),
        use_container_width=True,
        hide_index=True
    )
