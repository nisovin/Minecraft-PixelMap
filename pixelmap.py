from os import listdir
from os import nice
from os.path import isfile, join, getmtime
from nbt.region import RegionFile
from PIL import Image
import traceback
import time

regionPath = "/home/game/gameserver/world/region/"
outputPath = "/home/game/map/"
useHeightmap = "WORLD_SURFACE" # WORLD_SURFACE / LIGHT_BLOCKING / MOTION_BLOCKING / MOTION_BLOCKING_NO_LEAVES

def main():

	nice(20)

	for file in listdir(regionPath):
		if file.find(".mca") > 0:
		
			rmod = getmtime(regionPath + file)
			imod = 0
			if isfile(outputPath + file + ".png"):
				imod = getmtime(outputPath + file + ".png")
				
			if rmod > imod:
				attempts = 0
				while attempts < 3:
					try:
						attempts += 1
						RegionMap(file)
						attempts = 5
					except:
						print "  Failed to read region file"
						time.sleep(3)
				
			else:
				print "Skipping " + file

	js = "var images = [];\n"
	for file in listdir(outputPath):
		if file.find(".png") > 0:
			js += "images.push('" + file + "');\n"
	file = open(outputPath + "images.js", "w")
	file.write(js)
	file.close()


class RegionMap:

	def __init__(self, filename):
		print "Processing region file " + filename
		colormap = BlockColorMap()
		file = open(regionPath + filename, 'rb')
		region = RegionFile(fileobj = file)

		img = Image.new('RGBA', (32 * 16, 32 * 16))
		for c in region.get_chunks():
			cx = c['x']
			cz = c['z']			
			chunk = Chunk(region, cx, cz)			
			if chunk.status != 'postprocessed':
				continue
			for x in range(0, 16):
				for z in range(0, 16):
					col = chunk.getColumnInfo(x, z)
					color = colormap.getColor(col)
					img.putpixel((cx * 16 + x, cz * 16 + z), color)
		img.save(outputPath + filename + ".png")
			
		file.close()

