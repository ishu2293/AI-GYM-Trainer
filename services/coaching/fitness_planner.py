
import json
import os
import sqlite3
from datetime import datetime
import re
import html
import streamlit as st


DB_PATH = os.path.join(os.getcwd(), "data.db")


def init_fitness_planner_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fitness_plans (
                user_id INTEGER PRIMARY KEY,
                profile_json TEXT NOT NULL,
                plan_text TEXT,
                updated_at TEXT NOT NULL
            )
        """)
        conn.commit()


def load_fitness_plan(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT profile_json, plan_text, updated_at
            FROM fitness_plans
            WHERE user_id = ?
            """,
            (int(user_id),),
        ).fetchone()

    if not row:
        return None

    return {
        "profile": json.loads(row[0]),
        "plan": row[1] or "",
        "updated_at": row[2],
    }


def save_fitness_plan(user_id, profile, plan_text):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO fitness_plans
                (user_id, profile_json, plan_text, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                profile_json = excluded.profile_json,
                plan_text = excluded.plan_text,
                updated_at = excluded.updated_at
            """,
            (
                int(user_id),
                json.dumps(profile),
                plan_text,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()


def clean_fitness_plan(text):
    # Convert HTML line breaks to real newlines.
    text = re.sub(
        r"<br\s*/?>",
        "\n",
        text,
        flags=re.IGNORECASE,
    )

    # Remove common HTML formatting tags.
    text = re.sub(
        r"</?(?:p|div|span|strong|b|em|i|ul|ol|li)\b[^>]*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Decode entities such as &amp; and &nbsp;.
    text = html.unescape(text)

    # Keep only the two requested sections.
    match = re.search(
        r"(?im)^\s*#{0,3}\s*(?:\d+[.)]\s*)?"
        r"(Weekly Workout Schedule|Weekly Workout Plan)\s*:?\s*$",
        text,
    )

    if match:
        text = text[match.start():]

    # Remove content after the diet plan.
    end_match = re.search(
        r"(?im)^\s*#{1,3}\s+"
        r"(?:Additional Information|Conclusion|Disclaimer|FAQs|"
        r"Extra Tips|Further Recommendations)\b.*$",
        text,
    )

    if end_match:
        text = text[:end_match.start()]

    return text.strip()



def render_fitness_planner(user_id, llm_coach):
    init_fitness_planner_db()

    saved = load_fitness_plan(user_id)
    saved_profile = saved["profile"] if saved else {}

    st.title("🥗 AI Diet & Workout Planner")
    st.write(
        "Create a fitness plan based on your goals, schedule, "
        "diet preferences, and available equipment."
    )

    # Set defaults only once, so edits are preserved during reruns.
    defaults = {
        "planner_goal": "Muscle gain",
        "planner_diet": "Vegetarian",
        "planner_location": "Gym",
        "planner_level": "Beginner",
        "planner_age": 20,
        "planner_height": 160.0,
        "planner_weight": 55.0,
        "planner_days": "4 days",
        "planner_equipment": "Standard gym equipment",
        "planner_allergies": "",
        "planner_restrictions": "",
    }

    profile_fields = {
        "planner_goal": "goal",
        "planner_diet": "diet",
        "planner_location": "location",
        "planner_level": "level",
        "planner_age": "age",
        "planner_height": "height_cm",
        "planner_weight": "weight_kg",
        "planner_days": "days",
        "planner_equipment": "equipment",
        "planner_allergies": "allergies",
        "planner_restrictions": "restrictions",
    }

    for key, default in defaults.items():
        if key not in st.session_state:
            field = profile_fields[key]
            st.session_state[key] = saved_profile.get(field, default)

    with st.form("fitness_profile_form"):
        st.subheader("Your fitness profile")

        goal = st.selectbox(
            "Fitness goal",
            ["Muscle gain", "Weight loss", "General fitness",
             "Strength and endurance"],
            key="planner_goal",
        )

        diet = st.selectbox(
            "Diet preference",
            ["Vegetarian", "Vegan", "Eggetarian", "Non-vegetarian"],
            key="planner_diet",
        )

        location = st.selectbox(
            "Where will you exercise?",
            ["Gym", "Home", "Both home and gym"],
            key="planner_location",
        )

        level = st.selectbox(
            "Fitness level",
            ["Beginner", "Intermediate", "Advanced"],
            key="planner_level",
        )

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age", min_value=13, max_value=100,
                step=1, key="planner_age",
            )
            height = st.number_input(
                "Height (cm)", min_value=80.0, max_value=250.0,
                step=1.0, key="planner_height",
            )

        with col2:
            weight = st.number_input(
                "Weight (kg)", min_value=20.0, max_value=350.0,
                step=1.0, key="planner_weight",
            )
            days = st.selectbox(
                "Workout frequency",
                ["2 days", "3 days", "4 days", "5 days", "6 days"],
                key="planner_days",
            )

        equipment = st.text_input(
            "Available equipment",
            key="planner_equipment",
            help="For example, dumbbells, resistance bands, or gym machines.",
        )

        allergies = st.text_input(
            "Food allergies",
            key="planner_allergies",
            placeholder="e.g. peanuts, milk",
        )

        restrictions = st.text_input(
            "Other dietary needs or preferences",
            key="planner_restrictions",
            placeholder="e.g. lactose-free, budget-friendly meals",
        )

        generate = st.form_submit_button(
            "Generate & Save My Plan",
            type="primary",
            use_container_width=True,
        )

    if generate:
        profile = {
            "goal": goal,
            "diet": diet,
            "location": location,
            "level": level,
            "age": int(age),
            "height_cm": float(height),
            "weight_kg": float(weight),
            "days": days,
            "equipment": equipment.strip() or "Not specified",
            "allergies": allergies.strip() or "None specified",
            "restrictions": restrictions.strip() or "None specified",
        }

        if not llm_coach:
            st.error(
                "AI planning is unavailable. Check your Groq API key "
                "and model configuration."
            )
        else:
            try:
                with st.spinner("Creating your personalized plan..."):
                    raw_plan = llm_coach.generate_fitness_plan(profile)
                    plan = clean_fitness_plan(raw_plan)
                    save_fitness_plan(user_id, profile, plan)

                st.session_state["planner_current_plan"] = plan
                st.session_state["planner_saved_at"] = datetime.now().strftime(
                    "%d %b %Y, %I:%M %p"
                )
                st.success("Your plan has been generated and saved!")

            except Exception as e:
                st.error(f"Could not generate the plan: {e}")

    # Show the saved plan after generation or when reopening the page.
    saved = load_fitness_plan(user_id)
    current_plan = st.session_state.get("planner_current_plan")

    if saved:
        st.divider()
        st.subheader("Your saved plan")
        st.caption(f"Last saved: {saved['updated_at']}")

        if st.button("Load Latest Saved Plan", use_container_width=True):
            st.session_state["planner_current_plan"] = saved["plan"]
            st.rerun()

        if current_plan is None:
            current_plan = saved["plan"]

    if current_plan:
        st.markdown(current_plan, unsafe_allow_html=False)

    st.caption(
        "Safety note: AI-generated plans are general guidance, not medical "
        "advice. Nutrition estimates are approximate. Consult a qualified "
        "professional for medical conditions, special dietary needs, "
        "or persistent pain."
    )
