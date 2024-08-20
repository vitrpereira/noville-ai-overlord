from profiler import Profiler
from openai_model import OpenAiModel
from head_prompt import HEAD_PROMPT_INVESTMENT_HELPER

class InvestmentBot:
    def __init__(self):
        self.profiler = Profiler()
        self.questions = self.profiler.questionnaire()
        self.openai_model = OpenAiModel()
        self.responses = {}
        self.current_question = None
        self.head_prompt = HEAD_PROMPT_INVESTMENT_HELPER
        self.greeted = False
        self.completed = False  # Track if the conversation is complete

    def initial_conversation(self, user_message):
        if not self.greeted:
            self.greeted = True
            self.current_question = list(self.questions.keys())[0]
            return self.call_model(self.build_question(self.current_question), user_message)
        
        if self.completed:
            return self.call_model(
                system_attachment=f"{self.risk_profile()}",
                user_message=user_message
            )

        if self.current_question and self.current_question not in self.responses:
            self.update_responses(self.current_question, user_message)
            next_question = self.ask_next_question()

            if next_question:
                response_message = self.build_question(next_question)
            else:
                response_message = self.risk_profile()
                self.completed = True  # Mark as completed
                self.current_question = None  # Clear current question

            return self.call_model(response_message, user_message)

    def ask_next_question(self):
        unanswered_questions = [q for q in self.questions if q not in self.responses]

        if unanswered_questions:
            self.current_question = unanswered_questions[0]
            return self.current_question
        else:
            return None
    
    def build_question(self, question):
        return f"QUESTION TO ASK: {self.questions[question]} OPTIONS TO PROVIDE: {self.get_options_for_question(question)}"
    
    def call_model(self, system_attachment, user_message):
        if self.completed:
            # Only send the final result, no additional prompts
            system_prompt = f"PASS IT TO THE USER [RISK TOLERANCE RESULT] {system_attachment}"
        else:
            # Include the head prompt and additional prompt for ongoing questions
            system_prompt = f"{self.head_prompt}\n[ADDITIONAL PROMPT]: {system_attachment}"
        
        return self.openai_model.generate_conversation(
                system_prompt=system_prompt,
                head_prompt=self.head_prompt,
                user_message=user_message
        )

    def update_responses(self, question, answer):
        self.responses[question] = answer.strip()

    def get_options_for_question(self, question):
        scores = self.profiler.scores()
        if question in scores:
            return " / ".join(scores[question].keys())
        return ""

    def risk_profile(self):
        profile, risk_score = self.profiler.calculate_risk_profile(self.responses)
        return f"The user risk profile is: '{profile}'. Their risk score: {risk_score}."
