""" 

Write a function called package_dependency_solver that takes a dictionary
where keys are package names and values are lists of dependencies
(other packages that must be installed first).
The function should return a list of packages in the correct order of installation.

A package can only be installed if all its dependencies have already been installed.

If two or more packages are ready to be installed at the same time,
they should be added to the result in alphabetical order.

If a circular dependency exists
(e.g., Package A needs Package B, and Package B needs Package A),
the function must return an empty list [].

If the input dictionary is empty, return an empty list [].

>>> package_dependency_solver({"tal": ["hola", "que"], "que": ["hola"], "hola": []})
['hola', 'que', 'tal']

>>> package_dependency_solver({"A": ["B"], "B": ["A"]})
[]

>>> package_dependency_solver({"main": ["lib"], "lib": []})
['lib', 'main']

 """

def test(packages: dict[str, list[str]]) -> list[str]:
    # Make a copy so we don't destroy the original data
    deps = {pkg: list(d) for pkg, d in packages.items()}
    result = []

    deps =packages.copy()

    while deps:
        # 1. Find all packages that currently have NO dependencies
        # Sorting here handles the "alphabetical order" rule perfectly
        ready = sorted([pkg for pkg, d in deps.items() if not d])

        # 2. If nobody is ready but we still have packages, it's a CIRCULAR dependency
        if not ready:
            return []

        # 3. Take the first ready package (alphabetical)
        current = ready[0]
        result.append(current)

        # 4. Remove it from our tracking dictionary
        del deps[current]

        # 5. Remove 'current' from the dependency lists of all remaining packages
        for pkg in deps:
            if current in deps[pkg]:
                deps[pkg].remove(current)

    return result


def package_dependency_solver(packages: dict[str, list[str]]) -> list[str]:
    """ peeling the onion
    1. make a copy of the packages dict 
    --- while the deps exists: ----
    2. find packages with NO dependencies
    3. if dosent exist, return empty list
    4. take first package of the ready list and put it to the current
    remove it from the tracing
    5. in the remaining packages, remove the current one 
    """
    pkg = {pack: sorted(l) for pack, l in packages.items()}

    result = []

    while pkg:
        no_dep = []
        for pack, llist in pkg.items():
            if len(llist) == 0:
                no_dep += [pack]

        if len(no_dep) == 0:
            return []

        no_dep.sort()

        for remove in no_dep:
            pkg.pop(remove)
            result += [remove]

        for pack, llist in pkg.items():
            for l in list(llist):
                if l not in pkg:
                    llist.remove(l)

    return result



print(package_dependency_solver({"tal": ["hola", "que"], "que": ["hola"], "hola": []}))
print("['hola', 'que', 'tal']")
print()
print(package_dependency_solver({"tal": ["hola", "que"], "que": ["hola","adios"], "hola": []}))
print("['hola', 'que', 'tal']")
print()
print(package_dependency_solver({"tal": ["hola", "que"], "que": ["hola","adios"], "hola": [], "eh!":["nopo"]}))
print("['hola', 'eh!', 'que', 'tal']")
print()
print(package_dependency_solver({"tal": ["hola", "que"], "que": ["hola","adios"], "hola": [], "eh!":[]}))
print("['eh!', 'hola', 'que', 'tal']")
print()
print(package_dependency_solver({"A": ["B"], "B": ["A"]})) # []
print("[]")
print()
print(package_dependency_solver({"main": ["lib"], "lib": []})) # ['lib', 'main']
print("['lib', 'main']")
print()
