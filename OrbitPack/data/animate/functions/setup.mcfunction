# Setup projector screen

execute at @s run summon armor_stand ~ ~ ~ {NoGravity:1b,Silent:1b,Invulnerable:1b,Invisible:1b,NoBasePlate:1b,Tags:["projector"]}
scoreboard objectives add frame_count dummy "Frame Count"
scoreboard players add @e[tag=projector] frame_count 0
execute at @e[tag=projector] run place template start

# Set storage
data modify storage minecraft:frames input set value {frame:0}
