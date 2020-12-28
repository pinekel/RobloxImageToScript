from PIL import Image
import math

#Image to script
#By pinekel

#V2


#Image loading
imageName = raw_input("Enter the name of the image to convert ( including file extension )\n>")
outputName = raw_input("Enter the name of the output script\n>")

image = Image.open(imageName)
image.convert("RGB")

data = image.load()
output = open(outputName + ".lua", "w")

width = image.width
height = image.height

#Convertion

chunkWidth = 22
chunkHeight = 22
#Dimentions of chunk unions ( Large chunk sizes results in distortion or error )

chunks = []

chunkI = 0
for chunkRow in range(int(math.ceil(height/chunkHeight))+1):
    for chunkCol in range(int(math.ceil(width/chunkWidth))+1):
        chunks.append([])
        for row in range(chunkHeight):
            if row+(chunkRow*chunkHeight) > height-1:
                continue
            chunks[chunkI].append([])
            for col in range(chunkWidth):
                if col+(chunkCol*chunkWidth) > width-1:
                    continue
                chunks[chunkI][row].append(data[col+(chunkCol*chunkWidth), row+(chunkRow*chunkHeight)])
        chunkI+=1
        print "Finished chunk " + str(len(chunks))

    chunkI+=1
    chunks.append(0)


output.write("local chunks = " + str(chunks).replace("[", "{").replace("]", "}").replace("(", "{").replace(")", "}"))

output.write("""

local width = %s
local height = %s

local chunkWidth = %s
local chunkHeight = %s

local origin = {0, 0, 0}

local template = Instance.new("Part")
template.Material = "SmoothPlastic"
template.Size = Vector3.new(0.05, 0.05, 0.05)
template.CanCollide = false
template.Anchored = true

local model = Instance.new("Model")
model.Parent = workspace
model.Name = script.Name

local chunkRow = 1
local chunkCol = 1

local lastPercent = 0

print("Beginning conversion...")
for i = 1, #chunks do
    local chunk = chunks[i]
    
    if math.round((i / #chunks) * 100) ~= lastPercent then
        lastPercent = math.round((i / #chunks) * 100)
        print(lastPercent .. "%% Complete...")
    end
    
    if chunk == 0 then
        chunkCol = 1
        chunkRow = chunkRow + 1
    else
        local chunkPixels = {}
        local chunkI = 0
        
        for row = 1, #chunk do
            for col = 1, #chunk[row] do
                chunkI = chunkI + 1
                
                local pixel = template:Clone()
                pixel.Color = Color3.fromRGB(chunk[row][col][1], chunk[row][col][2], chunk[row][col][3])
                pixel.Position = Vector3.new((origin[1]-(row + (chunkRow*chunkHeight)))/20, (origin[2])/20, (origin[3]+(col + (chunkCol*chunkWidth)))/20)

                if chunkI ~= #chunk*#chunk[row] then
                    chunkPixels[chunkI] = pixel
                elseif #chunkPixels ~= 1 then
                    pixel.Parent = script
                    local union = pixel:UnionAsync(chunkPixels)
                    union.Parent = model

                    pixel:Destroy()
                    for _, chunkPixel in pairs(chunkPixels) do
                        chunkPixel:Destroy()
                    end
                end
            end
        end
        chunkCol = chunkCol + 1
    end
end

print("Complete!")
"""%(width, height, chunkWidth, chunkHeight))

print "Done!"
output.close()