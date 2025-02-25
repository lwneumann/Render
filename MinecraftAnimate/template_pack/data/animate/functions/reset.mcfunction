schedule clear animate:play
execute at @e[tag=projector] run scoreboard players set @e[tag=projector] frame_count 0
execute store result storage minecraft:frames input.frame int 1 run scoreboard players get @e[tag=projector,limit=1] frame_count
function animate:clear