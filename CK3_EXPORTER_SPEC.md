Okay so the last step for this generator is to convert everything into a CK3 history file.

<character_id> = {	# Character ID is arbitrarily named -- I would just call it {dynasty_name}_character_{character_num} where character_num is literally what position they were generated at in the dynasty - required
	name 		# Character's given name - required
	dynasty 	# Character's surname - optional -> only required if character is part of the generated dynasty, do not add a dynasty variable if not apart of the dynasty (ie wives)
	religion	# Should prompt the user to enter this when they choose to export to CK3. Might not always have a "" around the string.
	culture		# Culture that the user picked in the wizard, lowercase. Might not always have a "" around the string - required
	father		# Pointer to father's <character_id> - optional
	mother		# Pointer to mother's <character_id> - optional
	
	# Events are added in a YYYY.MM.DD format, and preceding 0s do not exist
	# Births, deaths, and marriages are considered events
	YYYY.MM.DD = {		# Date of birth - required
		birth	        # required
		effect = { add_character_flag = do_not_generate_starting_family } 	# Do this for all male characters <30 (ie 'playable' characters).
	}
	YYYY.MM.DD = {		# Marriage date - optional
		add_spouse	 	# Pointer to the spouse's <character_id> - optional
						# Additional note: both spouses need to have a pointer to each other and they need to be married on the same date
	}
	YYYY.MM.DD = {		# Date of death - optional
		death			# This is inconsistent in the game files, but lets use 'yes'- optional
						# Just for the purposes of this generator, you should prompt the user to choose whether or not to add this field for living characters (at the time of generation). If the user selects 'yes', then put their death date a single day after the chosen start_date of the CK3 game (ie, the end_date for the generation).
	}
}


Some Examples pulled directly from the game files:
10011 = {
	name = "Robert"
	dynasty = 320
	religion = "catholic"
	culture = french
	father = 10026
	mother = 10027
	1035.1.1 = {
		birth = yes
	}
	1085.1.1 = {
		death = yes
	}
}
10026 = {
	name = "Renaud" #Renaud I de Nevers
	dynasty = 320 #Bauchaumont
	religion = "catholic"
	culture = french
	father = 40370 #Landry de Nevers
	mother = 277 #Mathilde de Bourgogne
	993.1.1 = {
		birth = "993.1.1"
	}
	1016.1.25 = {
		add_spouse = 10027 #Hedwige de France
	}
	1040.1.30 = {
		death = "1040.1.30"
	}
}
10027 = {
	name = "Hedwige" #Hedwige [Avoie] de France
	# AKA: Adelaide Havoise
	female = yes
	dynasty_house = house_capet
	religion = "catholic"
	culture = french
	father = 206 #Robert II de France
	mother = 333 #Constance d'Arles
	1003.1.1 = {
		birth = "1003.1.1"
	}
	#Renaud de Nevers
	1063.6.5 = {
		death = "1063.6.5"
	}
}
han_12068 = {
	name = "Zhen_8D1E"
	female = yes
	dynasty = wang_738B_273
	religion = "daoxue"
	culture = "han"
	father = han_11380
	1133.1.1 = { birth = yes }
	1149.1.1 = { add_spouse = han_11595 }
	1206.1.1 = { death = yes }
}
han_11595 = {
	name = "Hang_6C86"
	dynasty = song_5B8B_10
	religion = "daoxue"

	culture = "han"
	father = han_10769
	1121.1.1 = { birth = yes } # hypothetical
	1149.1.1 = { add_spouse = han_12068 }
	1178.1.1 = { death = yes } # hypothetical
}

han_9640 = {
	name = "Zhirou_81F3_67D4"
	female = yes
	dynasty = qiao_55AC_2
	religion = "daoxue"
	culture = "han"
	father = han_8359
	1064.1.1 = { birth = yes } # hypothetical
	1098.1.1 = { add_spouse = han_10298 }
	1140.1.1 = { death = yes } # hypothetical
}
125053 = {
	name = "Anna"
	female = yes
	religion = "orthodox"
	culture = "greek"
	1180.1.2 = {
		birth = "1180.1.2"
	}
	1220.1.2 = {
		death = "1220.1.2"
	}
}
# Character I made manually that works 100% in game
zhu_wentian_867 = {
	name = "Wéntiān"
	dynasty = afd_dynasty_zhu
	religion = "jingxue"
	culture = han
	840.11.23 = {
		birth = yes
		effect = {
			add_character_flag = do_not_generate_starting_family
		}
	}
	869.11.23 = {
		death = yes
	}
}