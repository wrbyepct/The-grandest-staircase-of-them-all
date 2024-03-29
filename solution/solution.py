
"""
Approach:
1. We can divide the possibilities into "steps variations"
    i.e.: When bricks = 6
          possibilities = 2 steps variations + 3 steps variations

    I convert them into algebras for convenience :

        TP = total possibilities
        P = steps variation possibilities
        S = steps
        B = bricks
        M = max_steps(B)
    So it's:
        TP = P(2S) + P(3S) + .... + P(MS)

2. The pattern to get the possibilities of N bricks:
       result  = precursor[ start     +    end (if not exists it's 0) ]
       ---------------------------------------
       B.P(2S) =         1     + (B - 2).P(2S)
       B.P(3S) = (B - 2).P(2S) + (B - 3).P(3S)
       B.P(4S) = (B - 3).P(3S) + (B - 4).P(4S)
                .
                .
                .
       B.P(MS) = (B - (M - 1)).P((M - 1)S) + (B - M).P(MS)

3. Simple recursion will create too many stacks, instead we can build the 2D array along the way
   So we can directly get the values from precursors, no callbacks needed
"""
"""
2022/10/28 updated specs version:

steps_variation(n, s):   { n >= 3 /\ s >= 2 /\ value:N /\ m = n - s}                        # Precondition
                         if
                           s = 2 -> value := roundUp((n - 3 + 1) / 2)                       # IFG statement
                           s > 2 -> m < 3        -> value := 0
                                    m = (3 \/ 4) -> value := 1
                                    m = 5        -> value := 2
                                    m > 5        -> value := steps_variation(m, s) + steps_variation(m, s - 1)
                         fi           
                         { \/ value = roundUp((n - 3 + 1) / 2) 
                           \/ value = 0 
                           \/ value = 1 
                           \/ value = 2
                           \/ value = steps_variation(m, s) + steps_variation(m, s - 1) }   # Post-condition
                           
                           
maxSteps(n): { n >= 3 }                                                                # Precondition
               base_bricks := 2                                                        # Initialization
                 max_steps := 1
             { n > base_bricks /\ max_steps = base_bricks - 1}                         # Loop condition & Loop invariant
               do n > base_bricks                                                      # DO statement
               ->  max_steps := base_bricks,
                           n := n - base_bricks,
                  base_steps := base_steps + 1,     
               od         
             { n <= base_steps /\ max_steps = base_bricks - 1 }                        # Post-condition( ~LC /\ LI )

total_variation(n, max_base_step): { n >= 3 /\ max_base_step >= 2 }
                                         i := 2
                                     total := 0
                                   { 2 <= i <= max_base_step /\ total = (+ s | 2 <= s < i : steps_variation(n, s)) }
                                     do 2 <= i <= max_base_step 
                                     -> total := total + steps_variation(n, s), 
                                            i := i + 1 
                                   { i > max_base_step /\ total = (+ s | 2 <= s < i : steps_variation(n, s)) }
"""
 

def get_min_bricks_for_steps():
    min_brick_list = {}
    distance = 3
    bricks = 3
    for i in range(3, 20):
        bricks += distance
        min_brick_list[i] = bricks
        distance += 1
    return min_brick_list


min_bricks_dict = get_min_bricks_for_steps()


def solution(bricks):
    # Base cases
    staircase_table = [
        [1, 0],      # N = 3
        [1, 0],      # N = 4
        [2, 0],      # N = 5
        [2, 1, 0]    # N = 6, corresponding steps variations [P(2S), P(3S), P(4S) ... etc]
    ]
    index = bricks - 3
    # If it's base case simply return the possibility sum
    if bricks == 3 or bricks == 4 or bricks == 5 or bricks == 6:
        return sum(staircase_table[index])

    # Build the 2D array along the way
    goal = bricks + 1
    for b in range(7, goal):
        iterations = get_max_steps(b) - 1
        bricks_possibilities = []
        i = b - 3    # index for currently building bricks combination
        for j in range(iterations):
            steps = j + 2
            possibilities = get_possibilities_of_n_steps(steps, staircase_table, i)
            bricks_possibilities.append(possibilities)
        # Simply add 0 to the end of the list for future accessing, so we don't need a try except error catching
        bricks_possibilities.append(0)
        staircase_table.append(bricks_possibilities)
    return sum(staircase_table[index])


def get_possibilities_of_n_steps(steps, table, index):
    # According to the patterns
    if steps == 2:
        return table[index - 2][0] + 1

    start = table[index - steps][steps - 3]
    end = table[index - steps][steps - 2]

    return start + end


def get_max_steps(bricks):
    # Get the maximum steps the bricks can build
    for steps in min_bricks_dict:
        if bricks - min_bricks_dict[steps] < 0:
            return steps - 1

    return 19  # Max steps is 19, for bricks <= 200


for i in range(3, 200):
    print(solution(i))
