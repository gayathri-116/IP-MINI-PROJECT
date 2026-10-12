-- WARNING: re-importing resets the demo database (users and bookings are cleared).
DROP DATABASE IF EXISTS wanderly;
CREATE DATABASE wanderly CHARACTER SET utf8mb4;
USE wanderly;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(80) NOT NULL, email VARCHAR(120) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL, role ENUM('user','admin') DEFAULT 'user', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE packages (
  id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(120) NOT NULL, destination VARCHAR(120) NOT NULL,
  country VARCHAR(40) NOT NULL DEFAULT 'India',
  region VARCHAR(20) NOT NULL, category VARCHAR(30) NOT NULL, days INT NOT NULL, price DECIMAL(10,2) NOT NULL,
  summary VARCHAR(255) NOT NULL, details TEXT NOT NULL, keywords VARCHAR(120) NOT NULL
);
CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, package_id INT NOT NULL, travel_date DATE NOT NULL,
  travellers INT NOT NULL, total DECIMAL(10,2) NOT NULL, status ENUM('Pending','Confirmed','Cancelled') DEFAULT 'Pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (package_id) REFERENCES packages(id) ON DELETE CASCADE
);
CREATE TABLE messages (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(80), email VARCHAR(120), message TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

INSERT INTO packages (title,destination,country,region,category,days,price,summary,details,keywords) VALUES
-- NORTH
('Kashmir Paradise','Srinagar, Gulmarg, Pahalgam (Jammu & Kashmir)','India','North','Nature',6,24500,'Dal Lake shikara, Gulmarg gondola and Pahalgam meadows.','Day 1 Srinagar and Dal Lake. Day 2 Mughal gardens. Day 3-4 Gulmarg. Day 5 Pahalgam. Day 6 return.','kashmir,dal,lake'),
('Leh Ladakh Road Trip','Leh, Nubra, Pangong (Ladakh)','India','North','Adventure',8,38900,'Khardung La, Nubra camels and Pangong Lake sunsets.','Acclimatise in Leh, monasteries, Nubra Valley, Pangong Tso, Sham Valley, return.','ladakh,pangong'),
('Manali & Shimla Escape','Manali, Shimla (Himachal Pradesh)','India','North','Adventure',6,16800,'Snow at Solang, toy train views and Mall Road evenings.','Shimla Mall Road and Kufri, drive to Manali, Solang, Atal Tunnel, Old Manali.','manali,himalaya'),
('Golden Temple & Wagah','Amritsar (Punjab)','India','North','Spiritual',3,8900,'Langar at the Golden Temple, Jallianwala Bagh, Wagah ceremony.','Day 1 Golden Temple. Day 2 Jallianwala Bagh and food walk. Day 3 Wagah border.','amritsar,golden,temple'),
('Rishikesh & Haridwar Yatra','Rishikesh, Haridwar (Uttarakhand)','India','North','Spiritual',4,9500,'Ganga aarti, river rafting and yoga by the river.','Haridwar aarti, Rishikesh Laxman Jhula, rafting, yoga session, Neelkanth.','rishikesh,ganga'),
('Jim Corbett Tiger Safari','Jim Corbett (Uttarakhand)','India','North','Wildlife',3,12400,'Jeep safaris in India oldest national park.','Two safaris in Dhikala or Bijrani zones, nature walk, riverside stay.','jim,corbett,tiger'),
('Golden Triangle','Delhi, Agra, Jaipur','India','North','Heritage',5,15500,'Red Fort, Taj Mahal at sunrise and Amber Fort.','Old and New Delhi, Agra Taj and Fort, Fatehpur Sikri, Jaipur city palace.','taj,mahal,agra'),
('Varanasi & Ayodhya Darshan','Varanasi, Ayodhya (Uttar Pradesh)','India','North','Spiritual',4,11200,'Boat rides on the Ganga and the Ram temple.','Varanasi ghats and Ganga aarti, Sarnath, Ayodhya temples, Saryu ghat.','varanasi,ghat'),
('Royal Rajasthan','Jaipur, Jodhpur, Udaipur (Rajasthan)','India','North','Heritage',7,27500,'Palaces, lake cities and the blue city of Jodhpur.','Jaipur, Pushkar, Jodhpur Mehrangarh, Ranakpur, Udaipur City Palace and lake.','udaipur,palace'),
('Desert Forts of Jaisalmer','Jaisalmer, Bikaner (Rajasthan)','India','North','Adventure',4,14900,'Camel safari and a night under the Thar dunes.','Jaisalmer fort, havelis, Sam dunes camp with folk music, Bikaner Junagarh.','jaisalmer,desert'),
('Chandigarh & Kasauli Weekend','Chandigarh, Kasauli (Punjab, Haryana)','India','North','City',3,9200,'Rock Garden, Sukhna Lake and pine hill walks.','Rock Garden, Rose Garden, Sukhna Lake, Kasauli hill walk and Pinjore gardens.','chandigarh,rock,garden'),
-- WEST
('Goa Beach Break','North and South Goa','India','West','Beach',4,13500,'Beaches, Portuguese churches and seafood shacks.','Baga and Calangute, Old Goa churches, Dudhsagar, South Goa Palolem.','goa,beach'),
('Mumbai & Ajanta Ellora','Mumbai, Aurangabad (Maharashtra)','India','West','Heritage',5,17800,'Gateway of India, rock-cut caves and Bibi Ka Maqbara.','Mumbai city, Elephanta, drive to Aurangabad, Ajanta, Ellora, Daulatabad.','mumbai,gateway'),
('Rann of Kutch & Gir Lions','Kutch, Gir (Gujarat)','India','West','Wildlife',6,21500,'White salt desert and Asiatic lion safari.','Ahmedabad, Rann Utsav tents, Bhuj, Somnath, Gir safari, Statue of Unity.','kutch,rann,white,desert'),
-- CENTRAL
('Khajuraho & Kanha Tigers','Khajuraho, Kanha (Madhya Pradesh)','India','Central','Wildlife',6,22800,'Temple sculptures and Kipling country tiger safaris.','Orchha, Khajuraho temples, Bandhavgarh or Kanha safaris, Jabalpur.','khajuraho,temple'),
('Bastar & Chitrakote Falls','Jagdalpur (Chhattisgarh)','India','Central','Nature',4,12600,'Indias widest waterfall and tribal Bastar markets.','Chitrakote falls, Tirathgarh, Kanger Valley caves, tribal village visit.','chitrakote,waterfall'),
-- EAST
('Kolkata & Darjeeling','Kolkata, Darjeeling (West Bengal)','India','East','Heritage',6,19600,'Victoria Memorial, toy train and Tiger Hill sunrise.','Kolkata trams and food, Darjeeling toy train, tea gardens, Tiger Hill.','darjeeling,tea'),
('Sundarbans Mangrove Cruise','Sundarbans (West Bengal)','India','East','Wildlife',3,10800,'Boat safari through the mangrove tiger reserve.','Drive from Kolkata, launch cruise, watchtowers, village visit.','sundarbans,mangrove'),
('Puri, Konark & Chilika','Puri, Bhubaneswar (Odisha)','India','East','Spiritual',5,13900,'Jagannath temple, Sun Temple and dolphins at Chilika.','Bhubaneswar temples, Konark, Puri beach, Chilika lake boat ride.','konark,sun,temple'),
('Buddhist Circuit','Bodh Gaya, Rajgir, Nalanda (Bihar)','India','East','Spiritual',4,11500,'Mahabodhi Temple and ruins of Nalanda.','Bodh Gaya, Rajgir ropeway, Nalanda ruins, Vaishali, Patna.','bodh,gaya,mahabodhi'),
('Jharkhand Waterfalls','Ranchi, Netarhat (Jharkhand)','India','East','Nature',4,10400,'Hundru and Dassam falls and Netarhat sunset.','Ranchi, Hundru, Jonha and Dassam falls, Betla National Park, Netarhat.','jharkhand,waterfall'),
-- NORTH-EAST
('Kaziranga & Meghalaya','Guwahati, Kaziranga, Shillong','India','North-East','Wildlife',7,28500,'One-horned rhinos and living root bridges.','Kamakhya, Kaziranga elephant safari, Shillong, Cherrapunji, Dawki river.','kaziranga,rhino'),
('Sikkim Himalaya','Gangtok, Pelling (Sikkim)','India','North-East','Nature',6,20900,'Tsomgo Lake, monasteries and Kanchenjunga views.','Gangtok, Tsomgo Lake, Nathula pass, Pelling skywalk, Yuksom.','sikkim,gangtok'),
('Tawang & Arunachal','Tawang, Bomdila (Arunachal Pradesh)','India','North-East','Adventure',7,32500,'Tawang monastery and Sela Pass.','Bhalukpong, Dirang, Sela Pass, Tawang monastery, Madhuri lake.','tawang,monastery'),
('Nagaland Hornbill Trail','Kohima, Khonoma (Nagaland)','India','North-East','Heritage',5,24800,'Naga villages and the Hornbill Festival.','Kohima war cemetery, Khonoma green village, Dzukou valley, Hornbill Festival.','nagaland,hornbill'),
('Manipur & Loktak Lake','Imphal, Loktak (Manipur)','India','North-East','Nature',4,17400,'Floating phumdis and Kangla Fort.','Imphal, Kangla Fort, Loktak lake, Keibul Lamjao, Moreh.','loktak,manipur'),
('Mizoram & Tripura Discovery','Aizawl, Agartala','India','North-East','Heritage',6,23200,'Hill capital Aizawl and Ujjayanta Palace.','Agartala palace, Neermahal, Aizawl, Reiek peak, local crafts.','tripura,palace'),
-- SOUTH
('Backwaters & Spice Hills','Kochi, Munnar, Alleppey (Kerala)','India','South','Nature',6,18500,'Houseboat nights and tea estate walks.','Kochi, Munnar tea, Thekkady spices, Alleppey houseboat stay.','kerala,backwaters'),
('Temple Trail of Tamil Nadu','Madurai, Rameswaram (Tamil Nadu)','India','South','Spiritual',4,9800,'Meenakshi Temple and Dhanushkodi.','Madurai temple, Rameswaram, Pamban bridge, Dhanushkodi, Chettinad lunch.','madurai,meenakshi,temple'),
('Ooty & Kodaikanal Hills','Ooty, Kodaikanal (Tamil Nadu)','India','South','Nature',5,13800,'Nilgiri toy train and Kodai lake mist.','Coonoor, Ooty botanical garden, toy train, Kodaikanal lake, Pillar Rocks.','ooty,nilgiri'),
('Pondicherry Heritage Stay','Puducherry','India','South','Beach',3,9600,'French Quarter, Auroville and Promenade beach.','French Quarter walk, Auroville Matrimandir, Paradise beach, cafes.','pondicherry,french,quarter'),
('Hampi & Mysore Palaces','Hampi, Mysore (Karnataka)','India','South','Heritage',6,17200,'Vijayanagara ruins and Mysore Palace lights.','Bengaluru, Mysore palace, Srirangapatna, Hampi ruins, Badami.','hampi,ruins'),
('Coorg Coffee Country','Coorg (Karnataka)','India','South','Nature',3,11400,'Coffee plantation stay and Abbey Falls.','Plantation stay, Abbey falls, Dubare elephant camp, Talakaveri.','coorg,coffee'),
('Hyderabad Nizam Trail','Hyderabad (Telangana)','India','South','City',3,9900,'Charminar, Golconda and biryani trails.','Charminar, Golconda Fort, Ramoji Film City, Hussain Sagar.','hyderabad,charminar'),
('Tirupati & Araku Valley','Tirupati, Visakhapatnam (Andhra Pradesh)','India','South','Spiritual',5,12800,'Balaji darshan and coffee hills of Araku.','Tirumala darshan, Srikalahasti, Vizag beaches, Araku train, Borra caves.','tirupati,araku'),
-- ISLANDS
('Island Days in the Andamans','Port Blair, Havelock','India','Islands','Beach',6,31500,'Radhanagar beach and snorkelling.','Cellular Jail, Havelock, Elephant Beach, Neil Island, Ross Island.','andaman,havelock,beach'),
('Lakshadweep Lagoons','Agatti, Bangaram','India','Islands','Beach',5,36500,'Coral lagoons, kayaking and glass-bottom boats.','Fly to Agatti, lagoon snorkelling, Bangaram island, kayaking, return.','lakshadweep,lagoon'),
-- INTERNATIONAL
('Dubai Desert & Skyline','Dubai','UAE','International','City',5,68000,'Burj Khalifa, desert safari and Abu Dhabi day trip.','Burj Khalifa, Dubai Mall, desert safari, dhow cruise, Sheikh Zayed Mosque.','dubai,skyline'),
('Singapore & Sentosa','Singapore','Singapore','International','City',4,72000,'Gardens by the Bay, Sentosa and night safari.','Marina Bay, Gardens by the Bay, Sentosa, Universal Studios, Night Safari.','singapore,marina,bay'),
('Bangkok & Phuket','Bangkok, Phuket','Thailand','International','Beach',6,59000,'Grand Palace temples and Phi Phi island hopping.','Bangkok palace and markets, flight to Phuket, Phi Phi tour, James Bond island.','thailand,phuket'),
('Bali Island Retreat','Ubud, Seminyak','Indonesia','International','Beach',5,64000,'Rice terraces, sea temples and beach clubs.','Ubud rice terraces, Tanah Lot, Uluwatu temple, Nusa Penida, Seminyak.','bali,temple'),
('Maldives Overwater Escape','Male, Maafushi','Maldives','International','Beach',4,95000,'Overwater villas, snorkelling and sandbank picnics.','Speedboat transfer, snorkelling with reef sharks, sunset cruise, sandbank.','maldives,overwater'),
('Paris & Swiss Alps','Paris, Interlaken, Lucerne','France/Switzerland','International','City',9,255000,'Eiffel Tower evenings and Jungfraujoch snow.','Paris Louvre and Eiffel, TGV to Switzerland, Interlaken, Jungfraujoch, Lucerne.','paris,eiffel'),
('London & Scotland','London, Edinburgh','United Kingdom','International','City',7,225000,'Tower Bridge, Buckingham Palace and Edinburgh Castle.','London sights, Windsor Castle, train to Edinburgh, Highlands day tour.','london,tower,bridge'),
('Tokyo & Mount Fuji','Tokyo, Kyoto','Japan','International','City',7,210000,'Shibuya crossing, Fuji views and Kyoto shrines.','Tokyo Shibuya and Asakusa, Mount Fuji, bullet train, Kyoto temples, Osaka.','tokyo,fuji'),
('Kuala Lumpur & Langkawi','Kuala Lumpur, Langkawi','Malaysia','International','City',5,56000,'Petronas Towers and island beaches.','Petronas Towers, Batu Caves, flight to Langkawi, cable car, island hopping.','kuala,lumpur,petronas'),
('Sri Lanka Ramayana & Beaches','Colombo, Kandy, Galle','Sri Lanka','International','Heritage',6,48000,'Sigiriya rock, tea hills and Galle Fort.','Colombo, Sigiriya, Kandy Temple of Tooth, Nuwara Eliya, Galle Fort.','sri,lanka,sigiriya'),
('Nepal Kathmandu & Pokhara','Kathmandu, Pokhara','Nepal','International','Spiritual',5,34000,'Pashupatinath, Boudhanath and Phewa Lake.','Kathmandu temples, Nagarkot sunrise, Pokhara lake, Sarangkot.','kathmandu,stupa'),
('Bhutan Happiness Trail','Paro, Thimphu','Bhutan','International','Heritage',6,78000,'Tigers Nest monastery and Dzong fortresses.','Paro, Tigers Nest hike, Thimphu, Punakha Dzong, Dochula pass.','bhutan,taktsang'),
('Turkey Istanbul & Cappadocia','Istanbul, Cappadocia','Turkey','International','Heritage',7,165000,'Hagia Sophia and hot air balloons at dawn.','Istanbul Blue Mosque and Bosphorus, flight to Cappadocia, balloon ride, caves.','cappadocia,balloons'),
('Vietnam Ha Long & Hanoi','Hanoi, Ha Long Bay','Vietnam','International','Nature',6,62000,'Limestone bay cruise and Old Quarter street food.','Hanoi Old Quarter, Ha Long Bay cruise, Ninh Binh, Ho Chi Minh City.','halong,bay'),
('New York & Niagara','New York, Niagara Falls','USA','International','City',8,365000,'Statue of Liberty, Times Square and Niagara Falls.','Manhattan, Statue of Liberty, Central Park, Washington DC, Niagara Falls.','new,york,skyline'),
('Sydney & Great Barrier Reef','Sydney, Cairns','Australia','International','Beach',8,330000,'Opera House harbour and reef snorkelling.','Sydney Opera House, Blue Mountains, flight to Cairns, reef cruise, Kuranda.','sydney,opera,house'),
('Mauritius Island Holiday','Port Louis, Grand Baie','Mauritius','International','Beach',5,85000,'Turquoise lagoons and Seven Coloured Earths.','Grand Baie, Ile aux Cerfs, Chamarel, Black River gorges, catamaran cruise.','mauritius,beach'),
('Egypt Pyramids & Nile','Cairo, Luxor','Egypt','International','Heritage',7,142000,'Giza pyramids and a Nile cruise.','Giza pyramids, Egyptian Museum, flight to Luxor, Valley of the Kings, Nile cruise.','egypt,pyramids');
