import numpy as np
from random import randint
import matplotlib.pyplot as plt
from student_class import Student
from mechanism_class import Mechanism, CurrentMechanism, PostedPriceMechanism, PayPerMinuteMechanism, OptMechanism

# Define hyper parameters

num_students = 200    # number of students
num_hours = 14        # number of hours
max_time = 10         # maximum time to be allocated to a single student in one office hours session
total_time = 120      # total number of minutes in a single set of office hours

start_time_dist = (lambda: randint(0, num_hours-1))
service_time_dist = (lambda: np.random.gamma(8, 1, size=None))
utility_func = (lambda par_1, time, mean: abs(np.random.normal(10 + par_1, 5))*2.0**(time-mean)/(2.0**(time-mean)+0.5))

# # # # # # # # # # # # # # # # # SAMPLING # # # # # # # # # # # # # # # # # # # # #

utilities = []     # amount of total utility amongst all of the students per trial
Trials = 1         # number of trials to be run

for trials in range(Trials):
    # REMINDER: Auction.generate_students(number of students,
    #                                     how much currency each student gets,
    #                                     distribution of start times,
    #                                     distribution of service times,
    #                                     utility functions,
    #                                     currency rule)

    # CURRENT MECHANISM:
    # Auction = CurrentMechanism([], num_hours, max_time, total_time)
    # Auction.generate_students(200, 0, start_time_dist, service_time_dist, utility_func, (lambda: True))

    # POSTED PRICE MECHANISM:
    # Auction = PostedPriceMechanism([], num_hours, max_time, total_time, list(range(num_hours)))
    # Auction.generate_students(200, 50, start_time_dist, service_time_dist, utility_func, (lambda utility, price: utility >= 15 + price))

    # FAST PASS MECHANISM:
    # Auction = PostedPriceMechanism([], num_hours, max_time, total_time, [1]*num_hours)
    # Auction.generate_students(200, 2, start_time_dist, service_time_dist, utility_func, (lambda utility, price: utility >= 20))

    # PAY PER MINUTE MECHANISM:
    Auction = PayPerMinuteMechanism([], num_hours, max_time, total_time, (10 + np.array(range(num_hours)))/7.8)
    Auction.generate_students(200, 50, start_time_dist, service_time_dist, utility_func, (lambda utility_rate, rate: utility_rate > rate))

    # THEORETICAL OPTIMAL MECHANISM:
    # Auction = OptMechanism([], num_hours, max_time, total_time)
    # Auction.generate_students(200, 0, start_time_dist, service_time_dist, utility_func, (lambda: True))

    Auction.run_auction()

    final_students = Auction.students
    final_utility = 0
    utility_sorted = []
    for student in final_students:
        final_utility += student.total_utility
    utilities.append(final_utility)

utilities.sort()
# utilities = utilities[:10000]
average_utility = np.mean(utilities)
median_utility = np.median(utilities)
print('Mean: %s, Median: %s' % (average_utility, median_utility))
n, bins, patches = plt.hist(utilities, 10, facecolor='blue', alpha=0.5)
plt.xlabel('Total utility')
plt.ylabel('Frequency')
plt.title(r'Current: Trials=%d, n=%d, k=%d, mean=%d, median=%d' %
          (Trials, num_students, num_hours, average_utility, median_utility))
# plt.show()