import json
import math
import copy

dA = 1
dB = 0.5    #0.5 default
feed = 0.055
k = 0.062

################################################################################
# helper functions
def populateList(length, value):
    list = []
    for i in range(length):
        list.append(value)
    return list

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def mesh_laplaceA(vertex_index, neighb_indices):
    neighbAvg = 0
    for i in neighb_indices:
        neighbAvg += meshA[i]
    neighbAvg /= len(neighb_indices)
    diff = neighbAvg - meshA[vertex_index]
    #print(diff)
    return diff 

def mesh_laplaceB(vertex_index, neighb_indices):
    neighbAvg = 0
    for i in neighb_indices:
        neighbAvg += meshB[i]
    neighbAvg /= len(neighb_indices)
    diff = neighbAvg - meshB[vertex_index]
    #print(diff)
    return diff

################################################################################
# Open JSON file
f = open(r'C:\Users\Prinz\Desktop\Projects\ISF\reaction_diffusion_repo\rd_existing_mesh\data\existing_mesh_data.json')
  
# returns JSON object as a dictionary
data = json.load(f)

#get the number mesh verticies
vertex_count = len(data['convolution_indices'])

# get laplace function order 
conv_groups = []
for i in data['convolution_indices']:
    conv_groups.extend([i])

# get seed pts numbers
seed_indices = []
for i in data['seed_indices']:
    seed_indices.append(i)

# Close file
f.close()

# check imported data
assert len(conv_groups) == vertex_count, "convolution groups don't match vertex count"
assert len(seed_indices) == len(data['seed_indices']), "seed not imported correctly"

# ################################################################################
# initialize A/B values
meshA = populateList(vertex_count,1)
nextA = populateList(vertex_count,1)
visA = populateList(vertex_count,1)    
meshB = populateList(vertex_count,0)
nextB = populateList(vertex_count,0)
visB = populateList(vertex_count,0)   

# plant B seed 
for i in seed_indices:
    meshB[i] = 1
    nextB[i] = 1

visualize = {}
visualize['seed'] = nextB[:]    #debug seed

# ################################################################################
# Main Loop
count = 0
jcount = 0
for i in range(100):
    #for j in range(len(laplace_indices)):
    for j in range(vertex_count):
        v_neighbors = conv_groups[j]    #neighbors for laplace
        a = meshA[j]
        b = meshB[j]

        #get next values 
        nextA[j] = a + (dA * mesh_laplaceA(j, v_neighbors)) - (a * b * b) + (feed * (1 - a))
        nextB[j] = b + (dB * mesh_laplaceB(j, v_neighbors)) + (a * b * b) - ((k + feed) * b)

        visA[j] = round(nextA[j], 2)  
        visB[j] = round(nextB[j], 2)  

        # Loop debugger
        # if i == 9:
            # print(j, ':', v_neighbors, ':', a , ':', b)
            # print('LA:', round(mesh_laplaceA(j, v_neighbors),2))
            # print('LB:', round(mesh_laplaceB(j, v_neighbors),2))

        jcount += 1
    count += 1
    print(count)

    tempA = meshA[:]
    meshA = nextA[:]
    nextA = tempA[:]

    tempB = meshB[:]
    meshB = nextB[:]
    nextB = tempB[:]

print(count)
print(jcount)
print('done calculating')

# ################################################################################

visualize['visA'] = visA
visualize['visB'] = visB

results = []
for i in range(len(nextA)):
    a = nextA[i]
    b = nextB[i]
    c = math.floor((a - b) * 255)
    c = constrain(c, 0, 255)
    results.append(c)

visualize['results'] = results

################################################################################
# test seed
json_object = json.dumps(visualize, indent=4)
with open(r'C:\Users\Prinz\Desktop\Projects\ISF\reaction_diffusion_repo\rd_existing_mesh\data\visualize.json', "w") as outfile:
    outfile.write(json_object)
outfile.close()



