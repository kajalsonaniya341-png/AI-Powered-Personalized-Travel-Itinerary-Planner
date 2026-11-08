"""Compact source for the sample tourism dataset (all Indian states and union territories).

Each destination is (state_or_ut, city, [places]) and each place is
    (name, "categories separated by spaces", entry_cost_inr, visit_hours, latitude, longitude, description)

HONESTY RULES
- Costs (rough Indian-adult entry estimate, 0 = free/open access) and hours are ESTIMATES.
- Coordinates are APPROXIMATE (about 1 km) and left as None whenever I was not confident.
- Ratings are never included. Nothing is verified. Replace with verified data before real use.
Run `python -m scripts.build_dataset` to regenerate data/places.json from this file.
"""

N = None

DESTINATIONS = [
    # ------------------------------------------------------------------ Rajasthan
    ("Rajasthan", "Jaipur", [
        ("Amber Fort", "history culture architecture", 100, 2.5, 26.9855, 75.8513, "A historic hilltop fort known for its architecture and scenic surroundings."),
        ("City Palace", "history culture museums", 200, 2, 26.9258, 75.8237, "A royal palace complex with courtyards, galleries and museum collections in the old city."),
        ("Hawa Mahal", "history culture architecture", 50, 1, 26.9239, 75.8267, "A landmark palace facade with many small windows, best known as a photo stop in the old city."),
        ("Jantar Mantar", "history museums culture", 50, 1, 26.9247, 75.8246, "An open-air collection of large astronomical instruments built for observing the sky."),
        ("Jal Mahal", "nature culture", 0, 1, 26.9535, 75.8462, "A palace set in a lake, usually enjoyed as a scenic viewpoint from the lakeside."),
        ("Albert Hall Museum", "museums culture history", 40, 1.5, 26.9116, 75.8195, "A museum in a heritage building displaying art, artefacts and regional crafts."),
        ("Chokhi Dhani", "food culture shopping", 800, 3, N, N, "An ethnic village-style resort offering traditional food, folk performances and handicraft stalls."),
    ]),
    ("Rajasthan", "Udaipur", [
        ("City Palace Udaipur", "history culture museums", 300, 2, 24.5760, 73.6830, "A large palace complex above the lake with museum sections and city views."),
        ("Lake Pichola", "nature culture", 0, 1.5, 24.5720, 73.6790, "A scenic lake in the old city, often explored by boat."),
        ("Jagdish Temple", "religious architecture", 0, 1, 24.5800, 73.6840, "A prominent temple in the old city with detailed carved architecture."),
        ("Saheliyon ki Bari", "nature culture", 50, 1, 24.5980, 73.6870, "A landscaped garden with fountains and lotus pools."),
        ("Fateh Sagar Lake", "nature", 0, 1.5, 24.5980, 73.6720, "A popular lake for evening walks and sunset views."),
    ]),
    ("Rajasthan", "Jodhpur", [
        ("Mehrangarh Fort", "history culture architecture museums", 600, 3, 26.2980, 73.0180, "A massive hilltop fort with a museum and wide views over the city."),
        ("Jaswant Thada", "history architecture", 50, 1, 26.3010, 73.0190, "A marble memorial near the fort known for its white domes."),
        ("Umaid Bhawan Palace", "history architecture museums", 100, 1.5, 26.2810, 73.0480, "A large palace partly open to visitors, with a small museum."),
        ("Clock Tower and Sardar Market", "shopping food culture", 0, 2, 26.2950, 73.0230, "A busy old-city market for spices, textiles and local snacks."),
    ]),
    ("Rajasthan", "Jaisalmer", [
        ("Jaisalmer Fort", "history culture architecture", 0, 2.5, 26.9125, 70.9130, "A living fort in the desert city with shops, homes and temples inside."),
        ("Patwon Ki Haveli", "history architecture museums", 100, 1, 26.9150, 70.9120, "A cluster of ornate merchant mansions in the old city."),
        ("Sam Sand Dunes", "adventure nature", 0, 3, 26.8400, 70.5100, "Desert dunes known for camel rides and sunset views."),
        ("Gadisar Lake", "nature history", 0, 1, 26.9060, 70.9140, "A historic water tank surrounded by small temples and shrines."),
    ]),
    ("Rajasthan", "Pushkar", [
        ("Brahma Temple", "religious", 0, 1, 26.4890, 74.5530, "A well-known temple dedicated to Brahma."),
        ("Pushkar Lake", "religious nature", 0, 1.5, 26.4880, 74.5510, "A sacred lake surrounded by ghats and temples."),
        ("Savitri Mata Temple", "religious nature", 0, 2, 26.4870, 74.5600, "A hilltop temple reached by steps or ropeway with views over the town."),
        ("Pushkar Bazaar", "shopping food", 0, 2, N, N, "A busy market street for handicrafts, clothing and snacks."),
    ]),
    ("Rajasthan", "Ranthambore", [
        ("Ranthambore National Park", "wildlife nature adventure", 1500, 3.5, 26.0170, 76.5020, "A tiger reserve visited on guided jeep or canter safaris."),
        ("Ranthambore Fort", "history architecture", 0, 2, 26.0200, 76.4590, "An old hill fort inside the park area with ruins and viewpoints."),
        ("Padam Talao", "nature wildlife", 0, 1, N, N, "A lake inside the park where wildlife is often spotted."),
    ]),
    # ------------------------------------------------------------------ Delhi
    ("Delhi", "Delhi", [
        ("Red Fort", "history culture architecture", 35, 2, 28.6562, 77.2410, "A large Mughal-era fort complex in Old Delhi with palaces, halls and gardens."),
        ("India Gate", "history culture", 0, 1, 28.6129, 77.2295, "A war memorial arch surrounded by lawns, popular for evening walks."),
        ("National Museum", "museums history culture", 20, 2, 28.6117, 77.2194, "A large museum with collections covering art, archaeology and heritage across many periods."),
        ("Lotus Temple", "religious culture architecture", 0, 1, 28.5535, 77.2588, "A flower-shaped house of worship open to visitors of all backgrounds, set in landscaped grounds."),
        ("Chandni Chowk", "food shopping culture history", 0, 2.5, 28.6506, 77.2303, "A historic market street in Old Delhi known for street food, spices, textiles and busy lanes."),
        ("Qutub Minar", "history culture architecture", 35, 1.5, 28.5245, 77.1855, "A tall medieval minaret within an archaeological complex of ruins and monuments."),
    ]),
    # ------------------------------------------------------------------ Madhya Pradesh
    ("Madhya Pradesh", "Bhopal", [
        ("Upper Lake", "nature adventure culture", 0, 2, 23.2560, 77.3350, "A large lake at the heart of the city with lakeside promenades and boating options."),
        ("Van Vihar National Park", "wildlife nature", 50, 2.5, 23.2420, 77.3700, "A protected park beside the lake with native wildlife and forest walking areas."),
        ("Tribal Museum", "museums culture", 50, 2, N, N, "A museum presenting the art, living traditions and heritage of tribal communities of the region."),
        ("Taj-ul-Masajid", "religious history architecture", 0, 1, N, N, "One of the large mosques in India, notable for its grand scale and architecture."),
        ("Indira Gandhi Rashtriya Manav Sangrahalaya", "museums culture nature", 30, 2.5, N, N, "A national museum of humankind with indoor galleries and open-air exhibits on cultures and lifestyles."),
    ]),
    ("Madhya Pradesh", "Khajuraho", [
        ("Western Group of Temples", "history culture architecture religious", 40, 2.5, 24.8523, 79.9199, "A group of medieval temples known for detailed stone sculpture."),
        ("Lakshmana Temple", "history architecture religious", 0, 1, 24.8520, 79.9210, "A well-preserved temple within the temple complex area."),
        ("Khajuraho Archaeological Museum", "museums history", 10, 1, N, N, "A small museum with sculptures recovered from the region."),
        ("Raneh Falls", "nature", 50, 2, 24.9100, 80.0200, "A scenic gorge and waterfall area outside the town."),
    ]),
    ("Madhya Pradesh", "Ujjain", [
        ("Mahakaleshwar Temple", "religious culture", 0, 2, 23.1829, 75.7683, "A major Shiva temple and a key pilgrimage stop in the city."),
        ("Ram Ghat", "religious culture", 0, 1.5, 23.1810, 75.7680, "A river ghat on the Shipra where evening rituals are held."),
        ("Harsiddhi Temple", "religious", 0, 1, 23.1850, 75.7670, "A temple honoured as a Shakti shrine near the main temple area."),
        ("Kal Bhairav Temple", "religious", 0, 1, N, N, "A temple dedicated to Kal Bhairav, popular with pilgrims."),
    ]),
    ("Madhya Pradesh", "Indore", [
        ("Rajwada Palace", "history architecture", 0, 1, 22.7185, 75.8556, "A historic palace in the heart of the old city."),
        ("Lal Bagh Palace", "history museums architecture", 100, 1.5, 22.7020, 75.8510, "A grand palace with a museum area and gardens."),
        ("Sarafa Bazaar", "food shopping", 0, 2, 22.7180, 75.8550, "A night street-food market famous locally for snacks and sweets."),
        ("Khajrana Ganesh Temple", "religious", 0, 1, 22.7330, 75.9000, "A popular Ganesh temple visited by many locals."),
    ]),
    # ------------------------------------------------------------------ Maharashtra
    ("Maharashtra", "Mumbai", [
        ("Gateway of India", "history architecture culture", 0, 1, 18.9220, 72.8347, "A waterfront arch monument and a common starting point for exploring south Mumbai."),
        ("Marine Drive", "nature culture", 0, 1.5, 18.9440, 72.8230, "A curved seafront promenade, popular for evening walks."),
        ("Elephanta Caves", "history culture architecture", 40, 4, 18.9633, 72.9315, "Rock-cut cave temples on an island reached by ferry."),
        ("Chhatrapati Shivaji Terminus", "history architecture", 0, 1, 18.9398, 72.8355, "A grand railway station building known for its Victorian Gothic design."),
        ("Chhatrapati Shivaji Maharaj Vastu Sangrahalaya", "museums history culture", 100, 2, 18.9269, 72.8326, "A large museum of art, archaeology and natural history."),
        ("Siddhivinayak Temple", "religious", 0, 1, 19.0170, 72.8300, "A well-known Ganesh temple in central Mumbai."),
    ]),
    ("Maharashtra", "Pune", [
        ("Shaniwar Wada", "history architecture", 25, 1.5, 18.5195, 73.8553, "The remains of a historic fort-palace in the old city."),
        ("Aga Khan Palace", "history museums", 25, 1.5, 18.5530, 73.9020, "A palace with a memorial museum set in landscaped grounds."),
        ("Sinhagad Fort", "history adventure nature", 0, 3, 18.3660, 73.7550, "A hill fort popular for treks and views."),
        ("Dagdusheth Halwai Ganpati Temple", "religious", 0, 1, 18.5160, 73.8560, "A busy Ganesh temple in the city centre."),
    ]),
    ("Maharashtra", "Aurangabad", [
        ("Ajanta Caves", "history culture architecture museums", 40, 4, 20.5519, 75.7033, "Rock-cut cave monasteries known for ancient paintings and sculpture."),
        ("Ellora Caves", "history culture architecture religious", 40, 4, 20.0258, 75.1780, "A large complex of rock-cut temples and monasteries."),
        ("Bibi Ka Maqbara", "history architecture", 25, 1, 19.9010, 75.3200, "A Mughal-era tomb often compared to the Taj Mahal in style."),
        ("Daulatabad Fort", "history architecture adventure", 25, 2.5, 19.9440, 75.2130, "A hill fort with winding passages and steep climbs."),
    ]),
    ("Maharashtra", "Nashik", [
        ("Trimbakeshwar Temple", "religious culture", 0, 2, 19.9320, 73.5310, "An important Shiva temple near the source of the Godavari."),
        ("Panchavati", "religious culture", 0, 1.5, 20.0060, 73.7900, "A riverside area with temples and ghats."),
        ("Sula Vineyards", "food nature culture", 400, 2, 20.0100, 73.6880, "A vineyard that offers tours and tastings."),
        ("Pandavleni Caves", "history adventure", 20, 1.5, 19.9420, 73.7580, "Ancient rock-cut caves on a hill outside the city."),
    ]),
    # ------------------------------------------------------------------ Goa
    ("Goa", "Goa", [
        ("Basilica of Bom Jesus", "religious history architecture", 0, 1, 15.5009, 73.9116, "A historic church in Old Goa, part of a group of colonial-era monuments."),
        ("Se Cathedral", "religious history architecture", 0, 1, 15.5030, 73.9120, "A large cathedral close to the Basilica in Old Goa."),
        ("Fort Aguada", "history nature", 0, 1.5, 15.4920, 73.7730, "A coastal Portuguese-era fort with sea views."),
        ("Baga Beach", "nature adventure food", 0, 3, 15.5553, 73.7517, "A busy beach known for water sports, cafes and nightlife."),
        ("Dudhsagar Falls", "nature adventure", 400, 4, 15.3144, 74.3143, "A tall waterfall in the forest, reached by jeep in season."),
    ]),
    # ------------------------------------------------------------------ Kerala
    ("Kerala", "Kochi", [
        ("Chinese Fishing Nets", "culture nature", 0, 1, 9.9658, 76.2420, "Large shore-operated fishing nets along Fort Kochi's waterfront."),
        ("Mattancherry Palace", "history museums culture", 20, 1, 9.9580, 76.2590, "A palace museum with murals and artefacts."),
        ("Jew Town", "shopping culture history", 0, 1.5, 9.9570, 76.2590, "A lane of antique and spice shops near the synagogue."),
        ("Santa Cruz Basilica", "religious architecture", 0, 0.5, 9.9630, 76.2440, "A historic church in Fort Kochi."),
    ]),
    ("Kerala", "Munnar", [
        ("Eravikulam National Park", "wildlife nature", 300, 3, 10.1500, 77.0600, "A high-altitude park known for mountain landscapes and Nilgiri tahr."),
        ("Mattupetty Dam", "nature", 0, 1, 10.1070, 77.1230, "A reservoir with boating and scenic views."),
        ("Tea Museum", "museums culture", 125, 1, 10.0900, 77.0620, "A small museum about the tea plantation history of the region."),
        ("Top Station", "nature", 0, 1.5, 10.0970, 77.2350, "A hilltop viewpoint known for sweeping views of the valley."),
    ]),
    ("Kerala", "Alleppey", [
        ("Alleppey Backwaters", "nature culture adventure", 1500, 4, 9.4981, 76.3388, "A network of canals and lagoons, usually explored by houseboat or shikara."),
        ("Alappuzha Beach", "nature", 0, 1.5, 9.4890, 76.3250, "A calm beach with an old pier."),
        ("Marari Beach", "nature", 0, 2, 9.6080, 76.2960, "A quiet beach popular for relaxing."),
    ]),
    ("Kerala", "Thiruvananthapuram", [
        ("Padmanabhaswamy Temple", "religious history architecture", 0, 1.5, 8.4828, 76.9436, "A major temple with strict dress rules for visitors."),
        ("Kovalam Beach", "nature adventure", 0, 3, 8.3988, 76.9820, "A crescent-shaped beach popular for swimming and sunsets."),
        ("Napier Museum", "museums architecture", 20, 1, 8.5080, 76.9560, "A museum in a distinctive heritage building."),
        ("Poovar Island", "nature", 0, 3, N, N, "A backwater and beach area south of the city."),
    ]),
    # ------------------------------------------------------------------ Karnataka
    ("Karnataka", "Bengaluru", [
        ("Lalbagh Botanical Garden", "nature", 30, 2, 12.9507, 77.5848, "A large botanical garden with a glasshouse and old trees."),
        ("Cubbon Park", "nature", 0, 1.5, 12.9763, 77.5929, "A large central park popular for walks."),
        ("Bangalore Palace", "history architecture", 270, 1.5, 12.9988, 77.5921, "A palace with Tudor-style architecture and gardens."),
        ("Vidhana Soudha", "architecture history", 0, 0.5, 12.9797, 77.5907, "The state legislature building, usually viewed from outside."),
        ("Bull Temple", "religious culture", 0, 1, 12.9430, 77.5680, "A temple known for its large Nandi statue."),
    ]),
    ("Karnataka", "Mysuru", [
        ("Mysore Palace", "history architecture culture", 100, 2, 12.3052, 76.6552, "A grand royal palace, especially striking when lit up on special evenings."),
        ("Chamundi Hills", "religious nature", 0, 2, 12.2724, 76.6700, "A hilltop temple area with views over the city."),
        ("Brindavan Gardens", "nature", 50, 1.5, 12.4220, 76.5720, "Terraced gardens below the KRS dam."),
        ("St. Philomena's Church", "religious architecture", 0, 0.5, 12.3150, 76.6540, "A large neo-Gothic church in the city."),
        ("Mysore Zoo", "wildlife nature", 100, 3, 12.3010, 76.6520, "One of the older zoos in India with a wide range of species."),
    ]),
    ("Karnataka", "Hampi", [
        ("Virupaksha Temple", "religious history architecture", 0, 1.5, 15.3350, 76.4600, "A living temple at the heart of the Vijayanagara ruins."),
        ("Vittala Temple", "history architecture", 40, 2, 15.3430, 76.4750, "A temple complex famous for the stone chariot and carved pillars."),
        ("Lotus Mahal", "history architecture", 40, 1, 15.3300, 76.4670, "A palace-era pavilion in the royal enclosure."),
        ("Hampi Bazaar", "shopping culture history", 0, 1.5, 15.3350, 76.4610, "A long street of ruins and shops facing the main temple."),
        ("Matanga Hill", "adventure nature", 0, 1.5, N, N, "A hill climb popular for sunrise views over the ruins."),
    ]),
    ("Karnataka", "Coorg", [
        ("Abbey Falls", "nature", 50, 1, 12.4570, 75.7330, "A waterfall surrounded by coffee estates."),
        ("Raja's Seat", "nature", 20, 1, 12.4200, 75.7370, "A garden viewpoint known for sunsets over the valley."),
        ("Namdroling Monastery", "religious culture", 0, 1.5, 12.4880, 75.9660, "A large Tibetan Buddhist monastery at Bylakuppe."),
        ("Dubare Elephant Camp", "wildlife nature", 100, 2, N, N, "A riverside elephant camp offering short visits."),
    ]),
    # ------------------------------------------------------------------ Tamil Nadu
    ("Tamil Nadu", "Chennai", [
        ("Marina Beach", "nature culture", 0, 1.5, 13.0500, 80.2824, "One of the longest urban beaches, busy in the evenings."),
        ("Kapaleeshwarar Temple", "religious architecture", 0, 1, 13.0340, 80.2700, "A Dravidian-style temple in Mylapore."),
        ("Fort St. George", "history museums", 25, 1.5, 13.0790, 80.2870, "A colonial-era fort that now houses a museum."),
        ("Government Museum Chennai", "museums history", 50, 2, 13.0700, 80.2570, "A large museum with art, archaeology and natural history sections."),
        ("San Thome Basilica", "religious architecture", 0, 1, 13.0330, 80.2780, "A neo-Gothic church near the beach."),
    ]),
    ("Tamil Nadu", "Madurai", [
        ("Meenakshi Amman Temple", "religious architecture culture", 0, 2, 9.9195, 78.1193, "A major temple complex with tall, brightly painted gateway towers."),
        ("Thirumalai Nayakkar Mahal", "history architecture", 50, 1, 9.9150, 78.1260, "A palace remnant with large pillared halls."),
        ("Gandhi Memorial Museum", "museums history", 0, 1.5, 9.9400, 78.1450, "A museum about the freedom movement in a historic palace."),
        ("Alagar Kovil", "religious nature", 0, 1.5, 10.0770, 78.2060, "A hillside temple outside the city."),
    ]),
    ("Tamil Nadu", "Mahabalipuram", [
        ("Shore Temple", "history architecture religious", 40, 1.5, 12.6165, 80.1990, "A stone temple on the waterfront."),
        ("Five Rathas", "history architecture", 40, 1, 12.6070, 80.2020, "Monolithic rock-cut shrines carved in the shape of chariots."),
        ("Arjuna's Penance", "history culture", 0, 0.5, 12.6170, 80.1920, "A huge open-air rock relief."),
        ("Krishna's Butter Ball", "history nature", 0, 0.5, 12.6160, 80.1930, "A massive balanced boulder on a hillside."),
    ]),
    ("Tamil Nadu", "Thanjavur", [
        ("Brihadisvara Temple", "religious history architecture", 0, 2, 10.7828, 79.1318, "A large Chola-era temple with a very tall tower."),
        ("Thanjavur Maratha Palace", "history museums architecture", 50, 1.5, 10.7870, 79.1350, "A palace complex with galleries."),
        ("Saraswathi Mahal Library", "museums history", 10, 1, N, N, "A historic library with old manuscripts."),
    ]),
    ("Tamil Nadu", "Ooty", [
        ("Government Botanical Garden", "nature", 50, 2, 11.4190, 76.7120, "A terraced garden with many plant collections."),
        ("Ooty Lake", "nature adventure", 20, 1.5, 11.4020, 76.6870, "A lake with boating and walking paths."),
        ("Doddabetta Peak", "nature", 10, 1.5, 11.4000, 76.7360, "The highest point in the Nilgiris with wide viewpoints."),
        ("Nilgiri Mountain Railway", "culture adventure", 50, 3, 11.4120, 76.6950, "A heritage mountain railway through tea country."),
    ]),
    ("Tamil Nadu", "Rameswaram", [
        ("Ramanathaswamy Temple", "religious architecture", 0, 2, 9.2880, 79.3170, "A major temple known for its long pillared corridors."),
        ("Dhanushkodi", "nature history", 0, 2, 9.1800, 79.4300, "A sandy tip of land with ruins, reached by road."),
        ("Pamban Bridge", "history nature", 0, 1, 9.2830, 79.2000, "A sea bridge connecting the island to the mainland."),
        ("Dr. APJ Abdul Kalam Memorial", "museums history", 0, 1, 9.2780, 79.3560, "A memorial with exhibits about the former president."),
    ]),
    # ------------------------------------------------------------------ Telangana / Andhra Pradesh
    ("Telangana", "Hyderabad", [
        ("Charminar", "history architecture shopping", 25, 1, 17.3616, 78.4747, "A landmark monument with a busy bazaar around it."),
        ("Golconda Fort", "history architecture", 25, 2.5, 17.3833, 78.4011, "A large hill fort with acoustic features and views."),
        ("Hussain Sagar Lake", "nature culture", 0, 1.5, 17.4239, 78.4738, "A large central lake with a Buddha statue."),
        ("Ramoji Film City", "culture adventure", 1500, 6, 17.2543, 78.6808, "A large film studio complex with themed tours."),
        ("Salar Jung Museum", "museums culture history", 20, 2.5, 17.3713, 78.4804, "A major museum with a large private art collection."),
        ("Chowmahalla Palace", "history architecture museums", 80, 1.5, 17.3578, 78.4717, "A restored palace complex of the Nizams."),
    ]),
    ("Andhra Pradesh", "Visakhapatnam", [
        ("RK Beach", "nature culture", 0, 1.5, 17.7143, 83.3230, "A city beach popular for evening walks."),
        ("Kailasagiri", "nature culture", 20, 2, 17.7490, 83.3420, "A hilltop park with sea views."),
        ("Borra Caves", "nature adventure", 80, 2, 18.2800, 82.8800, "Limestone caves with stalactites near Araku."),
        ("Araku Valley", "nature culture", 0, 4, 18.3273, 82.8775, "A hill valley region known for coffee plantations."),
        ("INS Kursura Submarine Museum", "museums history", 50, 1, 17.7140, 83.3280, "A decommissioned submarine open to visitors."),
    ]),
    ("Andhra Pradesh", "Tirupati", [
        ("Tirumala Venkateswara Temple", "religious culture", 0, 4, 13.6833, 79.3472, "One of the most visited temples in the world; queues can be long."),
        ("Sri Padmavathi Temple", "religious", 0, 1.5, 13.6049, 79.4190, "A temple at Tiruchanur dedicated to the goddess Padmavathi."),
        ("Chandragiri Fort", "history museums", 10, 1.5, 13.5860, 79.3190, "A historic hill fort with a small museum."),
        ("Silathoranam", "nature history", 0, 0.5, N, N, "A natural rock arch near the temple area."),
    ]),
    # ------------------------------------------------------------------ Uttar Pradesh
    ("Uttar Pradesh", "Agra", [
        ("Taj Mahal", "history culture architecture", 50, 3, 27.1751, 78.0421, "A white-marble mausoleum and one of the best-known monuments in the world."),
        ("Agra Fort", "history architecture", 50, 2, 27.1795, 78.0211, "A large red-sandstone fort with palaces and halls."),
        ("Fatehpur Sikri", "history architecture", 50, 3, 27.0940, 77.6610, "A well-preserved abandoned Mughal capital city."),
        ("Mehtab Bagh", "nature history", 30, 1, 27.1830, 78.0430, "A garden across the river with a classic Taj view."),
        ("Itimad-ud-Daulah", "history architecture", 30, 1, 27.1930, 78.0300, "A finely decorated tomb on the riverbank."),
    ]),
    ("Uttar Pradesh", "Varanasi", [
        ("Kashi Vishwanath Temple", "religious culture", 0, 2, 25.3109, 83.0107, "A major Shiva temple in the old city."),
        ("Dashashwamedh Ghat", "religious culture", 0, 2, 25.3070, 83.0104, "The main ghat, known for the evening Ganga aarti."),
        ("Sarnath", "history religious museums", 25, 3, 25.3810, 83.0230, "A Buddhist site with ruins, a stupa and a museum."),
        ("Assi Ghat", "culture religious", 0, 1.5, 25.2890, 83.0060, "A popular ghat for morning rituals and music."),
        ("Ramnagar Fort", "history museums", 50, 1.5, 25.2690, 83.0230, "A riverside fort with a small museum."),
    ]),
    ("Uttar Pradesh", "Lucknow", [
        ("Bara Imambara", "history architecture", 50, 2, 26.8690, 80.9120, "A large 18th-century complex known for its vast hall and maze."),
        ("Rumi Darwaza", "history architecture", 0, 0.5, 26.8700, 80.9100, "A tall ornate gateway near the Imambara."),
        ("Chota Imambara", "history architecture religious", 20, 1, 26.8730, 80.9050, "An ornate shrine and hall."),
        ("British Residency", "history", 25, 1.5, 26.8610, 80.9220, "Ruins from the 1857 uprising."),
        ("Hazratganj", "shopping food", 0, 2, 26.8500, 80.9400, "A central shopping and dining district."),
    ]),
    ("Uttar Pradesh", "Ayodhya", [
        ("Ram Janmabhoomi Temple", "religious culture", 0, 2, 26.7956, 82.1940, "A major temple complex; visitor rules and timings change often."),
        ("Hanuman Garhi", "religious", 0, 1, 26.8000, 82.2030, "A hilltop temple reached by a flight of steps."),
        ("Kanak Bhawan", "religious architecture", 0, 1, 26.7980, 82.1980, "A decorated temple in the town."),
        ("Saryu Ghat", "religious nature", 0, 1.5, 26.8030, 82.2050, "River ghats where evening aarti is held."),
    ]),
    ("Uttar Pradesh", "Prayagraj", [
        ("Triveni Sangam", "religious nature culture", 0, 2, 25.4260, 81.8860, "The meeting point of the Ganga and Yamuna rivers, reached by boat."),
        ("Anand Bhawan", "history museums", 20, 1.5, 25.4560, 81.8490, "A historic family home turned museum."),
        ("Allahabad Fort", "history architecture", 0, 1, 25.4290, 81.8730, "A riverside fort, partly open to visitors."),
        ("Khusro Bagh", "history nature", 0, 1, 25.4430, 81.8190, "A walled garden with Mughal-era tombs."),
    ]),
    ("Uttar Pradesh", "Mathura", [
        ("Shri Krishna Janmasthan", "religious culture", 0, 1.5, 27.5040, 77.6700, "A temple complex at the traditional birthplace of Krishna."),
        ("Banke Bihari Temple", "religious culture", 0, 1.5, 27.5810, 77.6970, "A busy temple in Vrindavan."),
        ("Prem Mandir", "religious architecture", 0, 1.5, 27.5640, 77.6710, "A modern marble temple with evening light shows."),
        ("Vishram Ghat", "religious nature", 0, 1, 27.5030, 77.6890, "A river ghat on the Yamuna with daily aarti."),
    ]),
    # ------------------------------------------------------------------ Uttarakhand
    ("Uttarakhand", "Rishikesh", [
        ("Laxman Jhula", "culture religious", 0, 1, 30.1260, 78.3280, "A pedestrian suspension bridge over the Ganga."),
        ("Triveni Ghat", "religious culture", 0, 1.5, 30.1000, 78.2960, "The main ghat for the evening Ganga aarti."),
        ("Beatles Ashram", "history culture", 150, 1.5, 30.1030, 78.3010, "A ruined ashram complex with colourful murals, in forest."),
        ("River Rafting at Shivpuri", "adventure nature", 600, 3, N, N, "Seasonal white-water rafting on the Ganga with licensed operators."),
    ]),
    ("Uttarakhand", "Haridwar", [
        ("Har Ki Pauri", "religious culture", 0, 2, 29.9570, 78.1700, "The best-known ghat, famous for the evening Ganga aarti."),
        ("Mansa Devi Temple", "religious nature", 0, 1.5, 29.9600, 78.1680, "A hilltop temple reached by ropeway or on foot."),
        ("Chandi Devi Temple", "religious nature", 0, 1.5, 29.9660, 78.1850, "A hilltop temple with ropeway access."),
        ("Rajaji National Park", "wildlife nature", 800, 3, N, N, "A forest reserve nearby known for elephants and birds."),
    ]),
    ("Uttarakhand", "Nainital", [
        ("Naini Lake", "nature adventure", 0, 2, 29.3910, 79.4560, "A central lake with boating."),
        ("Naina Devi Temple", "religious", 0, 1, 29.3920, 79.4570, "A temple on the lakeshore."),
        ("Snow View Point", "nature", 0, 1.5, 29.3980, 79.4580, "A viewpoint with ropeway access."),
        ("Tiffin Top", "nature adventure", 0, 2, N, N, "A short hike to a viewpoint above the town."),
    ]),
    ("Uttarakhand", "Mussoorie", [
        ("Kempty Falls", "nature", 20, 1.5, 30.4430, 78.0330, "A popular waterfall on the road to Chakrata."),
        ("Gun Hill", "nature", 30, 1, 30.4590, 78.0660, "A hill with ropeway access and mountain views."),
        ("Mall Road", "shopping food", 0, 2, 30.4580, 78.0690, "The main promenade for shopping and snacks."),
        ("Lal Tibba", "nature", 0, 1, 30.4580, 78.0540, "A high viewpoint known for Himalayan views on clear days."),
    ]),
    ("Uttarakhand", "Jim Corbett", [
        ("Jim Corbett National Park", "wildlife nature adventure", 1500, 4, 29.5300, 78.7747, "A famous tiger reserve visited on safaris."),
        ("Corbett Falls", "nature", 50, 1, N, N, "A small waterfall in the Corbett area."),
        ("Garjiya Devi Temple", "religious nature", 0, 1, N, N, "A temple on a large rock in the Kosi river."),
    ]),
    # ------------------------------------------------------------------ Himachal Pradesh
    ("Himachal Pradesh", "Shimla", [
        ("The Ridge", "culture nature", 0, 1.5, 31.1048, 77.1734, "An open promenade at the centre of the town with mountain views."),
        ("Christ Church", "religious architecture history", 0, 0.5, 31.1050, 77.1730, "A colonial-era church on the Ridge."),
        ("Jakhu Temple", "religious nature", 0, 1.5, 31.1002, 77.1850, "A hilltop Hanuman temple with city views."),
        ("Kufri", "nature adventure", 50, 3, 31.0980, 77.2650, "A hill resort for walks, snow in winter, and viewpoints."),
        ("Mall Road Shimla", "shopping food", 0, 2, 31.1040, 77.1700, "A pedestrian shopping street."),
    ]),
    ("Himachal Pradesh", "Manali", [
        ("Hadimba Temple", "religious culture", 0, 1, 32.2480, 77.1800, "A wooden temple set in a cedar forest."),
        ("Solang Valley", "adventure nature", 500, 3, 32.3170, 77.1580, "A valley known for snow activities and paragliding in season."),
        ("Rohtang Pass", "adventure nature", 550, 5, 32.3720, 77.2460, "A high mountain pass; access needs a permit and is seasonal."),
        ("Old Manali", "culture food shopping", 0, 2, 32.2560, 77.1810, "A cafe-lined village area with local shops."),
        ("Jogini Falls", "nature adventure", 0, 2, N, N, "A waterfall reached by a short trek."),
    ]),
    ("Himachal Pradesh", "Dharamshala", [
        ("Tsuglagkhang Complex", "religious culture museums", 0, 2, 32.2260, 76.3210, "The main Tibetan temple complex with a small museum, in McLeod Ganj."),
        ("Bhagsu Waterfall", "nature", 0, 1.5, 32.2450, 76.3430, "A waterfall reached by a short walk from Bhagsu village."),
        ("Triund Trek", "adventure nature", 0, 5, N, N, "A popular day trek with views of the Dhauladhar range."),
        ("Kangra Fort", "history architecture", 40, 2, 32.0900, 76.2600, "One of the oldest forts in the region."),
    ]),
    # ------------------------------------------------------------------ Jammu & Kashmir
    ("Jammu and Kashmir", "Srinagar", [
        ("Dal Lake", "nature culture", 0, 3, 34.1100, 74.8700, "A large lake known for shikara rides and houseboats."),
        ("Shalimar Bagh", "history nature architecture", 30, 1.5, 34.1430, 74.8740, "A terraced Mughal garden."),
        ("Nishat Bagh", "history nature", 30, 1.5, 34.1100, 74.8680, "A Mughal garden overlooking the lake."),
        ("Hazratbal Shrine", "religious architecture", 0, 1, 34.1280, 74.8420, "A major shrine on the lake shore."),
        ("Shankaracharya Temple", "religious nature", 0, 1.5, 34.0770, 74.8360, "A hilltop temple with city views."),
    ]),
    ("Jammu and Kashmir", "Gulmarg", [
        ("Gulmarg Gondola", "adventure nature", 900, 3, 34.0480, 74.3870, "A cable car to high viewpoints and ski slopes."),
        ("Alpather Lake", "nature adventure", 0, 5, N, N, "A high-altitude lake, often frozen until early summer."),
        ("Strawberry Valley", "nature", 0, 1.5, N, N, "A meadow area in the Gulmarg region."),
    ]),
    ("Jammu and Kashmir", "Pahalgam", [
        ("Betaab Valley", "nature", 50, 2, N, N, "A scenic valley with meadows and river views."),
        ("Aru Valley", "nature adventure", 0, 3, N, N, "A quiet valley and trek starting point."),
        ("Lidder River", "nature adventure", 0, 2, N, N, "A river running through the town, good for walks."),
    ]),
    ("Jammu and Kashmir", "Jammu", [
        ("Raghunath Temple", "religious architecture", 0, 1, 32.7280, 74.8570, "A large temple complex in the city centre."),
        ("Bahu Fort", "history nature", 0, 1.5, 32.7150, 74.8650, "A hilltop fort with a temple and gardens."),
        ("Vaishno Devi Temple (Katra)", "religious adventure", 0, 8, 33.0300, 74.9490, "A major pilgrimage reached by a long uphill route from Katra."),
        ("Amar Mahal Museum", "museums history", 50, 1.5, N, N, "A palace turned museum."),
    ]),
    ("Ladakh", "Leh", [
        ("Leh Palace", "history architecture", 15, 1.5, 34.1650, 77.5850, "A ruined palace overlooking the town."),
        ("Shanti Stupa", "religious nature", 0, 1, 34.1680, 77.5700, "A white-domed stupa with sunset views."),
        ("Pangong Tso", "nature adventure", 0, 8, 33.7500, 78.6500, "A high-altitude lake; needs a permit and acclimatisation."),
        ("Nubra Valley", "nature adventure culture", 0, 8, 34.6000, 77.5600, "A valley with dunes and monasteries, reached via a high pass; permit needed."),
        ("Thiksey Monastery", "religious architecture culture", 50, 1.5, 34.0480, 77.6700, "A large hilltop monastery."),
        ("Magnetic Hill", "nature", 0, 0.5, 34.1900, 77.4400, "A roadside spot known for an optical illusion."),
    ]),
    # ------------------------------------------------------------------ Punjab / Haryana / Chandigarh
    ("Punjab", "Amritsar", [
        ("Golden Temple", "religious culture architecture food", 0, 3, 31.6200, 74.8765, "The holiest Sikh shrine, with a free community kitchen."),
        ("Jallianwala Bagh", "history museums", 0, 1, 31.6206, 74.8800, "A memorial garden to the 1919 massacre."),
        ("Wagah Border Ceremony", "culture history", 0, 3, 31.6040, 74.5730, "A daily flag-lowering ceremony at the India-Pakistan border."),
        ("Partition Museum", "museums history", 10, 1.5, 31.6240, 74.8780, "A museum about the 1947 Partition."),
        ("Durgiana Temple", "religious architecture", 0, 1, N, N, "A temple set in a pool, similar in layout to the Golden Temple."),
    ]),
    ("Haryana", "Kurukshetra", [
        ("Brahma Sarovar", "religious nature culture", 0, 1.5, 29.9606, 76.8400, "A large sacred tank, busy at festival times."),
        ("Jyotisar", "religious history", 0, 1, N, N, "A site linked to the Bhagavad Gita, with a banyan tree and temple."),
        ("Sheikh Chilli's Tomb", "history architecture", 10, 1, N, N, "A historic tomb complex."),
        ("Kurukshetra Panorama and Science Centre", "museums history", 50, 1.5, N, N, "A museum with a panorama about the Mahabharata."),
    ]),
    ("Chandigarh", "Chandigarh", [
        ("Rock Garden", "culture museums nature", 30, 2, 30.7525, 76.8101, "A sculpture garden built from waste and found objects."),
        ("Sukhna Lake", "nature", 0, 1.5, 30.7421, 76.8188, "A man-made lake used for boating and walks."),
        ("Zakir Hussain Rose Garden", "nature", 0, 1.5, 30.7460, 76.7830, "One of the largest rose gardens in Asia."),
        ("Capitol Complex", "architecture history", 0, 1.5, 30.7580, 76.8020, "Government buildings designed by Le Corbusier; visit by arrangement."),
    ]),
    # ------------------------------------------------------------------ Gujarat
    ("Gujarat", "Ahmedabad", [
        ("Sabarmati Ashram", "history museums", 0, 1.5, 23.0607, 72.5802, "Gandhi's former residence and a museum on the riverbank."),
        ("Adalaj Stepwell", "history architecture", 0, 1, 23.1670, 72.5810, "An intricately carved stepwell."),
        ("Sidi Saiyyed Mosque", "history architecture religious", 0, 0.5, 23.0270, 72.5810, "A mosque famous for its stone lattice windows."),
        ("Kankaria Lake", "nature culture", 20, 2, 23.0070, 72.6030, "A lakefront with attractions and walking areas."),
    ]),
    ("Gujarat", "Kevadia", [
        ("Statue of Unity", "history culture architecture", 380, 3, 21.8380, 73.7191, "One of the tallest statues in the world, with a viewing gallery."),
        ("Sardar Sarovar Dam", "nature architecture", 0, 1, 21.8300, 73.7480, "A large dam with viewpoints."),
        ("Shoolpaneshwar Wildlife Sanctuary", "wildlife nature", 100, 3, N, N, "A forest sanctuary nearby."),
    ]),
    ("Gujarat", "Dwarka", [
        ("Dwarkadhish Temple", "religious architecture", 0, 1.5, 22.2375, 68.9677, "A major Krishna temple."),
        ("Bet Dwarka", "religious nature", 0, 3, 22.4750, 69.0830, "An island reached by boat, with temples."),
        ("Nageshwar Jyotirlinga", "religious", 0, 1, 22.3380, 69.0780, "A Shiva temple on the road to Bet Dwarka."),
        ("Rukmini Devi Temple", "religious", 0, 1, N, N, "A temple dedicated to Rukmini near the town."),
    ]),
    ("Dadra and Nagar Haveli and Daman and Diu", "Diu", [
        ("Diu Fort", "history architecture", 0, 1.5, 20.7120, 70.9910, "A large coastal Portuguese fort."),
        ("Nagoa Beach", "nature", 0, 2, 20.7000, 70.9300, "A horseshoe-shaped beach."),
        ("St. Paul's Church", "religious architecture", 0, 0.5, 20.7110, 70.9860, "A baroque-style church."),
        ("Naida Caves", "history nature", 0, 1, 20.7130, 70.9860, "Old quarried caves with light shafts."),
    ]),
    # ------------------------------------------------------------------ East & North-East
    ("West Bengal", "Kolkata", [
        ("Victoria Memorial", "history museums architecture", 30, 2, 22.5448, 88.3426, "A marble memorial building and museum."),
        ("Howrah Bridge", "culture architecture", 0, 0.5, 22.5851, 88.3468, "A busy cantilever bridge over the Hooghly."),
        ("Dakshineswar Kali Temple", "religious", 0, 1.5, 22.6550, 88.3570, "A major riverside temple."),
        ("Indian Museum", "museums history", 50, 2, 22.5580, 88.3510, "One of the oldest and largest museums in the country."),
        ("Park Street", "food shopping", 0, 2, 22.5530, 88.3540, "A dining and nightlife street."),
        ("College Street Book Market", "shopping culture", 0, 1.5, 22.5750, 88.3640, "A long row of second-hand and new book stalls."),
    ]),
    ("West Bengal", "Darjeeling", [
        ("Tiger Hill", "nature", 50, 2, 26.9870, 88.2790, "A sunrise viewpoint for mountain views."),
        ("Batasia Loop", "nature history", 50, 1, 27.0170, 88.2480, "A railway loop with a war memorial and gardens."),
        ("Darjeeling Himalayan Railway", "culture adventure", 1500, 2, 27.0410, 88.2630, "A heritage narrow-gauge steam railway."),
        ("Peace Pagoda", "religious nature", 0, 1, 27.0030, 88.2640, "A white stupa with hill views."),
        ("Himalayan Mountaineering Institute", "museums adventure", 100, 1.5, N, N, "A mountaineering institute with a museum."),
    ]),
    ("West Bengal", "Sundarbans", [
        ("Sundarbans National Park", "wildlife nature adventure", 1000, 8, N, N, "A mangrove delta explored by boat; known for tigers and birds."),
        ("Sajnekhali Watch Tower", "wildlife nature", 0, 1, N, N, "A viewing tower with a small museum."),
    ]),
    ("Odisha", "Puri", [
        ("Jagannath Temple", "religious culture architecture", 0, 2, 19.8048, 85.8180, "A major temple; entry rules apply."),
        ("Puri Beach", "nature culture", 0, 2, 19.7980, 85.8260, "A wide beach near the town."),
        ("Chilika Lake", "nature wildlife adventure", 1500, 5, 19.7200, 85.3200, "A large brackish lagoon known for birds and boat trips."),
        ("Raghurajpur Heritage Village", "culture shopping", 0, 2, N, N, "A village of artisans known for palm-leaf and cloth paintings."),
    ]),
    ("Odisha", "Bhubaneswar", [
        ("Lingaraj Temple", "religious architecture", 0, 1, 20.2380, 85.8338, "A large medieval temple; non-Hindu entry is restricted."),
        ("Udayagiri and Khandagiri Caves", "history architecture", 25, 2, 20.2630, 85.7850, "Ancient rock-cut caves on twin hills."),
        ("Odisha State Museum", "museums history", 10, 1.5, 20.2530, 85.8420, "A museum of regional art and archaeology."),
        ("Nandankanan Zoological Park", "wildlife nature", 50, 3, 20.3980, 85.8190, "A zoo and botanical garden."),
        ("Dhauli Shanti Stupa", "religious history", 0, 1, 20.1920, 85.8380, "A peace stupa on a hill near ancient rock edicts."),
    ]),
    ("Odisha", "Konark", [
        ("Konark Sun Temple", "history architecture religious", 40, 2, 19.8876, 86.0945, "A chariot-shaped temple of intricate stonework."),
        ("Chandrabhaga Beach", "nature", 0, 1.5, 19.8860, 86.1260, "A beach near Konark, popular at sunrise."),
        ("Konark Archaeological Museum", "museums history", 10, 1, N, N, "A museum of sculptures recovered from the temple."),
    ]),
    ("Bihar", "Bodh Gaya", [
        ("Mahabodhi Temple", "religious history architecture", 0, 2, 24.6961, 84.9913, "The temple complex linked to the Buddha's enlightenment."),
        ("Great Buddha Statue", "religious", 0, 0.5, 24.6990, 84.9890, "A very large seated Buddha statue."),
        ("Dungeshwari Cave Temples", "religious history", 0, 1.5, N, N, "Caves where the Buddha is said to have meditated."),
        ("Bodh Gaya Archaeological Museum", "museums history", 5, 1, N, N, "A small local museum."),
    ]),
    ("Bihar", "Patna", [
        ("Golghar", "history architecture", 10, 1, 25.6170, 85.1450, "A large beehive-shaped granary with city views."),
        ("Patna Museum", "museums history", 20, 2, 25.6100, 85.1360, "A museum with art and archaeology."),
        ("Takht Sri Patna Sahib", "religious", 0, 1, 25.6190, 85.2020, "A major Sikh shrine."),
        ("Mahavir Mandir", "religious", 0, 0.5, 25.6010, 85.1380, "A busy temple near the railway station."),
    ]),
    ("Jharkhand", "Ranchi", [
        ("Hundru Falls", "nature adventure", 0, 2, N, N, "A waterfall outside the city, best seen after monsoon."),
        ("Jagannath Temple Ranchi", "religious architecture", 0, 1, N, N, "A hilltop temple."),
        ("Tagore Hill", "nature history", 0, 1, N, N, "A hill with a memorial and city views."),
        ("Rock Garden Ranchi", "nature culture", 20, 1, N, N, "A landscaped park with carved rock features."),
    ]),
    ("Chhattisgarh", "Raipur", [
        ("Mahant Ghasidas Memorial Museum", "museums history culture", 10, 1.5, 21.2370, 81.6330, "A regional museum of art and tribal culture."),
        ("Nandan Van Zoo and Safari", "wildlife nature", 50, 3, N, N, "A zoo and safari park near the city."),
        ("Purkhauti Muktangan", "museums culture", 20, 1.5, N, N, "An open-air museum on tribal heritage."),
        ("Vivekananda Sarovar", "nature", 0, 1, N, N, "A lake with a statue and walkways."),
    ]),
    ("Sikkim", "Gangtok", [
        ("Rumtek Monastery", "religious culture architecture", 0, 1.5, 27.2890, 88.5640, "A large monastery outside the city."),
        ("MG Marg", "shopping food culture", 0, 2, 27.3290, 88.6130, "A pedestrian promenade for shopping and cafes."),
        ("Tsomgo Lake", "nature adventure", 0, 4, 27.3740, 88.7640, "A high-altitude lake; permit required for the trip."),
        ("Enchey Monastery", "religious", 0, 1, 27.3380, 88.6190, "A small monastery above the city."),
        ("Hanuman Tok", "religious nature", 0, 1, 27.3360, 88.6350, "A hilltop temple with views."),
    ]),
    ("Assam", "Guwahati", [
        ("Kamakhya Temple", "religious architecture", 0, 2, 26.1664, 91.7059, "A major Shakti temple on Nilachal Hill."),
        ("Umananda Temple", "religious nature", 10, 1.5, 26.1960, 91.7440, "A small temple on a river island."),
        ("Assam State Museum", "museums culture", 10, 1.5, 26.1850, 91.7470, "A museum on regional heritage."),
        ("Pobitora Wildlife Sanctuary", "wildlife nature", 300, 3, N, N, "A sanctuary known for one-horned rhinos."),
    ]),
    ("Assam", "Kaziranga", [
        ("Kaziranga National Park", "wildlife nature adventure", 1000, 4, 26.5775, 93.1711, "A park known for one-horned rhinos, visited on jeep and elephant safaris."),
        ("Kakochang Waterfalls", "nature", 20, 1.5, N, N, "A forest waterfall near the park."),
    ]),
    ("Arunachal Pradesh", "Tawang", [
        ("Tawang Monastery", "religious culture architecture", 0, 1.5, 27.5861, 91.8594, "A large monastery with mountain views."),
        ("Sela Pass", "nature adventure", 0, 1, 27.5014, 92.1050, "A high mountain pass; road conditions are seasonal."),
        ("Nuranang Waterfall", "nature", 0, 1, N, N, "A tall waterfall on the way to Tawang."),
        ("Tawang War Memorial", "history", 0, 1, N, N, "A memorial to soldiers of the 1962 war."),
    ]),
    ("Meghalaya", "Shillong", [
        ("Umiam Lake", "nature adventure", 0, 2, 25.6600, 91.8900, "A reservoir lake with water sports."),
        ("Elephant Falls", "nature", 20, 1, 25.5430, 91.8130, "A multi-tiered waterfall near the city."),
        ("Don Bosco Centre for Indigenous Cultures", "museums culture", 100, 2, 25.5740, 91.8830, "A museum on the cultures of the North-East."),
        ("Shillong Peak", "nature", 20, 1, 25.5330, 91.8700, "The highest point near the city with views."),
    ]),
    ("Meghalaya", "Cherrapunji", [
        ("Nohkalikai Falls", "nature", 20, 1, 25.2590, 91.6990, "One of the tallest waterfalls in India."),
        ("Mawsmai Cave", "nature adventure", 30, 1, 25.2640, 91.7400, "A limestone cave with lit passages."),
        ("Double Decker Living Root Bridge", "nature culture adventure", 80, 4, 25.2500, 91.6790, "A bridge grown from tree roots, reached by a long stair trek."),
        ("Seven Sisters Falls", "nature", 0, 1, 25.2630, 91.7330, "A wide waterfall that is best viewed after rain."),
    ]),
    ("Manipur", "Imphal", [
        ("Loktak Lake", "nature wildlife culture", 0, 3, 24.5200, 93.8000, "A large lake with floating islands."),
        ("Kangla Fort", "history culture", 20, 1.5, 24.8150, 93.9480, "A historic palace site with temples."),
        ("Ima Keithel", "shopping culture", 0, 1.5, 24.8060, 93.9370, "A market run by women traders."),
        ("Shri Govindajee Temple", "religious", 0, 1, 24.8200, 93.9500, "A major Vaishnav temple."),
        ("INA Memorial Moirang", "history museums", 10, 1, 24.4980, 93.7660, "A memorial and museum on the Indian National Army."),
    ]),
    ("Mizoram", "Aizawl", [
        ("Mizoram State Museum", "museums culture", 10, 1.5, N, N, "A museum on the culture of the Mizo people."),
        ("Solomon's Temple", "religious architecture", 0, 1, N, N, "A large modern church."),
        ("Durtlang Hills", "nature", 0, 1.5, N, N, "A hill area with views of the city."),
        ("Reiek Heritage Village", "nature culture adventure", 20, 3, N, N, "A hill village and trek area."),
    ]),
    ("Nagaland", "Kohima", [
        ("Kohima War Cemetery", "history", 0, 1, 25.6630, 94.1040, "A memorial garden for soldiers of WWII."),
        ("Kisama Heritage Village", "culture museums", 20, 2, 25.6420, 94.1050, "Venue of the annual Hornbill Festival with traditional houses."),
        ("Dzukou Valley", "nature adventure", 0, 8, 25.5530, 94.0710, "A high valley known for trekking and flowers in season."),
        ("Nagaland State Museum", "museums culture", 10, 1.5, 25.6600, 94.1050, "A museum on Naga cultures."),
    ]),
    ("Tripura", "Agartala", [
        ("Ujjayanta Palace", "history architecture museums", 0, 1.5, 23.8350, 91.2820, "A former royal palace housing a museum."),
        ("Neermahal", "history architecture nature", 20, 2, 23.5110, 91.3010, "A palace in the middle of a lake, reached by boat."),
        ("Tripura Sundari Temple", "religious", 0, 1, 23.4880, 91.4840, "A major Shakti temple at Udaipur town."),
        ("Heritage Park Agartala", "nature culture", 20, 1, N, N, "A themed park on regional heritage."),
    ]),
    # ------------------------------------------------------------------ Islands & Puducherry
    ("Andaman and Nicobar Islands", "Port Blair", [
        ("Cellular Jail", "history museums", 30, 1.5, 11.6740, 92.7480, "A colonial-era prison with a light and sound show."),
        ("Ross Island", "history nature", 50, 2, 11.6770, 92.7640, "Ruins on a small island reached by ferry."),
        ("Radhanagar Beach (Havelock)", "nature adventure", 0, 3, 11.9820, 92.9510, "A wide white-sand beach on Havelock Island, reached by ferry."),
        ("Corbyn's Cove Beach", "nature adventure", 0, 1.5, 11.6460, 92.7510, "A beach near Port Blair for swimming and water sports."),
        ("Samudrika Naval Maritime Museum", "museums nature", 30, 1.5, 11.6580, 92.7390, "A museum about marine life and the islands."),
    ]),
    ("Lakshadweep", "Agatti", [
        ("Agatti Island Lagoon", "nature adventure", 0, 4, N, N, "A lagoon for snorkelling and water sports; permit needed to visit the islands."),
        ("Bangaram Atoll", "nature adventure", 0, 4, N, N, "An uninhabited-style coral island known for diving."),
        ("Kavaratti Marine Aquarium", "nature museums", 20, 1, N, N, "A small aquarium showing local marine life."),
    ]),
    ("Puducherry", "Puducherry", [
        ("Promenade Beach", "nature culture", 0, 1.5, 11.9340, 79.8340, "A seafront walkway in the French Quarter."),
        ("Auroville Matrimandir", "culture religious architecture", 0, 2, 12.0070, 79.8100, "A golden spherical meditation space; viewing by pass."),
        ("Paradise Beach", "nature", 100, 2, 11.8970, 79.8110, "A quiet beach reached by a short boat ride."),
        ("Sri Aurobindo Ashram", "religious culture", 0, 1, 11.9350, 79.8330, "A spiritual centre in the old town."),
        ("Basilica of the Sacred Heart of Jesus", "religious architecture", 0, 0.5, 11.9260, 79.8300, "A Gothic-style church."),
    ]),
]
