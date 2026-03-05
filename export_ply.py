# Simple exporter: write positions (+ optional rgb) from a SOPtoCHOP Null CHOP to a PLY file.
# Usage: put this script in a Text DAT inside TouchDesigner, edit chopPath/outPath, then Run.

chopPath = '/project1/null_inst'   # <- 修改为你的 SOPtoCHOP 输出的 Null CHOP 路径
outPath = 'C:/temp/pointcloud.ply' # <- 修改为目标路径

chop = op(chopPath)
if not chop:
    raise Exception("CHOP not found: " + chopPath)

# CHOP channels list
chanNames = [c.name for c in chop.channels()]

def has_channel(name):
    return name in chanNames

# determine number of points
if has_channel('tx'):
    n = len(chop['tx'].vals)
elif chop.numSamples > 0:
    n = len(chop.channels()[0].vals)
else:
    n = 0

# detect color channels
color_keys = None
if all(k in chanNames for k in ('r','g','b')):
    color_keys = ('r','g','b')
elif all(k in chanNames for k in ('Cd_r','Cd_g','Cd_b')):
    color_keys = ('Cd_r','Cd_g','Cd_b')

with open(outPath, 'w') as f:
    # PLY header (ascii)
    f.write('ply\\nformat ascii 1.0\\n')
    f.write(f'element vertex {n}\\n')
    f.write('property float x\\nproperty float y\\nproperty float z\\n')
    if color_keys:
        f.write('property uchar red\\nproperty uchar green\\nproperty uchar blue\\n')
    f.write('end_header\\n')
    # Write vertices
    for i in range(n):
        if has_channel('tx'):
            x = chop['tx'].vals[i]
            y = chop['ty'].vals[i] if has_channel('ty') else 0.0
            z = chop['tz'].vals[i] if has_channel('tz') else 0.0
        else:
            ch = chop.channels()
            x = ch[0].vals[i] if len(ch) > 0 else 0.0
            y = ch[1].vals[i] if len(ch) > 1 else 0.0
            z = ch[2].vals[i] if len(ch) > 2 else 0.0

        if color_keys:
            r = int(max(0, min(255, chop[color_keys[0]].vals[i]*255)))
            g = int(max(0, min(255, chop[color_keys[1]].vals[i]*255)))
            b = int(max(0, min(255, chop[color_keys[2]].vals[i]*255)))
            f.write(f'{x} {y} {z} {r} {g} {b}\\n')
        else:
            f.write(f'{x} {y} {z}\\n')

print(f'Wrote {n} points to {outPath}')