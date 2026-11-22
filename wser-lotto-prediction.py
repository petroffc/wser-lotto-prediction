#!/usr/bin/env python3

"""
This script calculates lottery odds for the Western States Endurance Run.

It is a Python port of the R script found in Appendix C of
'An Analysis of the Western States Lottery' by Ryan Witko (2016).

Christopher Petroff, November 2026.
"""

import numpy as np
import random
import pandas as pd

# Prompt for number of applicants by year
print('Enter comma separated list of number of applicants by increasing year:\n')
print('---------------------------------')
print('| year 1, year 2, year 3, etc.  |')
print('| (e.g., 4469, 2563, 1752, ...) |')
print('---------------------------------\n')
applicants = [int(x) for x in input().split(',')]
print('')

# Setup variables
# List of years
years = np.arange(0,len(applicants))
# List of tickets per applicant by year
ticketsPerApplicant = []
for index, year in enumerate(applicants):
    # 2^N-1 (we're zero indexed, so the index = N-1)
    ticketsPerApplicant.append(2 ** index)
# Total entries drawn from the lottery (254 in regular lottery + 3 in person)
raceCapacity = 254
# Longest number of years
numCategories = len(applicants)

# Check if there are enough applicants for a lottery
if sum(applicants) <= raceCapacity:
    print('Check number of applicants. (Race is not at capacity‽)')
    raise SystemExit

# Calculate tickets per year
originalTickets = [applicants * ticketsPerApplicant \
                   for applicants, ticketsPerApplicant \
                   in zip(applicants, ticketsPerApplicant)]
# List to update with expected values
ticketCounts = originalTickets

# Iterate through until the race is filled
for _ in np.arange(0,raceCapacity):
    # Calculate initial probability by year
    probOfSelectingCategory = [ticketCount / sum(ticketCounts) \
                               for ticketCount \
                               in ticketCounts]
    # Calculate expected reduction in tickets by year
    expTicketReduction = [probOfSelectingCategory * ticketsPerApplicant \
                          for probOfSelectingCategory, ticketsPerApplicant \
                          in zip(probOfSelectingCategory, ticketsPerApplicant)]
    # Calculate remaining tickets by year
    ticketCounts = [ticketCounts - expTicketReduction \
                    for ticketCounts, expTicketReduction \
                    in zip(ticketCounts, expTicketReduction)]

# Calculate tickets drawn by year
ticketsTaken = [originalTickets - ticketCounts \
                for originalTickets, ticketCounts \
                in zip(originalTickets, ticketCounts)]
# Calculate odds of selection by year
oddsOfSelection = [ticketsTaken / originalTickets \
                   for ticketsTaken, originalTickets \
                   in zip(ticketsTaken, originalTickets)]
# Calculate number of runners selected by year
numPeopleTaken = [oddsOfSelection * applicants \
                  for oddsOfSelection, applicants \
                  in zip(oddsOfSelection, applicants)]

# Make a DataFrame of the results
df = pd.DataFrame([applicants,
                   [str(round(year * 100, 2)) + '%' for year in oddsOfSelection],
                   [int(round(year, 0)) for year in numPeopleTaken]],
                  columns=['Year ' + str(year + 1) for year in years],
                  index=['Applicants', 'Probability', 'Number Drawn'])

# Set pandas display options and print results to terminal
pd.set_option('display.expand_frame_repr', True)
pd.set_option('display.width', 80)
pd.set_option('display.max_columns', None)
print(df)
