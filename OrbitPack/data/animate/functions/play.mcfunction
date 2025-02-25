
# Places frames and increments frame count. Scheduled at FPS?
execute store result storage minecraft:frames input.frame int 1 run scoreboard players get @e[tag=projector,limit=1] frame_count
function animate:place_frame with storage minecraft:frames input
execute at @e[tag=projector] run scoreboard players add @e[tag=projector] frame_count 1

schedule function animate:play 0.033s