class BlockColorMap:

	map = {}

	def __init__(self):
		self.map = {}
		
		self.map["stone"] = (90, 90, 90)
		self.map["coal_ore"] = (90, 90, 90)
		self.map["iron_ore"] = (90, 90, 90)
		self.map["mossy_stone_bricks"] = (90, 90, 90)
		self.map["chiseled_stone_bricks"] = (90, 90, 90)
		self.map["cracked_stone_bricks"] = (90, 90, 90)
		self.map["andesite"] = (90, 90, 90)
		self.map["diorite"] = (90, 90, 90)
		self.map["granite"] = (172, 140, 125)
		self.map["polished_andesite"] = (90, 90, 90)
		self.map["polished_diorite"] = (90, 90, 90)
		self.map["polished_granite"] = (172, 140, 125)
		self.map["mossy_cobblestone"] = (80, 80, 80)
		self.map["cobblestone_wall"] = (80, 80, 80)
		self.map["mossy_cobblestone_wall"] = (80, 80, 80)
		self.map["stone_slab"] = (90, 90, 90)
		self.map["infested_stone"] = (90, 90, 90)
		self.map["bone_block"] = (218, 214, 192)
		
		self.map["grass_block"] = (66, 100, 57)
		self.map["grass_path"] = (143, 121, 68)
		self.map["grass"] = (66, 100, 57)
		self.map["fern"] = (115, 176, 99)
		self.map["tall_grass"] = (115, 176, 99)
		self.map["large_fern"] = (115, 176, 99)
		self.map["dirt"] = (94, 68, 46)
		self.map["coarse_dirt"] = (94, 68, 46)
		self.map["podzol"] = (148, 88, 32)
		self.map["mycelium"] = (119, 100, 104)
		self.map["farmland"] = (80, 42, 14)
		self.map["clay"] = (149, 155, 164)
		
		self.map["dead_bush"] = (148, 99, 40)
		self.map["pumpkin"] = (206, 122, 27)
		self.map["melon"] = (163, 163, 38)
		self.map["dandelion"] = (241, 248, 53)
		self.map["poppy"] = (247, 15, 22)
		self.map["blue_orchid"] = (41, 174, 251)
		self.map["allium"] = (191, 117, 251)
		self.map["azure_bluet"] = (229, 234, 242)
		self.map["red_tulip"] = (211, 58, 23)
		self.map["orange_tulip"] = (222, 115, 31)
		self.map["white_tulip"] = (243, 243, 243)
		self.map["pink_tulip"] = (234, 190, 234)
		self.map["oxeye_daisy"] = (234, 230, 173)
		self.map["sunflower"] = (242, 228, 49)
		self.map["lilac"] = (222, 192, 226)
		self.map["rose_bush"] = (247, 15, 22)
		self.map["peony"] = (227, 184, 247)
		self.map["wheat"] = (213, 219, 69)
		self.map["sugar_cane"] = (80, 169, 30)
		self.map["nether_wart"] = (166, 37, 49)
		self.map["vine"] = (66, 100, 57)
		self.map["lily_pad"] = (66, 100, 57)
		self.map["cactus"] = (12, 102, 25)
		
		self.map["water"] = (102, 118, 235)
		self.map["bubble_column"] = (102, 118, 235)
		self.map["seagrass"] = (102, 118, 235)
		self.map["tall_seagrass"] = (102, 118, 235)
		self.map["kelp"] = (102, 118, 235)
		self.map["kelp_plant"] = (102, 118, 235)
		
		self.map["sea_lantern"] = (153, 187, 178)
		self.map["prismarine"] = (104, 172, 150)
		self.map["prismarine_bricks"] = (63, 124, 100)
		self.map["dark_prismarine"] = (53, 79, 64)
		
		self.map["lava"] = (200, 86, 16)
		self.map["magma_block"] = (190, 73, 18)
		self.map["netherrack"] = (136, 16, 16)
		self.map["red_nether_brick"] = (117, 20, 32)
		self.map["soul_sand"] = (56, 40, 29)
		self.map["quartz_block"] = (222, 220, 214)
		self.map["chiseled_quartz_block"] = (222, 220, 214)
		self.map["quartz_pillar"] = (222, 220, 214)
		self.map["quartz_slab"] = (222, 220, 214)
		self.map["quartz_stairs"] = (222, 220, 214)
		
		self.map["sand"] = (225, 219, 166)
		self.map["red_sand"] = (180, 103, 44)
		self.map["sandstone"] = (225, 219, 166)
		self.map["cut_sandstone"] = (225, 219, 166)
		self.map["gravel"] = (120, 120, 120)
		self.map["obsidian"] = (28, 23, 38)
		
		self.map["oak_log"] = (78, 61, 39)
		self.map["stripped_oak_log"] = (186, 149, 93)
		self.map["oak_leaves"] = (42, 121, 3)
		self.map["oak_sapling"] = (42, 121, 3)
		self.map["spruce_log"] = (35, 23, 11)
		self.map["stripped_spruce_log"] = (130, 96, 56)
		self.map["spruce_leaves"] = (68, 111, 68)
		self.map["spruce_sapling"] = (68, 111, 68)
		self.map["birch_log"] = (138, 137, 136)
		self.map["stripped_birch_log"] = (179, 153, 94)
		self.map["birch_leaves"] = (97, 129, 61)
		self.map["birch_sapling"] = (97, 129, 61)
		self.map["dark_oak_log"] = (15, 10, 3)
		self.map["stripped_dark_oak_log"] = (74, 60, 37)
		self.map["dark_oak_leaves"] = (15, 62, 0)
		self.map["dark_oak_sapling"] = (15, 62, 0)
		self.map["acacia_log"] = (43, 39, 35)
		self.map["stripped_acacia_log"] = (154, 90, 56)
		self.map["acacia_leaves"] = (31, 77, 10)
		self.map["acacia_sapling"] = (31, 77, 10)
		self.map["jungle_log"] = (91, 72, 29)
		self.map["stripped_jungle_log"] = (164, 137, 80)
		self.map["jungle_leaves"] = (58, 147, 24)
		self.map["jungle_sapling"] = (58, 147, 24)
		self.map["red_mushroom_block"] = (173, 21, 19)
		self.map["brown_mushroom_block"] = (145, 109, 85)
				
		self.map["snow_block"] = (225, 240, 240)
		self.map["snow"] = (225, 240, 240)
		self.map["ice"] = (171, 202, 253)
		self.map["packed_ice"] = (147, 174, 221)
		self.map["blue_ice"] = (114, 162, 247)
		
		self.map["terracotta"] = (150, 89, 63)
		self.map["orange_terracotta"] = (162, 81, 36)
		self.map["yellow_terracotta"] = (186, 132, 37)
		self.map["brown_terracotta"] = (77, 51, 37)
		self.map["white_terracotta"] = (210, 179, 162)
		self.map["light_gray_terracotta"] = (134, 106, 96)
		self.map["red_terracotta"] = (142, 62, 49)
		#self.map["terracotta"] = ()
		
		self.map["air"] = (0, 0, 0)
		self.map["cave_air"] = (50, 50, 50)
		self.map["cobweb"] = (200, 200, 200)
		self.map["beacon"] = (103, 214, 207)
		self.map["iron_block"] = (215, 215, 215)
		self.map["crafting_table"] = (78, 61, 39)
		self.map["chest"] = (78, 61, 39)
		self.map["ladder"] = (78, 61, 39)
		self.map["torch"] = (255, 217, 48)
		self.map["wall_torch"] = (255, 217, 48)

		woods = {
			"oak": (178, 142, 89),
			"spruce": (78, 59, 39),
			"birch": (212, 201, 139),
			"dark_oak": (50, 28, 8),
			"jungle": (113, 79, 52),
			"acacia": (166, 87, 44),
		}
		woodvars = ["_planks", "_slab", "_stairs", "_fence", "_fence_gate", "_door", "_trapdoor", "_button", "_pressure_plate"]
		stones = {
			"cobblestone": (80, 80, 80),
			"stone_brick": (80, 80, 80),
			"brick": (131, 73, 57),
			"sandstone": (255, 219, 166),
			"prismarine": (104, 172, 150),
			"prismarine_brick": (63, 124, 100),
			"dark_prismarine": (53, 79, 64),
			"nether_brick": (50, 27, 31)
		}
		stonevars = ["", "s", "_slab", "_stairs"]
		colors = {
			"white": (208, 213, 214),
			"orange": (226, 97, 26),
			"magenta": (169, 48, 159),
			"light_blue": (35, 136, 197),
			"yellow": (242, 176, 39),
			"lime": (94, 170, 30),
			"pink": (214, 100, 143),
			"gray": (54, 57, 61),
			"light_gray": (125, 125, 115),
			"cyan": (21, 118, 136),
			"purple": (99, 31, 155),
			"blue": (45, 47, 143),
			"brown": (97, 60, 32),
			"green": (72, 91, 36),
			"red": (141, 32, 32),
			"black": (9, 11, 15)
		}
		colorvars = ["_wool", "_carpet", "_concrete", "_concrete_powder", "_stained_glass", "_stained_glass_pane"]
		
		for t in woods:
			for v in woodvars:
				self.map[t + v] = woods[t]
		for t in stones:
			for v in stonevars:
				self.map[t + v] = stones[t]
		for t in colors:
			for v in colorvars:
				self.map[t + v] = colors[t]

		self.land = ["grass_block", "grass", "fern", "tall_grass", "large_fern", "dirt", "sand", "red_sand" "gravel", "podzol", "stone", "terracotta", "orange_terracotta"]
		self.water = ["water", "kelp", "kelp_plant", "bubble_column"]

		self.unknown = []


	def getColor(self, blockinfo):
		block = blockinfo['block']
		name = block['name'].replace("minecraft:", "")
		if name in self.land:
			if 'snowy' in block['properties'] and block['properties']['snowy'] == "true":
				return (250, 250, 250)
			color = self.map[name]
			if blockinfo['surface'] > 60:
				percent = (blockinfo['surface'] - 60) / float(100)
				if percent > .7:
					percent = .7
				return self.lighten(color, percent)
			return color
		elif name in self.water:
			color = self.map[name]
			if blockinfo['surface'] < 64 and 'depth' in blockinfo:
				depth = blockinfo['surface'] - blockinfo['depth']
				if depth > 0:
					percent = depth / float(80)
					if percent > .7:
						percent = 7
					return self.darken(color, percent)
			return color
		elif name in self.map:
			return self.map[name]
		else:
			if name not in self.unknown:
				print("  unknown: " + name)
			self.unknown.append(name)
			next = blockinfo['next']['name'].replace("minecraft:", "")
			if next in self.map:
				return self.map[next]
			else:
				return (50, 50, 50)

	def lighten(self, color, percent):
		r = color[0] + (255 - color[0]) * percent
		g = color[1] + (255 - color[1]) * percent
		b = color[2] + (255 - color[2]) * percent
		return (int(r), int(g), int(b))

	def darken(self, color, percent):
		r = color[0] - color[0] * percent
		g = color[1] - color[1] * percent
		b = color[2] - color[2] * percent
		return (int(r), int(g), int(b))

