USA = { S_i = {} }
for i = 0, 63 do
    for j = 0, 63 do
        USA.S_i[string.format("%d,%d,%d", i, j, math.random(0, 1))] = 1
    end
end

function N(x, y, S)
    local n = 0
    for i = -1, 1 do
        for j = -1, 1 do
            local alive = S[string.format("%d,%d,%d", (x + i) % 64, (y + j) % 64, 1)]
            if not (i == 0 and j == 0) and alive then
                n = n + 1
            end
        end
    end
    return n
end

function USA.delta_a(element, S)
    local result = {}
    local x, y, a = string.match(element, "(%d+),(%d+),(%d+)")
    x, y, a = tonumber(x), tonumber(y), tonumber(a)
    local neighbors = N(x, y, S)
    if a == 1 and (neighbors < 2 or neighbors > 3) then
        result[string.format("%d,%d,%d", x, y, 0)] = 1
    elseif a == 0 and neighbors == 3 then
        result[string.format("%d,%d,%d", x, y, 1)] = 1
    end
    return result
end

function USA.delta_b(element, S)
    local result = {}
    for _, _ in pairs(USA.delta_a(element, S)) do
        result[element] = 1
    end
    return result
end

function USA.update()
    local A, B = {}, {}
    for element, _ in pairs(USA.S_i) do
        for addElement, _ in pairs(USA.delta_a(element, USA.S_i)) do
            A[addElement] = 1
        end
        for subElement, _ in pairs(USA.delta_b(element, USA.S_i)) do
            B[subElement] = 1
        end
    end
    for addElement, _ in pairs(A) do
        USA.S_i[addElement] = 1
    end
    for subElement, _ in pairs(B) do
        USA.S_i[subElement] = nil
    end
end

function love.draw()
    love.graphics.clear(0.9, 0.9, 0.9)
    for element, _ in pairs(USA.S_i) do
        local x, y, a = string.match(element, "(%d+),(%d+),(%d+)")
        x, y, a = tonumber(x), tonumber(y), tonumber(a)
        love.graphics.setColor(1 - a, 1 - a, 1 - a)
        love.graphics.rectangle("fill", 144 + x * 8, 44 + y * 8, 8, 8)
    end
    USA.update()
end
