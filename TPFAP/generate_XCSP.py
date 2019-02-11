'''
A script that creates a XCSP file given a Frequence Asignement Problem
'''

def count_one(matrix, n, p):
    count = 0
    for i in range(n):
        for j in range(p):
            if(matrix[i][j] == 1):
                count += 1
    return count


filename = "fap3.xcsp"
max_constraint_arity = 2
n_parabolas = 4
n_frequencies = 8


#This matrix has an element equal to 1 if frequencies i and j are linked by a constraint
m_constraints = [[0,1,1,1],
                 [1,0,1,1],
                 [1,1,0,1],
                 [1,1,1,0]]

n_agents = count_one(m_constraints, n_parabolas, n_parabolas)
n_variables = count_one(m_constraints, n_parabolas, n_parabolas)
#Il y a deux fois moins de contraintes que de relations de contraintes, car les contraintes sont symétriques :
# R(f1, f2) <==> R(f2, f1)
n_constraints = count_one(m_constraints, n_parabolas, n_parabolas)/2


print(m_constraints.count(1))
if (len(m_constraints) != n_parabolas):
    raise  ValueError("m_relation has wrong dimensions, too many or too few rows, should be " + str(n_parabolas))
for k in range(n_parabolas):
    if (len(m_constraints[k]) != n_parabolas):
        raise ValueError("m_relation has wrong dimensions, too many or too few columns on row number " + str(k) + "\n , should be " + str(n_parabolas) + "\n")

#domain : [1,2,3]

lw_bnd = 1
up_bnd = 4
nb_values_domain = len(range(lw_bnd,up_bnd + 1))


stats=[["number of parabolas", n_parabolas], ["number of frequencies", n_frequencies]]


file = open("XCSP/" + filename, "w")

##################
######HEADER######
##################


file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\n")
file.write("<instance xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
           " xsi:noNamespaceSchemaLocation=\"src/frodo2/algorithms/XCSPschemaJaCoP.xsd\">\n\n")
file.write("  <presentation name=\""+filename +"\" maxConstraintArity=\""+str(max_constraint_arity)+"\" maximize=\"false\" format=\"XCSP 2.1_FRODO\">\n")

for stat in stats :
    file.write("    <stats name=\""+ stat[0]+"\">"+str(stat[1])+"</stats>\n")
file.write("  </presentation>\n\n")

##################
######AGENTS######
##################



agents = []
file.write("  <agents nbAgents=\"" +str(n_agents)+"\">\n")
for i in range(n_parabolas):
    for j in range(n_parabolas):
        if m_constraints[i][j] == 1:
            agent = "a"+ str(i) + "_" + str(j)
            file.write("    <agent name=\""+agent+"\" />\n")
            agents.append(agent)
print("agents : "+ str(agents))
file.write("  </agents>\n\n")

###################
######DOMAINS######
###################

n_domains = 1
domain_name = "d0"

file.write("  <domains nbDomains=\"1\">\n")
file.write("    <domain name=\"" + domain_name +"\" nbValues=\"" + str(nb_values_domain) + "\">" + str(lw_bnd) + ".." + str(up_bnd) + "</domain>\n")
file.write("  </domains>\n\n")

print("domain = " + str(list(range(lw_bnd,up_bnd + 1))))

###################
#####VARIABLES#####
###################


file.write("  <variables nbVariables=\""+str(n_variables)+"\">\n")

variables = []
for i in range(n_parabolas):
    for j in range(n_parabolas):
        if m_constraints[i][j] == 1:
            print((i,j))
            variable_name = "f"+str(i)+"_"+str(j)
            file.write("    <variable name=\""+variable_name+"\" domain=\""+domain_name+"\" agent=\"a"+ str(i) + "_" + str(j) +"\" />\n")
file.write("  </variables>\n\n")


###################
####PREDICATES#####
###################

file.write("  <predicates nbPredicates=\"1\">\n"  
           "    <predicate name=\"FAPINEQ\">\n"  
           "      <parameters> int X int Y</parameters>\n" 
           "      <expression>\n"
           "        <functional> gt(abs(sub(X, Y)), 5) </functional>\n"
           "      </expression>\n"
           "    </predicate>\n"
           "  </predicates>\n\n")


###################
####CONSTRAINTS####
###################

file.write("  <constraints nbConstraints=\""+ str(n_constraints)+"\">\n")

for i in range(n_parabolas):
    for j in range(n_parabolas):
        if m_constraints[i][j] == 1 and i<j:
            file.write("    <constraint name=\"frequencies_f"+ str(i) + "_" + str(j)+"_and_f"+ str(j) + "_" + str(i)+"_don't_interfere\" arity=\"2\" scope=\"f"+str(i)+"_"+str(j)+" f"+str(j)+"_"+str(i)+"\" reference=\"FAPINEQ\" >\n")
            file.write("      <parameters> f"+ str(i) + "_" + str(j)+" f"+ str(j) + "_" + str(i)+" </parameters>\n")
            file.write("    </constraint>\n")
file.write("  </constraints>\n"  
"</instance>")
file.close()