def stiffnes(n_elem):

    #code for setting up stifnnes matrix of euler Bernoulli beam

    import numpy as np
    import sys


    fixed_dofs = [0, 1, -1, -2]
    E  =  1 #Pa
    Iz =  1 #m^4
    L  =  1 / n_elem #m

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

   # for dof in fixed_dofs:
   #    for i in [0, 1]: 
   #        k_struct = np.delete(k_struct, dof, axis = i)
   
    k_struct = k_struct[2:-2, 2:-2]#only works for clamped-clamped


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

   # for dof in fixed_dofs:
   #     f = np.delete(f, dof)
    f =  f[2:-2]

    return f 


def random_load_generator(n_elem):
    import random
    import numpy as np

    n_nod = n_elem + 1
    n_dofs = n_nod * 2
    free_dofs = n_dofs - 4 #4 belonging to a clamped-clamped beam
    f = np.zeros(free_dofs)
    for i in range(0, 40, 2):
        if random.choice([True, False]):
            f[i] = random.random()   
    
    return f



def stress_recovery(displ, n_elem):

    import numpy as np
    import ipdb

    x = np.linspace(0, 1, n_elem)

    L = 1 / n_elem

    B_0 = np.array([-6 / L ** 2, - 4 / L, 6 / L ** 2, - 2 / L]) #stress-deformation vector
    B_1 = B_0 + np.array([12 / L ** 3, 6 / L ** 2, - 12 / L ** 3, 6 / L ** 2])

    B_x = lambda x: np.array([- 6 / L ** 2 + 12 * x / L ** 3, \
                              - 4 / L      +  6 * x / L ** 2, \
                                6 / L ** 2 - 12 * x / L ** 3, \
                              - 2 / L      +  6 * x / L ** 2])
    
    timesteps = np.arange(0, np.size(displ, 1))
    stress_elem = np.zeros([n_elem, np.size(timesteps)])

    #ipdb.set_trace()
    #timesteps = np.arange(0, np.size(displ, 1))
    for time in timesteps:
        displ_t = np.concatenate(([0, 0], displ[:, time], [0, 0]))
        for elem in range(n_elem):
           # stress_elem[elem, 0] = - B_0.transpose() @ displ[2*elem:2*elem+4]
           # stress_elem[elem, 1] = - B_1.transpose() @ displ[2*elem:2*elem+4]

           stress_elem[elem, time] = - B_x(L / 2) @ displ_t[2*elem:2*elem+4]


    return stress_elem




def stiff_2nd_order(n_elem):

    #code for setting up 2nd order stifnnes matrix of euler Bernoulli beam
    import numpy as np
    import sys


    #np.set_printoptions(threshold=sys.maxsize)
    #import matplotlib.plot as plt

    fixed_dofs = [1, 0, -2, -1] #assuming clamped-clamped
    T = 1
    L = 1
    Le = L / n_elem
    #local stiffness matrix from 2nd order term
    k = np.array([[6 / 5 * T / Le,  T / 10,\
                  -6 / 5 * T / Le,  T / 10],
                 [ T / 10, 2 * Le * T / 15,\
                  -T / 10,    -Le * T / 30 ],
                 [-6 / 5 * T / Le, -T / 10,\
                   6 / 5 * T / Le, -T / 10],
                 [ T / 10,    -Le * T / 30 ,\
                  -T / 10, 2 * Le * T / 15]])

    dof_node = 2
    dof_elem = 4
    #n_elem   = 21
    tot_dofs = n_elem * dof_node + 2

    k_struct = np.zeros([tot_dofs,tot_dofs])

    for i in range(n_elem):
        k_struct[2*i:2*i+4, 2*i:2*i+4] += k

  #  for dof in fixed_dofs:
  #      for i in [0, 1]: 
  #          k_struct = np.delete(k_struct, dof, axis = i)
    k_struct = k_struct[2:-2, 2:-2]

    return  k_struct



def mass_matrix_HRZ(n_elem):

    #code for setting up mass matrix with HRZ lumping  
    import numpy as np
    import sys


    #np.set_printoptions(threshold=sys.maxsize)
    #import matplotlib.plot as plt

    fixed_dofs = [1, 0, -1, -2] #assuming clamped-clamped
    rho = 1
    A   = 1
    L   = 1
    Le = L / n_elem
    mass  = rho * A * Le
    #local HRZ matrix
    m = np.diag([mass *.5, mass * Le ** 2 / 78, mass * .5, mass * Le ** 2 / 78]) 
    dof_node = 2
    dof_elem = 4
    #n_elem   = 21
    tot_dofs = n_elem * dof_node + 2

    m_struct = np.zeros([tot_dofs,tot_dofs])

    for i in range(n_elem):
        m_struct[2*i:2*i+4, 2*i:2*i+4] += m 

  #  for dof in fixed_dofs:
  #      for i in [0, 1]: 
  #          m_struct = np.delete(m_struct, dof, axis = i)
   
    m_struct = m_struct[2:-2, 2:-2]#only works for clamped clamped

    return  m_struct

def mass_matrix(n_elem):

    #code for setting up mass a consistent mass matrix  
    import numpy as np
    import sys


    #np.set_printoptions(threshold=sys.maxsize)
    #import matplotlib.plot as plt

    fixed_dofs = [1, 0, -1, -2] #assuming clamped-clamped
    rho = 1 #kg/m^3
    A   = 1 #m^2
    L   = 1 #m
    Le = L / n_elem
    mass  = rho * A * Le #kg
    #local mass matrix
    m = mass / 420 * np.array([[156, 22 * Le, 54, -13 * Le], 
                               [22 * Le, 4 * Le ** 2, 13 * Le, -3 * Le ** 2], 
                               [54, 13  * Le, 156, -22 * Le],
                               [-13 * Le, -3 * Le ** 2, -22 * Le, 4 * Le ** 2]])
    dof_node = 2
    dof_elem = 4
    #n_elem   = 21
    tot_dofs = n_elem * dof_node + 2

    m_struct = np.zeros([tot_dofs,tot_dofs])

    for i in range(n_elem):
        m_struct[2*i:2*i+4, 2*i:2*i+4] += m 

  #  for dof in fixed_dofs:
  #      for i in [0, 1]: 
  #          m_struct = np.delete(m_struct, dof, axis = i)
   
    m_struct = m_struct[2:-2, 2:-2]#only works for clamped clamped

    return  m_struct
