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

MODIFICACIÓN DEL EXAMEN: si hay una dependencia a un paquete que no existe en la lista de paquetes, se debe ignorar y dar por bueno. 

 """ 


def package_dependency_solver(packages: dict[str, list[str]]) -> list[str]:

    ordenados = []
    for paq in packages.keys():
        ordenados.append(paq)
    
    ordenados.sort()
    out = []
    copy = packages.copy()

    for key in copy.keys():
        copy[key] = sorted(copy[key])
        for paq in copy[key]:
            if paq not in ordenados:
                copy[key].remove(paq)              

    while ordenados:
        nodep = []
        for paq in ordenados:
            if len (copy[paq]) == 0:
                nodep.append(paq)

        if len(nodep) ==0:
            return []

        for dep in nodep:
            out.append(dep)
            copy.pop(dep)
            ordenados.remove(dep)

        for dep in nodep:
            for paqlist in copy.values():
                try:
                    paqlist.remove(dep)
                except:
                    ...
      
    return out


def package_dependency_solver2(packages: dict[str, list[str]]) -> list[str]:
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
