from src.services import rag_service

class InsuranceQAAgent:
    def __init__(self):
        # If we needed a separate LLM or vector store client, init here
        pass

    def verify_policy(self, policy_query: str):
        """Check if the policy exists or can be found. Returns standardized ID or False."""
        result = rag_service.find_policy(policy_query)
        # `find_policy` could search a database or documents for the policy name/number
        return result  # e.g., returns policy_id string if found, or False/None if not

    async def answer_question(self, question: str, policy_id: str) -> str:
        """Use RAG to answer a question about the given policy."""
        # We call the query_rag function with the question and policy context
        answer = rag_service.query_policy(question, policy_id)
        # In a real scenario, query_rag might itself use an LLM, so it could be async.
        # Here we assume it's fast or handled synchronously for simplicity.
        return answer
