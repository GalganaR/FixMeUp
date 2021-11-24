class Student:
    def __init__(self, index, currency, utility_funcs, time_allot_week, currency_rule):
        self.index = index                             # Keeps track of student for debugging purposes
        self.currency = currency                       # Amount of money left, double
        self.utility_funcs = utility_funcs             # Utility functions over the week, list of lambda functions
        self.utility_func = self.utility_funcs[0]      # Current day's utility function, lambda function
        self.total_utility = 0                         # How much utility this student has obtained so far
        self.time_allot_week = time_allot_week         # List of doubles representing how much time they want to be seen
        self.time_allot_day = self.time_allot_week[0]  # Double representing how much time they want to be seen today
        self.currency_rule = currency_rule             # How much utility is needed for the student to pay posted price, lambda_function
        self.counter = 1

    def update(self, currency_used, new_utility):
        self.currency -= currency_used          # Subtract off how much currency the student used
        self.total_utility += new_utility       # Increase total utility
        if self.counter < len(self.time_allot_week):
            self.utility_func = self.utility_funcs[self.counter]
            self.time_allot_day = self.time_allot_week[self.counter]
            self.counter += 1