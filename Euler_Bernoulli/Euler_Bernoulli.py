def stiffnes(n_elem):

    #code for setting up stifnnes matrix of euler Bernoulli beam

    import numpy as np
    import sys


    #np.set_printoptions(threshold=sys.maxsize)
    #import matplotlib.plot as plt

    fixed_dofs = [1, 0, -2, -1]
    E  =  1
    Iz =  1
    L  =  1 / n_elem

    k = np.array([[12 * E * Iz / L ** 3, 6 * E * Iz / L ** 2,\
                  -12 * E * Iz / L ** 3, 6 * E * Iz / L ** 2],
                 [  6 * E * Iz / L ** 2, 4 * E * Iz / L,\
                   -6 * E * Iz / L ** 2, 2 * E * Iz / L],
                 [-12 * E * Iz / L ** 3,-6 * E * Iz / L ** 2,\
                   12 * E * Iz / L ** 3,-6 * E * Iz / L ** 2],
                 [  6 * E * Iz / L ** 2, 2 * E * Iz / L,\
                   -6 * E * Iz / L ** 2 ,4 * E * Iz / L]])

    dof_node = 2
    dof_elem = 4
    #n_elem   = 21
    tot_dofs = n_elem * dof_node + 2

    k_struct = np.zeros([tot_dofs,tot_dofs])

    for i in range(n_elem):
        k_struct[2*i:2*i+4, 2*i:2*i+4] += k

    for dof in fixed_dofs:
        for i in [0, 1]: 
            k_struct = np.delete(k_struct, dof, axis = i)


    return  k_struct


def nodal_load(load, n_elem):
    #Function that calculates the nodal loads.
    import numpy as np
    
    q = load
    L = 1 / n_elem
    dof_node = 2
    tot_dofs = n_elem * dof_node + 2
    
    
    r_elem = np.array([-q * L / 2, -q * L ** 2 / 12,\
                       -q * L / 2,  q * L ** 2 / 12])
    
   
    fixed_dofs = [1, 0, -2, -1]    
                       
    f = np.zeros([tot_dofs])                   
                       
    for i in range(n_elem):
        f[2*i:2*i+4] += r_elem

    for dof in fixed_dofs:
        f = np.delete(f, dof)


    return f 


def random_load_generator(n_elem):
    import random
    import numpy as np

    n_nod = n_elem + 1
    n_dofs = n_nod * 2
    free_dofs = n_dofs - 4
    f = np.zeros(free_dofs)
    for i in range(0, 40, 2):
        if random.choice([True, False]):
            f[i] = random.random()   
    
    return f



def stress_recovery(displ, n_elem):

    import numpy as np

    x = np.linspace(0, 1, n_elem)

    L = 1 / n_elem

    B_0 = np.array([-6 / L ** 2, - 4 / L, 6 / L ** 2, - 2 / L]) #stress-deformation vector
    B_1 = B_0 + np.array([12 / L ** 3, 6 / L ** 2, - 12 / L ** 3, 6 / L ** 2])

    B_x = lambda x: np.array([- 6 / L ** 2 + 12 * x / L ** 3, \
                              - 4 / L      +  6 * x / L ** 2, \
                                6 / L ** 2 - 12 * x / L ** 3, \
                              - 2 / L      +  6 * x / L ** 2])
    
    stress_elem = np.zeros([n_elem])


    displ = np.concatenate(([0, 0], displ, [0, 0]))

    for elem in range(n_elem):
       # stress_elem[elem, 0] = - B_0.transpose() @ displ[2*elem:2*elem+4]
       # stress_elem[elem, 1] = - B_1.transpose() @ displ[2*elem:2*elem+4]
       stress_elem[elem] = - B_x(L / 2) @ displ[2*elem:2*elem+4]


    return stress_elem




