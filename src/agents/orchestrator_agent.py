import os
from src.agents.zip_code_agent import ZipCodeAgent
from src.agents.insurance_qa_agent import InsuranceQAAgent
from src.agents.policy_mapping import resolve_policy, load_policy_mapping

class OrchestratorAgent:
    def __init__(self):
        self.state = "ASK_NAME"
        self.name = None
        self.location = None
        self.policy_id = None
        self.zip_agent = ZipCodeAgent(api_key=os.getenv("GOOGLE_MAPS_API_KEY"))
        self.qa_agent = InsuranceQAAgent()  # might not need API key if local

        self.llm_model = os.getenv("LLM_MODEL", "OPENAI_GPT4.1")

    def reset_session(self):
        """Reset conversation state at start of a new chat."""
        self.state = "ASK_NAME"
        self.name = None
        self.location = None
        self.policy_id = None

    def get_greeting(self):
        return "Hi! 👋 What’s your name?"

    async def handle_message(self, user_input) -> str:
        if self.state == "ASK_NAME":
            self.name = user_input.strip()
            self.state = "ASK_ZIP"
            return f"Nice to meet you, {self.name}! What’s your ZIP code?"

        elif self.state == "ASK_ZIP":
            zip_code = user_input.strip()
            if not zip_code.isdigit() or len(zip_code) not in (5, 9):
                return "That doesn’t look like a valid ZIP code. Please enter a 5-digit ZIP."
            city, state, hospitals = await self.zip_agent.lookup(zip_code)
            if city and state:
                self.location = (city, state)
                self.state = "ASK_POLICY"
                nearest_hosp = hospitals[0] if hospitals else "an in-network hospital"
                return (f"Great, I see you’re in {city}, {state}. " 
                        f"The nearest in-network hospital I found is {nearest_hosp}. "
                        "Please enter your policy number or policy name.")
            else:
                return "Sorry, I couldn’t find that location. Could you double-check your ZIP code?"


        elif self.state == "ASK_POLICY":
            policy_query = user_input.strip()
            policy_id, exact = resolve_policy(policy_query)
            if policy_id is None:
                return "❌ I couldn’t find that policy. Try again."
            self.policy_id = policy_id
            self.state = "CHAT"
            policy_name = load_policy_mapping()[policy_id]
            if not exact:
                print(f"[PolicyResolver] Assumed policy: {user_input} → {policy_name}")
                return (
                    f"I couldn’t find an exact match, but assuming you meant **{policy_name}**. "
                    "If this is correct, please go ahead and ask your question."
                )
            else:
                return (
                    f"Thanks! You are covered under the **{policy_name}** policy. "
                    "How can I assist you today?"
                )

        elif self.state == "CHAT":
            question = user_input
            answer = await self.qa_agent.answer_question(question, self.policy_id)
            return answer

        else:
            return "Sorry, something went wrong with the conversation flow."
