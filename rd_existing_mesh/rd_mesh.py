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

# get pts
pts = []
for i in data['mesh_verticies']:
    #access pt attributes via 0,1,2 (X,Y,Z)
    X = i['pt']['X']
    Y = i['pt']['Y']
    Z = i['pt']['Z']
    pt = [X, Y, Z]
    pts.append(pt)

# get laplace function order 
laplace_indices = []
for i in data['laplace_indices']:
    laplace_indices.append(i)

# get vertex neighbors
neighbors = []
for i in data['vertex_neighbors']:
    neighbors.extend([i])

# get seed pts numbers
s = []
for i in data['seed_pts']:
    s.append(i)

# Close file
f.close()

# check imported data
assert len(laplace_indices) == len(pts), "laplace and pts lists are different lengths"
assert len(neighbors) == len(laplace_indices), "vertex neighbors and pts list are diff lengths"
assert len(s) == len(data['seed_pts'])

################################################################################
# initialize A/B values
meshA = populateList(len(pts),1)
nextA = populateList(len(pts),1)
visA = populateList(len(pts),1)
initialA = populateList(len(pts),42)     
meshB = populateList(len(pts),0)
nextB = populateList(len(pts),0)
visB = populateList(len(pts),0)   
initialB = populateList(len(pts),42)

# plant B seed 
for i in s:
    meshB[i] = 1
    nextB[i] = 1

visualize = {}
visualize['seed'] = copy.deepcopy(nextB)

################################################################################
# Main Loop
count = 0
jcount = 0
for i in range(100):
    #for j in range(len(laplace_indices)):
    for j in laplace_indices:
        v_neighbors = neighbors[j]    #neighbors for laplace
        a = meshA[j]
        b = meshB[j]

        #get next values 
        nextA[j] = a + (dA * mesh_laplaceA(j, v_neighbors)) - (a * b * b) + (feed * (1 - a))
        nextB[j] = b + (dB * mesh_laplaceB(j, v_neighbors)) + (a * b * b) - ((k + feed) * b)

        visA[j] = round(nextA[j], 2)  
        visB[j] = round(nextB[j], 2)  

        # Loop debugger
        if i == 9:
            # print(j, ':', v_neighbors, ':', a , ':', b)
            # print('LA:', round(mesh_laplaceA(j, v_neighbors),2))
            # print('LB:', round(mesh_laplaceB(j, v_neighbors),2))
            initialA[j] = a
            initialB[j] = b
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

################################################################################

visualize['visA'] = visA
visualize['visB'] = visB
visualize['initialA'] = initialA
visualize['initialB'] = initialB

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