class Chunk:

	def __init__(self, region, x, z):
		self.chunk = region.get_chunk(x, z)['Level']			
		self.x = self.chunk['xPos'].value
		self.z = self.chunk['zPos'].value
		self.status = str(self.chunk['Status'].value)
		self.sections = [None] * 16
		self.heightmaps = {}
		if self.status != 'postprocessed':
			return
		for sec in self.chunk['Sections']:
			blockstates = sec['BlockStates']
			bits = len(blockstates) * 64 / 4096
			blocks = self.unpackBits(blockstates, bits)
			palette = self.processPalette(sec['Palette'])
			types = []
			for b in blocks:
				types.append(palette[b])
			self.sections[sec['Y'].value] = types

	def getColumnInfo(self, x, z):
		surface = self.getHeightMap(useHeightmap)
		y = surface[z * 16 + x]
		block = self.getBlock(x, y, z)
		while (block['name'] == "minecraft:air" or block['name'] == "minecraft:cave_air") and y > 2:
			y = y - 1
			block = self.getBlock(x, y, z)
		nextblock = self.getBlock(x, y - 1, z)
		ocean = self.getHeightMap('OCEAN_FLOOR')
		depth = ocean[z * 16 + x]
		return { "surface": y, "block": block, "next": nextblock, "depth": depth }

	def getHeightMap(self, type):
		if type in self.heightmaps:
			return self.heightmaps[type]
		data = self.chunk['Heightmaps'][type]
		heightmap = self.unpackBits(data, 9)
		self.heightmaps[type] = heightmap
		return heightmap

	def processPalette(self, p):
		palette = []
		for e in p:
			entry = {"name": str(e['Name'].value), "properties": {}}
			if 'Properties' in e:
				for prop in e['Properties']:
					entry['properties'][str(prop)] = str(e['Properties'][prop])
			palette.append(entry)
		return palette

	def getBlock(self, x, y, z):
		sec = y // 16
		y -= sec * 16
		if self.sections[sec] == None:
			return {"name": "minecraft:air", "properties": {}}
		return self.sections[sec][y * 256 + z * 16 + x]


	def unpackBits(self, list, size):
		bitmask = (2 ** size) - 1
		unpacked = []
		extrabits = 0
		extraval = 0
		for num in list:
			bits = 0
			if extrabits > 0:
				bits = size - extrabits
				tempmask = (2 ** bits) - 1
				val = num & tempmask
				val = val << extrabits
				val = val | extraval
				unpacked.append(val)
				num = num >> bits
			while bits < 64 - size:
				val = num & bitmask
				unpacked.append(val)
				bits += size
				num = num >> size
			extrabits = 64 - bits
			if extrabits > 0:
				extraval = num & ((2 ** extrabits) - 1)
		if extrabits > 0:
			unpacked.append(extraval)
		return unpacked

main()
