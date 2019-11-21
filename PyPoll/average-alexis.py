def average(numbers):
    sum = 0.0
    for n in numbers:
        sum += n
    return (sum/len(numbers))

def average_better(numbers):
        return (sum(numbers)/len(numbers))

def average_mean(numbers):
    return(mean(numbers))

def average_comprehension(numbers):
    sum = 0.0
    for n in numbers:
        sum += n
    return (sum/len(numbers))


l = [34, 56, 232, 56.7]

print("Average: %f" % average(l))

print("Average: %f" % average_better(l))

print("Average: %f" % average_mean(l))