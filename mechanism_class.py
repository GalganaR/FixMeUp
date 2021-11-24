from abc import abstractmethod
from student_class import Student
import random
import numpy as np
import heapq


class Mechanism:

    def __init__(self, students, num_hours, max_time, total_time):
        self.students = students          # array of students
        self.num_hours = num_hours        # number of office hours held
        self.max_time = max_time          # maximum amount of time to allocate to a single student in one set of hours
        self.total_time = total_time      # the total amount of time each set of hours lasts
        self.remaining_time = total_time  # initialize remaining time to be the total time in one set of hours
        self.time_counter = 0

    # Create a single student with given currency, start and service time distributions, utility functions, and a currency rule
    def generate_student(self, index, currency, start_time_dist, service_time_dist, utility_func, currency_rule):
        start_time = start_time_dist()                     # Determines when the student starts their homework
        service_times = [0] * start_time                   # 0 service time when they haven't started the homework
        student_utilities = [lambda time: 0] * start_time  # 0 utility when they haven't started the homework
        for j in range(self.num_hours - start_time):
            service_time = service_time_dist()
            service_times.append(service_time)
            student_utilities.append(lambda time: np.sign(time) * utility_func(start_time + j, time, service_time - 2))
        return Student(index, currency, student_utilities, service_times, currency_rule)

    # Creates a group of students with the given parameters
    def generate_students(self, num_students, currency, start_time_dist, service_time_dist, utility_func, currency_rule):
        for i in range(num_students):
            self.students.append(
                self.generate_student(i, currency, start_time_dist, service_time_dist, utility_func, currency_rule))

    # runs the entire week's worth of office hours
    def run_auction(self):
        for i in range(self.num_hours):
            self.run_single()

    # runs a single office hours session and updates the students
    def run_single(self):
        pass


# Uses the current mechanism
class CurrentMechanism(Mechanism):

    def __init__(self, students, num_hours, max_time, total_time):
        Mechanism.__init__(self, students, num_hours, max_time, total_time)

    def run_single(self):
        self.remaining_time = self.total_time
        for student in self.students:
            time_allocated = min(self.remaining_time, self.max_time, student.time_allot_day)
            utility = student.utility_func(time_allocated)
            student.update(0, utility)
            self.remaining_time -= time_allocated
        random.shuffle(self.students)


# Uses the posted price mechanism
class PostedPriceMechanism(Mechanism):

    def __init__(self, students, num_hours, max_time, total_time, posted_prices):
        Mechanism.__init__(self, students, num_hours, max_time, total_time)
        self.posted_prices = posted_prices  # array of posted prices, one price per day
        self.counter = 0                    # will help determine the posted price per day

    def run_single(self):
        self.remaining_time = self.total_time
        posted_price = self.posted_prices[self.counter]
        no_pass_students = []

        # If one has the sufficient currency and the currency rule
        for student in self.students:
            time_allocated = min(self.remaining_time, self.max_time, student.time_allot_day)
            utility = student.utility_func(time_allocated)
            if student.currency >= posted_price and student.currency_rule(utility, posted_price):
                student.update(posted_price, utility)
                self.remaining_time -= time_allocated
            else:
                no_pass_students.append((student, utility, time_allocated))

        # This implementation guarantees that the last student's question(s) are fully answered
        for student, utility, time_allocated in no_pass_students:
            if self.remaining_time > 0:
                student.update(0, utility)
                self.remaining_time -= time_allocated
            else:
                student.update(0, 0)
                self.remaining_time = 0

        random.shuffle(self.students)
        self.counter += 1


# Uses the pay-per-minute mechanism
class PayPerMinuteMechanism(Mechanism):

    def __init__(self, students, num_hours, max_time, total_time, rates):
        Mechanism.__init__(self, students, num_hours, max_time, total_time)
        self.rates = rates  # Array of utility per minute rates, one for each day
        self.counter = 0    # Keeps track of the utility per minute rate per day

    def run_single(self):
        self.remaining_time = self.total_time
        rate = self.rates[self.counter]
        no_pass_students = []

        for student in self.students:
            time_allocated = min(self.remaining_time, self.max_time, student.time_allot_day)
            utility_rate = student.utility_func(time_allocated)/(time_allocated + 0.01)
            if student.currency_rule(utility_rate, rate) and student.currency >= time_allocated * rate:
                student.update(time_allocated * rate, utility_rate * time_allocated)
                self.remaining_time -= time_allocated
            else:
                no_pass_students.append((student, utility_rate, time_allocated))

        # This implementation assumes that the last student's question(s) are fully answered
        for student, utility_rate, time_allocated in no_pass_students:
            utility = utility_rate * time_allocated
            if self.remaining_time > 0:
                student.update(0, utility)
                self.remaining_time -= time_allocated
            else:
                student.update(0, 0)
                self.remaining_time = 0


# Uses the theoretical near-optimum greedy strategy
class OptMechanism(Mechanism):

    def __init__(self, students, num_hours, max_time, total_time):
        Mechanism.__init__(self, students, num_hours, max_time, total_time)

    def run_single(self):
        self.remaining_time = self.total_time
        unsorted_list = []
        for student in self.students:
            time_allocated = min(self.remaining_time, self.max_time, student.time_allot_day)
            utility_per_time = student.utility_func(time_allocated)/(time_allocated + 0.01)
            unsorted_list.append((utility_per_time, time_allocated, student))

        sorted_list = sorted(unsorted_list, key=lambda x: -x[0])

        # This implementation assumes that the last student's question(s) are fully answered
        for utility_per_time, time_allocated, student in sorted_list:
            utility = utility_per_time * time_allocated
            if self.remaining_time > 0:
                student.update(0, utility)
                self.remaining_time -= time_allocated
            else:
                student.update(0, 0)
                self.remaining_time = 0