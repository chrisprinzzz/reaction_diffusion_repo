import json
################################################################################
# Helper Functions
def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def print2dList(L):
    print(repr2dList(L))

################################################################################
# import data
# Open JSON file
f = open(r'C:\Users\Prinz\Desktop\Projects\ISF\ReactionDiffusion\data\jsons\mesh_attributes.json')
  
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
# check grids

