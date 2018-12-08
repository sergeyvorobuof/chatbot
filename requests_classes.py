from stop_words import get_stop_words

# Description classes of different requests


class1 = ['где поесть','Покажи все достопримечательности', 'Покажи места на Таганке', 'куда сходить на новокузнецкой', 'покажи места рядом со мной', 'куда сходить рядом', 'кафе около меня', 'развлекательные места','интересные места', 'еда']

class2 = ['Напомни','уведомления','включи','включи уведомления', 'напоминалку включи', 'Включить уведомления', 'хочу доехать до Таганской', 'Разбуди меня', 'напомни мне переходы', 'я хочу поехать до Маяковской']

class3 = ['бульвар рокоссовского','черкизовская','преображенская площадь','сокольники','красносельская','комсомольская','красные ворота','чистые пруды','лубянка','охотный ряд','библиотека имени ленина','кропоткинская','парк культуры','фрунзенская','спортивная','воробьёвы горы','университет','проспект вернадского','юго-западная','тропарёво','румянцево','саларьево','ховрино','речной вокзал','водный стадион','войковская','сокол','аэропорт','динамо','белорусская','маяковская','тверская','театральная','новокузнецкая','павелецкая','автозаводская','технопарк','коломенская','каширская','кантемировская','царицыно','орехово','домодедовская','красногвардейская','алма-атинская','пятницкое шоссе','митино','волоколамская','мякинино','строгино','крылатское','молодёжная','кунцевская','славянский бульвар','парк победы','киевская','смоленская','арбатская','площадь революции','курская','бауманская','электрозаводская','семёновская','партизанская','измайловская','первомайская','щёлковская','кунцевская','пионерская','филёвский парк','багратионовская','фили','кутузовская','студенческая','международная','выставочная','киевская','смоленская','арбатская','александровский сад','киевская','краснопресненская','белорусская','новослободская','проспект мира','комсомольская','курская','таганская','павелецкая','добрынинская','октябрьская','парк культуры','медведково','бабушкинская','свиблово','ботанический сад','вднх','алексеевская','рижская','проспект мира','сухаревская','тургеневская','китай-город','третьяковская','октябрьская','шаболовская','ленинский проспект','академическая','профсоюзная','новые черёмушки','калужская','беляево','коньково','тёплый стан','ясенево','новоясеневская','планерная','сходненская','тушинская','спартак','щукинская','октябрьское поле','полежаевская','беговая','улица 1905 года','баррикадная','пушкинская','кузнецкий мост','китай-город','таганская','пролетарская','волгоградский проспект','текстильщики','кузьминки','рязанский проспект','выхино','лермонтовский проспект','жулебино','котельники','раменки','ломоносовский проспект','минская','парк победы','третьяковская','марксистская','площадь ильича','авиамоторная','шоссе энтузиастов','перово','новогиреево','новокосино','алтуфьево','бибирево','отрадное','владыкино','петровско-разумовская','тимирязевская','дмитровская','савёловская','менделеевская','цветной бульвар','чеховская','боровицкая','полянка','серпуховская','тульская','нагатинская','нагорная','нахимовский проспект','севастопольская','чертановская','южная','пражская','улица академика янгеля','аннино','бульвар дмитрия донского','селигерская','верхние лихоборы','окружная','петровско-разумовская','фонвизинская','бутырская','марьина роща','достоевская','трубная','сретенский бульвар','чкаловская','римская','крестьянская застава','дубровка','кожуховская','печатники','волжская','люблино','братиславская','марьино','борисово','шипиловская','зябликово','деловой центр','шелепиха','хорошёвская','цска','петровский парк','каширская','варшавская','каховская','битцевский парк','лесопарковая','улица старокачаловская','улица скобелевская','бульвар адмирала ушакова','улица горчакова','бунинская аллея','тимирязевская','улица милашенкова','телецентр','улица академика королёва','выставочный центр','улица сергея эйзенштейна','окружная','владыкино','ботанический сад','ростокино','белокаменная','бульвар рокоссовского','локомотив','измайлово','соколиная гора','шоссе энтузиастов','андроновка','нижегородская','новохохловская','угрешская','дубровка','автозаводская','зил','верхние котлы','крымская','площадь гагарина','лужники','кутузовская','деловой центр','шелепиха','хорошёво','зорге','панфиловская','стрешнево','балтийская','коптево','лихоборы']