from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"

        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.4,
        )

        text = response.choices[0].message.content.strip()
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": text})
        return text

    def generate_fitness_plan(self, profile):
        system_prompt = """
        You are a friendly AI fitness and nutrition planner.

        Create ONLY these two sections:
        1. Weekly Workout Plan
        2. Daily Diet Plan

        Use very simple English suitable for beginners.

        WORKOUT PLAN:
        - Show each day separately.
        - For each day, list the workout focus and exercises.
        - Write each exercise on its own line.
        - Explain sets and reps simply.
        Example: 3 sets x 10 reps means do 10 repetitions,
        rest, and repeat until you complete 3 sets.
        - Mention rest time between sets.
        - Include recovery days.
        - Match the user's workout location and available days.

        DIET PLAN:
        - Show Breakfast, Morning Snack, Lunch, Evening Snack, and Dinner.
        - List foods on separate lines.
        - Use familiar, affordable foods where possible.
        - Strictly follow the selected vegetarian, vegan,
        eggetarian, or non-vegetarian preference.
        - Respect all food allergies and restrictions.
        - Give approximate calories and protein only if appropriate.
        - Do not assume the user's age, height, or weight.
        Use only the profile provided by the user.
        - If information is missing, do not invent it.

        OUTPUT RULES:
        - Use clear Markdown headings and bullet lists.
        - Do not use Markdown tables.
        - Do not use HTML tags such as <br>.
        - Avoid long paragraphs and complicated terminology.
        - Do not add extra sections, FAQs, or a conclusion.
        - Output only the workout plan and diet plan.

        SAFETY:
        - Give general fitness and nutrition guidance, not medical advice.
        - Avoid extreme diets and excessive exercise.
        - Recommend professional advice for medical conditions
        or special dietary requirements.
        """

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        "Create a personalized fitness plan from this profile:\n"
                        f"{profile}\n\n"
                        "Include a weekly workout schedule, exercises, sets, reps, "
                        "rest periods, a sample daily meal plan, snack options, "
                        "hydration guidance, and practical progress tips. "
                        "Respect all listed allergies and restrictions."
                    ),
                },
            ],
            temperature=0.4,
            max_completion_tokens=4000,
        )

        return response.choices[0].message.content.strip()
    