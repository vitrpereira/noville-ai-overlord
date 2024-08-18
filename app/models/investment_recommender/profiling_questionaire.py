

class ProfilingQuestionaire:
    def __init__(self):
        ...

    def calculate_risk_profile(self, responses):
        scores = self.scores()
        total_score = 0

        for question, answer in responses.items():
            if question in scores and answer in scores[question]:
                total_score += scores[question][answer]
        
        if total_score <= 70:
            profile = "Conservative"
        elif total_score <= 140:
            profile = "Moderate"
        else:
            profile = "Aggressive"
        
        return profile, total_score
    
    @staticmethod
    def questionaire():
        questions = {
            'time_horizon': 'How long do you plan to keep your money invested?',
            'investment_knowledge': 'How would you classify your investment knowledge?',
            'risk_tolerance': 'Let\'s say your investments drop by 25%. What would you do?',
            'investment_objectives': 'What do you want to achieve with your investments?',
            'income_stability': 'How would you classify your income stability?',
            'liquidity_needs': 'How quickly you need would you need to retrieve your money back?',
        }
        return questions

    @staticmethod
    def scores():
        scores = {
            'time_horizon': {
                'Less than 1 year': 0,
                '1 to 3 years': 10,
                '3 to 5 years': 20,
                '5 to 10 years': 30,
                'More than 10 years': 40
            },
            'investment_knowledge': {
                'Just getting started': 0,
                'Know a thing or two': 10,
                'Moderate': 20,
                'Advanced': 30,
                'Expert': 40
            },
            'risk_tolerance': {
                'Sell everything': 0,
                'Sell some investments': 10,
                'Do nothing': 20,
                'Buy more': 30
            },
            'investment_objectives': {
                'Preserve my equity': 0,
                'Income generation': 10, 
                'Balanced growth': 20,
                'Aggressive growth': 30
            },
            'income_stability': {
                'Very unstable': 0,
                'Unstable': 10,
                'Somewhat stable': 20,
                'Stable': 30,
                'Very stable': 40
            },
            'liquidity_needs': {
                'Very important': 0,
                'Somewhat important': 10,
                'Not very important': 20,
                'Not important at all': 30
            }
        }

        return scores