

from __future__ import annotations
import random
from typing import Optional
from queue import PriorityQueue
import time



class Reverter:
    """This class represents an array to be sorted. It formally encodes the states of the problem
    """
    
    def __init__(self,size:int,init=True) -> None:
        """The class only sorts an array containing numbers 1..size. The constructor shuffles the array
        in order to create an unsorted array.

        Args:
            size (int): the size of the array
            init (bool, optional): if True, the array is initialized with value 1..size, the shuffled, else, the array
            remains empty (it is used to clone the array). Defaults to True.
        """
        self.cost = 0  # Initialize the cost attribute
        self.parent = None

        if init:
            self.table=list(range(1,size+1))
            random.shuffle(self.table)
            self.hash()
            self.parent=None
        else:
            self.table=[]
    
    
    def __str__(self) -> str:
        """returns a string representation of the object Reverter

        Returns:
            str: the string representation
        """
        return str(self.table)

    
    def hash(self):
        """Compute a hashcode of the array. Since it is not possible to hash a list, this one is first
        converted to a tuple
        """
        return hash(tuple(self.table))       # hadii modifitha : hash(tuple(self.table))

    def __hash__(self):
        return hash(tuple(self.table)) 
    
    def __eq__(self, __value: Reverter) -> bool:
        """Tests whether the current object if equals to another object (Reverter). The comparison is made by comparing the hashcodes

        Args:
            __value (Reverter): _description_

        Returns:
            bool: True if self==__value, else it is False
        """
        return self.__hash__==__value.__hash__
    
    
    def is_the_goal(self) -> bool :
        """Tests whether the table is already sorted (so that the search is stopped)

        Returns:
            bool: True if the table is sorted, else it is False.
        """
        for i in range(1,len(self.table)):
            if self.table[i-1]>self.table[i]:return False
        return True
    
    
    def clone(self) -> Reverter:
        """This methods create a copy of the current object

        Returns:
            Reverter: the copy to be created
        """
        res=Reverter(len(self.table),False)
        res.table=[*self.table]
        res.parent=self
        return res
    
    def actions(self) -> list[Reverter]:
        """This class builds a list of possible actions. The returned list contains a set of tables depending of possible
        reverting of the current table

        Returns:
            list[Reverter]: the list of tables obtained after applying the possible reverting
        """
        res=[]
        sz=len(self.table)
        for i in range(sz):
            r=self.clone()
            v=self.table[i:]
            v.reverse()
            r.table=self.table[:i]+v
            r.hash()
            res.append(r)
        return res

    def solveBreadth(self) -> Optional[Reverter]:
        """Implements breadth-first search.

        Returns:
            Optional[Reverter]: The sorted table if possible, else None.
        """
        queue = [self]  # Initialize queue with initial state
        visited = set()  # Set to track visited states

        while queue:
            current_state = queue.pop(0)  # Dequeue the front state
            if current_state:
                hash_value = hash(current_state)
            visited.add(current_state.__hash__())  # Mark as visited

            if current_state.is_the_goal():
                return current_state  # Found the goal state

            # Generate all possible actions from the current state
            next_states = current_state.actions()
            for next_state in next_states:
                next_hash = hash(next_state)
                if next_hash not in visited:
                    queue.append(next_state)  # Enqueue new states
        return None  # No solution found
  
   
    
    def solveDepth(self) -> Optional[Reverter]:
        """Implements depth-first search.

        Returns:
            Optional[Reverter]: The sorted table if possible, else None.
        """
        stack = [self]  # Initialize stack with initial state
        visited = set()  # Set to track visited states

        while stack:
            current_state = stack.pop()  # Pop the top state
            visited.add(current_state.__hash__())  # Mark as visited

            if current_state.is_the_goal():
                return current_state  # Found the goal state

            # Generate all possible actions from the current state
            next_states = current_state.actions()
            for next_state in next_states:
                if next_state.__hash__() not in visited:
                    stack.append(next_state)  # Push new states onto the stack
        return None  # No solution found
    
    def solveRandom(self, max_iterations: int = 10000) -> Optional[Reverter]:
        """This method implements random search to find a sorted table.

        Args:
            max_iterations (int): The maximum number of iterations to attempt.

        Returns:
            Optional[Reverter]: The sorted table if found, else None.
        """
        current_state = self
        for _ in range(max_iterations):
            if current_state.is_the_goal():
                return current_state
            actions = current_state.actions()
            current_state = random.choice(actions)
        return None
    
    def solveHeuristic1(self) -> Optional[Reverter]:
        """This method implements heuristic search (heuristic n° 1)

        Returns:
            Optional[Reverter]: the sorted table is possible
        """
        
        raise NotImplementedError("This method is not yet implemented")
    
    def solveHeuristic2(self) -> Optional[Reverter]:
        """This method implements heuristic search (heuristic n° 2)

        Returns:
            Optional[Reverter]: the sorted table is possible
        """
        raise NotImplementedError("This method is not yet implemented")
    #These methods will provide the PriorityQueue with a way to compare Reverter objects by defining an ordering based on their attributes.
    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __gt__(self, other):
        return self.__hash__() > other.__hash__() 

    def UniformCost(self) -> Optional[Reverter]:
        """This method implements heuristic search (your proposed heuristic)
        UCS uses priority queue, priority is the cumulative cost (smaller cost)

        Returns:
            Optional[Reverter]: the sorted table is possible
        """
        queue = PriorityQueue()
        queue.put((0, self))  # (cost, state)
        visited = set()  # Set to keep track of visited states

        while not queue.empty():
            cost, current_state = queue.get()  # Get the state with the lowest cost
            print(f"Current state: {current_state}, Cost: {cost}")  # Debug print

            if current_state.is_the_goal():
                print("Goal found!")  # Debug print
                return current_state  # Found the goal state

            visited.add(current_state.__hash__())  # Add current state to visited set to avoid revisiting

            # Generate all possible actions from the current state
            for next_state in current_state.actions():
                if next_state.__hash__() not in visited:
                    total_cost = cost + self.cost_function(current_state, next_state)
                    queue.put((total_cost, next_state))
                    print(f"Enqueued: {next_state}, Total Cost: {total_cost}")  # Debug print
           
        print("No solution found")  # Debug print
        return None  # No solution found

    def cost_function(self, current_state, next_state):        # For this example, the cost is the number of positions that are out of place
        return 1
    
    
    
    
size=4          #8,...,15,...
rev=Reverter(size,True)
r=rev.UniformCost()
print(r)