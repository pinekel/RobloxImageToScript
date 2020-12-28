from PIL import Image
import math

#Image to script
#By pinekel

#V1


#Image selection
imageDirection = raw_input("Name of image to convert.\n>")
outputDirection = raw_input("Name of output script.\n>")

image = Image.open(imageDirection)
image = image.convert('RGB')
data = image.load()

script = open(outputDirection + ".lua", "w")
script.write("data = {")

size = image.size

#Conversion

for y in range(size[1]):
    script.write("{")
    for x in range(size[0]):
        pixelData = data[x, y]
        script.write("{%s, %s, %s}"%(str(pixelData[0]), str(pixelData[1]), str(pixelData[2])))
        if x != size[0]-1:
            script.write(", ")
    if y != size[1]-1:
            script.write("}, ")
    print "Finished row %s"%str(y+1)
print "Finished data translation"
script.write("}}")
script.write("""
local height = %s
local width = %s

local origin = {0, 0, 0}

local template = Instance.new("Part")
template.Anchored = true
template.CanCollide = false
template.Material = "SmoothPlastic"
template.Size = Vector3.new(0.05, 0.05, 0.05)
template.Rotation = Vector3.new(90, 0, 0)

local timeLastWaited = tick()

print("Converting data...")
for y = 1, height do
    for x = 1, width do
        local pixel = template:Clone()
        local color = data[y][x]
        
        pixel.Color = Color3.fromRGB(color[1], color[2], color[3])
        pixel.Position = Vector3.new((origin[1]+x)/20, (origin[2])/20, (origin[3]+y)/20)
        pixel.Parent = script

        if tick()-timeLastWaited > 1 then
            timeLastWaited = tick()
            wait(0)
        end
    end
end

print("Done")
"""%(size[1], size[0]))

script.close()
