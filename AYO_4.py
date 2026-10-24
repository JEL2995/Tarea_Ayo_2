# Pseaudo code for SA
# function SIMULATED-ANNEALING(problem, schedule) returns a state
#   current = problem.INITIAL_STATE
#   for t = 1 to infinity do
#     T = schedule(t)
#     if T = 0 then return current
#     next = RANDOM_SUCCESSOR(current)       # Diff 1: Random pick (not best)
#     delta_E = next.VALUE - current.VALUE
#     if delta_E > 0 then
#       current = next
#     else
#       current = next with probability e^(delta_E / T) # Diff 2: Accept bad moves
