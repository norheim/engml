from depexpressions import Expression

# Example code for playing with expressions
e = Expression()

e.add(1)
e.add(2, [1])

e.add(1)

# Create independent expressions
e.add(5)
e.add(7)
e.add(3)

# Dependent expression definitions
e.add(11, [5, 7])
e.add(8, [7, 3])
e.add(2, [11])
e.add(9, [11])
e.add(10, [3])

# Updating dependency definitions
e.add(7, [10])

# Propagating independent expressions changes
e.propagate(3)

# Redifinition again
e.add(7, [])
e.propagate(3)
