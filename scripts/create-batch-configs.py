#!/usr/bin/env python3
"""Create all 32 book configs for naturaleza, numeros, musica, mi-mundo."""
import json, os

CONFIGS_DIR = os.path.join(os.path.dirname(__file__), 'configs')

PROMPT_PREFIX = "Warm, child-friendly watercolor illustration, landscape 16:9 format, soft pastel colors, "

books = [
    # NATURALEZA (weeks 80-87)
    {
        "slug": "week-80-el-sol", "title": "El Sol", "subtitle": "The Sun", "theme": "naturaleza", "week": 80, "emoji": "☀️",
        "meta_desc": "Learn about the sun in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el sol Spanish, sun Spanish kids, bilingual children books",
        "pages": [
            {"title": "El Sol", "footer": "The Sun", "prompt": PROMPT_PREFIX + "a bright friendly sun rising over green hills with a small village below, morning light."},
            {"title": "El sol brilla.", "footer": "The sun shines.", "prompt": PROMPT_PREFIX + "a radiant sun shining brightly in a blue sky with fluffy clouds, rays of warm light."},
            {"title": "El sol es amarillo.", "footer": "The sun is yellow.", "prompt": PROMPT_PREFIX + "a happy yellow sun with gentle rays illuminating a field of sunflowers."},
            {"title": "El sol da calor.", "footer": "The sun gives warmth.", "prompt": PROMPT_PREFIX + "children playing in a sunny park, feeling warm sunshine on their faces."},
            {"title": "El sol sale temprano.", "footer": "The sun rises early.", "prompt": PROMPT_PREFIX + "a beautiful sunrise over mountains with orange and pink sky, birds flying."},
            {"title": "El sol se esconde.", "footer": "The sun hides.", "prompt": PROMPT_PREFIX + "a sunset scene with the sun dipping below the horizon, purple and orange sky."},
            {"title": "¡Gracias, sol!", "footer": "Thank you, sun!", "prompt": PROMPT_PREFIX + "a child waving at a friendly smiling sun in a bright sky with a rainbow."},
        ],
        "vocab": [{"es":"sol","en":"sun","emoji":"☀️"},{"es":"brilla","en":"shines","emoji":"✨"},{"es":"amarillo","en":"yellow","emoji":"🟡"},{"es":"calor","en":"warmth","emoji":"🔥"},{"es":"temprano","en":"early","emoji":"🌅"},{"es":"cielo","en":"sky","emoji":"🌤️"}],
        "badge": {"emoji":"☀️","name":"Amigo del Sol","nameEn":"Friend of the Sun"}
    },
    {
        "slug": "week-81-la-luna", "title": "La Luna", "subtitle": "The Moon", "theme": "naturaleza", "week": 81, "emoji": "🌙",
        "meta_desc": "Learn about the moon in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, la luna Spanish, moon Spanish kids",
        "pages": [
            {"title": "La Luna", "footer": "The Moon", "prompt": PROMPT_PREFIX + "a beautiful full moon in a starry night sky over a quiet village."},
            {"title": "La luna es redonda.", "footer": "The moon is round.", "prompt": PROMPT_PREFIX + "a big round moon glowing softly in a dark blue sky."},
            {"title": "La luna brilla de noche.", "footer": "The moon shines at night.", "prompt": PROMPT_PREFIX + "moonlight shining over a peaceful lake at night with reflections."},
            {"title": "La luna es blanca.", "footer": "The moon is white.", "prompt": PROMPT_PREFIX + "a white moon glowing against deep blue sky with gentle clouds."},
            {"title": "Los animales ven la luna.", "footer": "The animals see the moon.", "prompt": PROMPT_PREFIX + "cute animals like owls and rabbits looking up at the moon in a forest."},
            {"title": "La luna nos cuida.", "footer": "The moon watches over us.", "prompt": PROMPT_PREFIX + "a child sleeping peacefully in bed with moonlight coming through the window."},
            {"title": "¡Buenas noches, luna!", "footer": "Good night, moon!", "prompt": PROMPT_PREFIX + "a child in pajamas waving at a friendly moon from their window."},
        ],
        "vocab": [{"es":"luna","en":"moon","emoji":"🌙"},{"es":"redonda","en":"round","emoji":"⭕"},{"es":"noche","en":"night","emoji":"🌃"},{"es":"blanca","en":"white","emoji":"⬜"},{"es":"brilla","en":"shines","emoji":"✨"},{"es":"estrellas","en":"stars","emoji":"⭐"}],
        "badge": {"emoji":"🌙","name":"Explorador Nocturno","nameEn":"Night Explorer"}
    },
    {
        "slug": "week-82-las-estrellas", "title": "Las Estrellas", "subtitle": "The Stars", "theme": "naturaleza", "week": 82, "emoji": "⭐",
        "meta_desc": "Learn about stars in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, las estrellas Spanish, stars Spanish kids",
        "pages": [
            {"title": "Las Estrellas", "footer": "The Stars", "prompt": PROMPT_PREFIX + "a magical night sky full of bright twinkling stars over a meadow."},
            {"title": "Las estrellas brillan.", "footer": "The stars shine.", "prompt": PROMPT_PREFIX + "thousands of sparkling stars twinkling in a deep blue sky."},
            {"title": "Las estrellas son muchas.", "footer": "There are many stars.", "prompt": PROMPT_PREFIX + "a vast sky filled with countless stars, milky way visible, child looking up."},
            {"title": "Una estrella fugaz.", "footer": "A shooting star.", "prompt": PROMPT_PREFIX + "a bright shooting star streaking across a night sky over a hill."},
            {"title": "Las estrellas hacen formas.", "footer": "Stars make shapes.", "prompt": PROMPT_PREFIX + "constellations connected by glowing lines in the sky, a bear shape visible."},
            {"title": "Yo cuento estrellas.", "footer": "I count stars.", "prompt": PROMPT_PREFIX + "a child lying on grass pointing at stars and counting them."},
            {"title": "¡Me gustan las estrellas!", "footer": "I like the stars!", "prompt": PROMPT_PREFIX + "a happy child hugging a star-shaped pillow under a starry sky."},
        ],
        "vocab": [{"es":"estrellas","en":"stars","emoji":"⭐"},{"es":"brillan","en":"shine","emoji":"✨"},{"es":"muchas","en":"many","emoji":"🔢"},{"es":"fugaz","en":"shooting","emoji":"💫"},{"es":"formas","en":"shapes","emoji":"🔷"},{"es":"cuento","en":"I count","emoji":"🔢"}],
        "badge": {"emoji":"⭐","name":"Cazador de Estrellas","nameEn":"Star Hunter"}
    },
    {
        "slug": "week-83-la-montana", "title": "La Montaña", "subtitle": "The Mountain", "theme": "naturaleza", "week": 83, "emoji": "🏔️",
        "meta_desc": "Learn about mountains in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, la montaña Spanish, mountain Spanish kids",
        "pages": [
            {"title": "La Montaña", "footer": "The Mountain", "prompt": PROMPT_PREFIX + "a majestic mountain with a snowy peak under a blue sky with fluffy clouds."},
            {"title": "La montaña es alta.", "footer": "The mountain is tall.", "prompt": PROMPT_PREFIX + "a very tall mountain reaching into the clouds, tiny trees at the base."},
            {"title": "La montaña tiene nieve.", "footer": "The mountain has snow.", "prompt": PROMPT_PREFIX + "a snow-covered mountain peak sparkling in sunlight."},
            {"title": "Hay árboles en la montaña.", "footer": "There are trees on the mountain.", "prompt": PROMPT_PREFIX + "a mountain covered with green pine trees and wildflowers."},
            {"title": "Los animales viven aquí.", "footer": "Animals live here.", "prompt": PROMPT_PREFIX + "cute mountain animals like deer and eagles on a mountainside."},
            {"title": "Yo subo la montaña.", "footer": "I climb the mountain.", "prompt": PROMPT_PREFIX + "a child happily hiking up a mountain trail with a small backpack."},
            {"title": "¡Qué linda montaña!", "footer": "What a beautiful mountain!", "prompt": PROMPT_PREFIX + "a child at the top of a mountain looking at a beautiful panoramic view."},
        ],
        "vocab": [{"es":"montaña","en":"mountain","emoji":"🏔️"},{"es":"alta","en":"tall","emoji":"📏"},{"es":"nieve","en":"snow","emoji":"❄️"},{"es":"árboles","en":"trees","emoji":"🌲"},{"es":"animales","en":"animals","emoji":"🦌"},{"es":"subo","en":"I climb","emoji":"🧗"}],
        "badge": {"emoji":"🏔️","name":"Escalador Valiente","nameEn":"Brave Climber"}
    },
    {
        "slug": "week-84-el-bosque", "title": "El Bosque", "subtitle": "The Forest", "theme": "naturaleza", "week": 84, "emoji": "🌲",
        "meta_desc": "Learn about the forest in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el bosque Spanish, forest Spanish kids",
        "pages": [
            {"title": "El Bosque", "footer": "The Forest", "prompt": PROMPT_PREFIX + "a magical enchanted forest with tall green trees and sunlight filtering through leaves."},
            {"title": "El bosque tiene árboles.", "footer": "The forest has trees.", "prompt": PROMPT_PREFIX + "many tall trees in a lush green forest with a winding path."},
            {"title": "Hay flores en el bosque.", "footer": "There are flowers in the forest.", "prompt": PROMPT_PREFIX + "colorful wildflowers growing on the forest floor among tree trunks."},
            {"title": "Los pájaros cantan.", "footer": "The birds sing.", "prompt": PROMPT_PREFIX + "cute colorful birds singing on tree branches in a sunlit forest."},
            {"title": "Una ardilla salta.", "footer": "A squirrel jumps.", "prompt": PROMPT_PREFIX + "a cute fluffy squirrel jumping between tree branches in a forest."},
            {"title": "El bosque es verde.", "footer": "The forest is green.", "prompt": PROMPT_PREFIX + "a lush green forest with ferns, moss, and bright green leaves everywhere."},
            {"title": "¡Me encanta el bosque!", "footer": "I love the forest!", "prompt": PROMPT_PREFIX + "a happy child exploring a friendly forest with butterflies and sunshine."},
        ],
        "vocab": [{"es":"bosque","en":"forest","emoji":"🌲"},{"es":"árboles","en":"trees","emoji":"🌳"},{"es":"flores","en":"flowers","emoji":"🌸"},{"es":"pájaros","en":"birds","emoji":"🐦"},{"es":"ardilla","en":"squirrel","emoji":"🐿️"},{"es":"verde","en":"green","emoji":"🟢"}],
        "badge": {"emoji":"🌲","name":"Guardián del Bosque","nameEn":"Forest Guardian"}
    },
    {
        "slug": "week-85-el-desierto", "title": "El Desierto", "subtitle": "The Desert", "theme": "naturaleza", "week": 85, "emoji": "🏜️",
        "meta_desc": "Learn about the desert in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el desierto Spanish, desert Spanish kids",
        "pages": [
            {"title": "El Desierto", "footer": "The Desert", "prompt": PROMPT_PREFIX + "a vast beautiful desert with golden sand dunes under a bright blue sky."},
            {"title": "El desierto es grande.", "footer": "The desert is big.", "prompt": PROMPT_PREFIX + "endless sand dunes stretching to the horizon under a big sky."},
            {"title": "Hay cactus aquí.", "footer": "There are cacti here.", "prompt": PROMPT_PREFIX + "friendly-looking saguaro cacti standing tall in a sandy desert."},
            {"title": "El sol calienta.", "footer": "The sun heats up.", "prompt": PROMPT_PREFIX + "bright sun beating down on desert sand with heat shimmer."},
            {"title": "Un lagarto corre.", "footer": "A lizard runs.", "prompt": PROMPT_PREFIX + "a cute colorful lizard running across desert sand near a rock."},
            {"title": "La arena es suave.", "footer": "The sand is soft.", "prompt": PROMPT_PREFIX + "soft golden sand ripples in the desert with gentle wind patterns."},
            {"title": "¡El desierto es bonito!", "footer": "The desert is pretty!", "prompt": PROMPT_PREFIX + "a stunning desert sunset with orange and purple sky over sand dunes."},
        ],
        "vocab": [{"es":"desierto","en":"desert","emoji":"🏜️"},{"es":"grande","en":"big","emoji":"🔶"},{"es":"cactus","en":"cactus","emoji":"🌵"},{"es":"sol","en":"sun","emoji":"☀️"},{"es":"lagarto","en":"lizard","emoji":"🦎"},{"es":"arena","en":"sand","emoji":"⏳"}],
        "badge": {"emoji":"🏜️","name":"Aventurero del Desierto","nameEn":"Desert Adventurer"}
    },
    {
        "slug": "week-86-la-cascada", "title": "La Cascada", "subtitle": "The Waterfall", "theme": "naturaleza", "week": 86, "emoji": "💧",
        "meta_desc": "Learn about waterfalls in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, la cascada Spanish, waterfall Spanish kids",
        "pages": [
            {"title": "La Cascada", "footer": "The Waterfall", "prompt": PROMPT_PREFIX + "a beautiful waterfall cascading down mossy rocks into a clear pool surrounded by lush greenery."},
            {"title": "El agua cae.", "footer": "The water falls.", "prompt": PROMPT_PREFIX + "water flowing down rocks creating a gentle waterfall with mist."},
            {"title": "La cascada hace ruido.", "footer": "The waterfall makes noise.", "prompt": PROMPT_PREFIX + "a powerful waterfall splashing into rocks with spray and mist rising."},
            {"title": "El agua es fría.", "footer": "The water is cold.", "prompt": PROMPT_PREFIX + "crystal clear cold water in a waterfall pool with small fish visible."},
            {"title": "Hay un arcoíris.", "footer": "There is a rainbow.", "prompt": PROMPT_PREFIX + "a rainbow forming in the mist of a waterfall in a tropical forest."},
            {"title": "Las plantas crecen.", "footer": "Plants grow.", "prompt": PROMPT_PREFIX + "lush green ferns and flowers growing around a misty waterfall."},
            {"title": "¡Qué linda cascada!", "footer": "What a beautiful waterfall!", "prompt": PROMPT_PREFIX + "a child marveling at a majestic waterfall in a green paradise."},
        ],
        "vocab": [{"es":"cascada","en":"waterfall","emoji":"💧"},{"es":"agua","en":"water","emoji":"💦"},{"es":"cae","en":"falls","emoji":"⬇️"},{"es":"fría","en":"cold","emoji":"🥶"},{"es":"arcoíris","en":"rainbow","emoji":"🌈"},{"es":"plantas","en":"plants","emoji":"🌿"}],
        "badge": {"emoji":"💧","name":"Explorador de Cascadas","nameEn":"Waterfall Explorer"}
    },
    {
        "slug": "week-87-el-volcan", "title": "El Volcán", "subtitle": "The Volcano", "theme": "naturaleza", "week": 87, "emoji": "🌋",
        "meta_desc": "Learn about volcanoes in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el volcán Spanish, volcano Spanish kids",
        "pages": [
            {"title": "El Volcán", "footer": "The Volcano", "prompt": PROMPT_PREFIX + "a majestic volcano with a pointy top against a blue sky, friendly and not scary."},
            {"title": "El volcán es grande.", "footer": "The volcano is big.", "prompt": PROMPT_PREFIX + "a very large volcano towering over a small village, peaceful scene."},
            {"title": "El volcán tiene humo.", "footer": "The volcano has smoke.", "prompt": PROMPT_PREFIX + "gentle white smoke puffs coming from the top of a green volcano."},
            {"title": "La lava es roja.", "footer": "The lava is red.", "prompt": PROMPT_PREFIX + "gentle glowing orange-red lava flowing slowly down a volcano, not scary."},
            {"title": "El volcán duerme.", "footer": "The volcano sleeps.", "prompt": PROMPT_PREFIX + "a peaceful sleeping volcano covered in green grass and flowers."},
            {"title": "Hay rocas aquí.", "footer": "There are rocks here.", "prompt": PROMPT_PREFIX + "interesting volcanic rocks of different shapes around a volcano base."},
            {"title": "¡Qué fuerte el volcán!", "footer": "How strong the volcano is!", "prompt": PROMPT_PREFIX + "a mighty but friendly-looking volcano with a rainbow over it."},
        ],
        "vocab": [{"es":"volcán","en":"volcano","emoji":"🌋"},{"es":"grande","en":"big","emoji":"🔶"},{"es":"humo","en":"smoke","emoji":"💨"},{"es":"lava","en":"lava","emoji":"🔴"},{"es":"rocas","en":"rocks","emoji":"🪨"},{"es":"fuerte","en":"strong","emoji":"💪"}],
        "badge": {"emoji":"🌋","name":"Científico del Volcán","nameEn":"Volcano Scientist"}
    },
    # NÚMEROS (weeks 88-95)
    {
        "slug": "week-88-el-uno", "title": "El Uno", "subtitle": "The Number One", "theme": "numeros", "week": 88, "emoji": "1️⃣",
        "meta_desc": "Learn the number one in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el uno Spanish, number one Spanish kids",
        "pages": [
            {"title": "El Uno", "footer": "The Number One", "prompt": PROMPT_PREFIX + "a large friendly number 1 surrounded by one apple, one star, one flower."},
            {"title": "Uno es un número.", "footer": "One is a number.", "prompt": PROMPT_PREFIX + "a big colorful number 1 standing proudly on a hill."},
            {"title": "Tengo una manzana.", "footer": "I have one apple.", "prompt": PROMPT_PREFIX + "one big shiny red apple on a table, clearly just one."},
            {"title": "Veo una estrella.", "footer": "I see one star.", "prompt": PROMPT_PREFIX + "one bright star shining alone in a twilight sky."},
            {"title": "Una mariposa vuela.", "footer": "One butterfly flies.", "prompt": PROMPT_PREFIX + "one beautiful colorful butterfly flying over a flower garden."},
            {"title": "Un sol en el cielo.", "footer": "One sun in the sky.", "prompt": PROMPT_PREFIX + "one happy sun in a bright blue sky over a meadow."},
            {"title": "¡El uno es especial!", "footer": "One is special!", "prompt": PROMPT_PREFIX + "a child holding up one finger proudly, number 1 in the background."},
        ],
        "vocab": [{"es":"uno","en":"one","emoji":"1️⃣"},{"es":"manzana","en":"apple","emoji":"🍎"},{"es":"estrella","en":"star","emoji":"⭐"},{"es":"mariposa","en":"butterfly","emoji":"🦋"},{"es":"sol","en":"sun","emoji":"☀️"},{"es":"número","en":"number","emoji":"🔢"}],
        "badge": {"emoji":"1️⃣","name":"Maestro del Uno","nameEn":"Master of One"}
    },
    {
        "slug": "week-89-el-dos", "title": "El Dos", "subtitle": "The Number Two", "theme": "numeros", "week": 89, "emoji": "2️⃣",
        "meta_desc": "Learn the number two in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el dos Spanish, number two Spanish kids",
        "pages": [
            {"title": "El Dos", "footer": "The Number Two", "prompt": PROMPT_PREFIX + "a large friendly number 2 with two cute kittens next to it."},
            {"title": "Dos es un número.", "footer": "Two is a number.", "prompt": PROMPT_PREFIX + "a big colorful number 2 made of building blocks."},
            {"title": "Tengo dos manos.", "footer": "I have two hands.", "prompt": PROMPT_PREFIX + "a child showing two open hands, counting fingers."},
            {"title": "Veo dos pájaros.", "footer": "I see two birds.", "prompt": PROMPT_PREFIX + "two cute colorful birds sitting together on a branch."},
            {"title": "Dos ojos tengo.", "footer": "I have two eyes.", "prompt": PROMPT_PREFIX + "a friendly child's face with two big bright eyes, pointing at them."},
            {"title": "Dos pies para caminar.", "footer": "Two feet to walk.", "prompt": PROMPT_PREFIX + "two small feet in colorful shoes walking on a path."},
            {"title": "¡El dos es divertido!", "footer": "Two is fun!", "prompt": PROMPT_PREFIX + "two children playing together, number 2 in the background."},
        ],
        "vocab": [{"es":"dos","en":"two","emoji":"2️⃣"},{"es":"manos","en":"hands","emoji":"🙌"},{"es":"pájaros","en":"birds","emoji":"🐦"},{"es":"ojos","en":"eyes","emoji":"👀"},{"es":"pies","en":"feet","emoji":"🦶"},{"es":"caminar","en":"walk","emoji":"🚶"}],
        "badge": {"emoji":"2️⃣","name":"Maestro del Dos","nameEn":"Master of Two"}
    },
    {
        "slug": "week-90-el-tres", "title": "El Tres", "subtitle": "The Number Three", "theme": "numeros", "week": 90, "emoji": "3️⃣",
        "meta_desc": "Learn the number three in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el tres Spanish, number three Spanish kids",
        "pages": [
            {"title": "El Tres", "footer": "The Number Three", "prompt": PROMPT_PREFIX + "a large friendly number 3 with three colorful balloons."},
            {"title": "Tres es un número.", "footer": "Three is a number.", "prompt": PROMPT_PREFIX + "a big colorful number 3 made of flowers."},
            {"title": "Tres globos en el aire.", "footer": "Three balloons in the air.", "prompt": PROMPT_PREFIX + "three bright colorful balloons floating in a blue sky."},
            {"title": "Tres colores bonitos.", "footer": "Three pretty colors.", "prompt": PROMPT_PREFIX + "three paint splashes in red, blue, and yellow."},
            {"title": "Tres gatitos juegan.", "footer": "Three kittens play.", "prompt": PROMPT_PREFIX + "three adorable kittens playing with a ball of yarn."},
            {"title": "Tres flores crecen.", "footer": "Three flowers grow.", "prompt": PROMPT_PREFIX + "three beautiful flowers growing in a garden, each a different color."},
            {"title": "¡Me gusta el tres!", "footer": "I like three!", "prompt": PROMPT_PREFIX + "a child holding three fingers up with a big smile."},
        ],
        "vocab": [{"es":"tres","en":"three","emoji":"3️⃣"},{"es":"globos","en":"balloons","emoji":"🎈"},{"es":"colores","en":"colors","emoji":"🎨"},{"es":"gatitos","en":"kittens","emoji":"🐱"},{"es":"flores","en":"flowers","emoji":"🌸"},{"es":"crecen","en":"grow","emoji":"🌱"}],
        "badge": {"emoji":"3️⃣","name":"Maestro del Tres","nameEn":"Master of Three"}
    },
    {
        "slug": "week-91-el-cuatro", "title": "El Cuatro", "subtitle": "The Number Four", "theme": "numeros", "week": 91, "emoji": "4️⃣",
        "meta_desc": "Learn the number four in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el cuatro Spanish, number four Spanish kids",
        "pages": [
            {"title": "El Cuatro", "footer": "The Number Four", "prompt": PROMPT_PREFIX + "a large friendly number 4 with four cute puppies around it."},
            {"title": "Cuatro es un número.", "footer": "Four is a number.", "prompt": PROMPT_PREFIX + "a big colorful number 4 made of stars."},
            {"title": "Cuatro patas tiene el perro.", "footer": "The dog has four legs.", "prompt": PROMPT_PREFIX + "a cute puppy standing showing four legs, each leg highlighted."},
            {"title": "Cuatro ruedas tiene el carro.", "footer": "The car has four wheels.", "prompt": PROMPT_PREFIX + "a cute colorful toy car showing four round wheels."},
            {"title": "Cuatro estaciones del año.", "footer": "Four seasons of the year.", "prompt": PROMPT_PREFIX + "four quadrants showing spring, summer, fall, winter scenes."},
            {"title": "Cuatro esquinas tiene.", "footer": "It has four corners.", "prompt": PROMPT_PREFIX + "a colorful square with four highlighted corners, playful design."},
            {"title": "¡Cuatro es genial!", "footer": "Four is great!", "prompt": PROMPT_PREFIX + "a child holding four fingers up proudly with four stars around."},
        ],
        "vocab": [{"es":"cuatro","en":"four","emoji":"4️⃣"},{"es":"patas","en":"legs","emoji":"🐾"},{"es":"ruedas","en":"wheels","emoji":"🛞"},{"es":"estaciones","en":"seasons","emoji":"🍂"},{"es":"esquinas","en":"corners","emoji":"🔷"},{"es":"carro","en":"car","emoji":"🚗"}],
        "badge": {"emoji":"4️⃣","name":"Maestro del Cuatro","nameEn":"Master of Four"}
    },
    {
        "slug": "week-92-el-cinco", "title": "El Cinco", "subtitle": "The Number Five", "theme": "numeros", "week": 92, "emoji": "5️⃣",
        "meta_desc": "Learn the number five in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el cinco Spanish, number five Spanish kids",
        "pages": [
            {"title": "El Cinco", "footer": "The Number Five", "prompt": PROMPT_PREFIX + "a large friendly number 5 with five colorful stars around it."},
            {"title": "Cinco es un número.", "footer": "Five is a number.", "prompt": PROMPT_PREFIX + "a big colorful number 5 made of building blocks."},
            {"title": "Cinco dedos en mi mano.", "footer": "Five fingers on my hand.", "prompt": PROMPT_PREFIX + "a child's hand showing five spread fingers, each a different color."},
            {"title": "Cinco manzanas rojas.", "footer": "Five red apples.", "prompt": PROMPT_PREFIX + "five shiny red apples arranged in a row on a table."},
            {"title": "Cinco patitos nadan.", "footer": "Five little ducks swim.", "prompt": PROMPT_PREFIX + "five cute yellow ducklings swimming in a row on a pond."},
            {"title": "Cinco amigos juegan.", "footer": "Five friends play.", "prompt": PROMPT_PREFIX + "five diverse children playing together in a circle in a park."},
            {"title": "¡Dame cinco!", "footer": "High five!", "prompt": PROMPT_PREFIX + "two children giving each other a high five with big smiles."},
        ],
        "vocab": [{"es":"cinco","en":"five","emoji":"5️⃣"},{"es":"dedos","en":"fingers","emoji":"🖐️"},{"es":"manzanas","en":"apples","emoji":"🍎"},{"es":"patitos","en":"ducklings","emoji":"🐥"},{"es":"amigos","en":"friends","emoji":"👫"},{"es":"juegan","en":"play","emoji":"⚽"}],
        "badge": {"emoji":"5️⃣","name":"Maestro del Cinco","nameEn":"Master of Five"}
    },
    {
        "slug": "week-93-las-letras", "title": "Las Letras", "subtitle": "The Letters", "theme": "numeros", "week": 93, "emoji": "🔤",
        "meta_desc": "Learn about letters in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, las letras Spanish, letters Spanish kids",
        "pages": [
            {"title": "Las Letras", "footer": "The Letters", "prompt": PROMPT_PREFIX + "colorful alphabet letters floating playfully in the air, A B C prominent."},
            {"title": "A es la primera.", "footer": "A is the first.", "prompt": PROMPT_PREFIX + "a big colorful letter A with an apple (manzana) next to it."},
            {"title": "B es de bebé.", "footer": "B is for baby.", "prompt": PROMPT_PREFIX + "a big colorful letter B with a cute baby next to it."},
            {"title": "C es de casa.", "footer": "C is for house.", "prompt": PROMPT_PREFIX + "a big colorful letter C with a cute house next to it."},
            {"title": "Las letras hacen palabras.", "footer": "Letters make words.", "prompt": PROMPT_PREFIX + "letters coming together to spell simple words like SOL and MAMA."},
            {"title": "Yo aprendo las letras.", "footer": "I learn the letters.", "prompt": PROMPT_PREFIX + "a child happily writing letters on a colorful chalkboard."},
            {"title": "¡Me gustan las letras!", "footer": "I like letters!", "prompt": PROMPT_PREFIX + "a child surrounded by floating colorful letters, reaching for them joyfully."},
        ],
        "vocab": [{"es":"letras","en":"letters","emoji":"🔤"},{"es":"primera","en":"first","emoji":"1️⃣"},{"es":"palabras","en":"words","emoji":"💬"},{"es":"aprendo","en":"I learn","emoji":"📚"},{"es":"escribo","en":"I write","emoji":"✏️"},{"es":"leo","en":"I read","emoji":"📖"}],
        "badge": {"emoji":"🔤","name":"Amigo de las Letras","nameEn":"Letter Friend"}
    },
    {
        "slug": "week-94-el-abecedario", "title": "El Abecedario", "subtitle": "The Alphabet", "theme": "numeros", "week": 94, "emoji": "📖",
        "meta_desc": "Learn the alphabet in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el abecedario Spanish, alphabet Spanish kids",
        "pages": [
            {"title": "El Abecedario", "footer": "The Alphabet", "prompt": PROMPT_PREFIX + "a beautiful alphabet chart with all letters in rainbow colors on a wall."},
            {"title": "A, B, C, D, E.", "footer": "A, B, C, D, E.", "prompt": PROMPT_PREFIX + "five big colorful letters A B C D E with cute animals for each."},
            {"title": "F, G, H, I, J.", "footer": "F, G, H, I, J.", "prompt": PROMPT_PREFIX + "five big colorful letters F G H I J with fun objects for each."},
            {"title": "K, L, M, N, Ñ.", "footer": "K, L, M, N, Ñ.", "prompt": PROMPT_PREFIX + "five big colorful letters K L M N Ñ with items for each."},
            {"title": "O, P, Q, R, S.", "footer": "O, P, Q, R, S.", "prompt": PROMPT_PREFIX + "five big colorful letters O P Q R S with pictures for each."},
            {"title": "Cantamos el abecedario.", "footer": "We sing the alphabet.", "prompt": PROMPT_PREFIX + "children singing together with musical notes and letters floating around."},
            {"title": "¡Yo sé el abecedario!", "footer": "I know the alphabet!", "prompt": PROMPT_PREFIX + "a proud child with a complete alphabet poster behind them, celebrating."},
        ],
        "vocab": [{"es":"abecedario","en":"alphabet","emoji":"📖"},{"es":"cantar","en":"sing","emoji":"🎤"},{"es":"letras","en":"letters","emoji":"🔤"},{"es":"aprender","en":"learn","emoji":"📚"},{"es":"eñe","en":"ñ letter","emoji":"🇪🇸"},{"es":"vocal","en":"vowel","emoji":"🅰️"}],
        "badge": {"emoji":"📖","name":"Rey del Abecedario","nameEn":"Alphabet King"}
    },
    {
        "slug": "week-95-contar", "title": "Contar", "subtitle": "Counting", "theme": "numeros", "week": 95, "emoji": "🔢",
        "meta_desc": "Learn to count in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, contar Spanish, counting Spanish kids",
        "pages": [
            {"title": "Contar", "footer": "Counting", "prompt": PROMPT_PREFIX + "numbers 1 through 5 in big colorful style with corresponding objects."},
            {"title": "Uno, dos, tres.", "footer": "One, two, three.", "prompt": PROMPT_PREFIX + "numbers 1 2 3 with one apple, two oranges, three bananas."},
            {"title": "Cuatro, cinco.", "footer": "Four, five.", "prompt": PROMPT_PREFIX + "numbers 4 5 with four flowers and five butterflies."},
            {"title": "Cuento mis juguetes.", "footer": "I count my toys.", "prompt": PROMPT_PREFIX + "a child counting colorful toys arranged in a line, pointing at each."},
            {"title": "Cuento las estrellas.", "footer": "I count the stars.", "prompt": PROMPT_PREFIX + "a child pointing at five numbered stars in the sky."},
            {"title": "Cuento los dedos.", "footer": "I count my fingers.", "prompt": PROMPT_PREFIX + "small hands with fingers extended, numbers floating above each finger."},
            {"title": "¡Yo sé contar!", "footer": "I know how to count!", "prompt": PROMPT_PREFIX + "a happy child surrounded by numbers 1 through 5 floating around."},
        ],
        "vocab": [{"es":"contar","en":"count","emoji":"🔢"},{"es":"juguetes","en":"toys","emoji":"🧸"},{"es":"dedos","en":"fingers","emoji":"🖐️"},{"es":"cuántos","en":"how many","emoji":"❓"},{"es":"más","en":"more","emoji":"➕"},{"es":"menos","en":"less","emoji":"➖"}],
        "badge": {"emoji":"🔢","name":"Contador Estrella","nameEn":"Star Counter"}
    },
    # MÚSICA (weeks 96-103)
    {
        "slug": "week-96-la-guitarra", "title": "La Guitarra", "subtitle": "The Guitar", "theme": "musica", "week": 96, "emoji": "🎸",
        "meta_desc": "Learn about the guitar in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, la guitarra Spanish, guitar Spanish kids",
        "pages": [
            {"title": "La Guitarra", "footer": "The Guitar", "prompt": PROMPT_PREFIX + "a beautiful acoustic guitar leaning against a chair in a cozy room."},
            {"title": "La guitarra tiene cuerdas.", "footer": "The guitar has strings.", "prompt": PROMPT_PREFIX + "close-up of guitar strings vibrating with musical notes floating."},
            {"title": "Yo toco la guitarra.", "footer": "I play the guitar.", "prompt": PROMPT_PREFIX + "a child happily strumming a small colorful guitar."},
            {"title": "La guitarra suena bonito.", "footer": "The guitar sounds pretty.", "prompt": PROMPT_PREFIX + "musical notes flowing from a guitar, colorful and magical."},
            {"title": "Canto con la guitarra.", "footer": "I sing with the guitar.", "prompt": PROMPT_PREFIX + "a child singing while someone plays guitar in a garden."},
            {"title": "La guitarra es de madera.", "footer": "The guitar is made of wood.", "prompt": PROMPT_PREFIX + "a warm wooden guitar with beautiful wood grain, close-up."},
            {"title": "¡Me encanta la guitarra!", "footer": "I love the guitar!", "prompt": PROMPT_PREFIX + "a child hugging a small guitar with musical notes and hearts around."},
        ],
        "vocab": [{"es":"guitarra","en":"guitar","emoji":"🎸"},{"es":"cuerdas","en":"strings","emoji":"🎵"},{"es":"toco","en":"I play","emoji":"🎶"},{"es":"suena","en":"sounds","emoji":"🔊"},{"es":"canto","en":"I sing","emoji":"🎤"},{"es":"madera","en":"wood","emoji":"🪵"}],
        "badge": {"emoji":"🎸","name":"Guitarrista Estrella","nameEn":"Star Guitarist"}
    },
    {
        "slug": "week-97-el-tambor", "title": "El Tambor", "subtitle": "The Drum", "theme": "musica", "week": 97, "emoji": "🥁",
        "meta_desc": "Learn about the drum in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el tambor Spanish, drum Spanish kids",
        "pages": [
            {"title": "El Tambor", "footer": "The Drum", "prompt": PROMPT_PREFIX + "a bright colorful drum with drumsticks on top, fun and inviting."},
            {"title": "El tambor hace ruido.", "footer": "The drum makes noise.", "prompt": PROMPT_PREFIX + "a drum being hit with sound waves and musical notes radiating out."},
            {"title": "Yo golpeo el tambor.", "footer": "I hit the drum.", "prompt": PROMPT_PREFIX + "a child happily hitting a colorful drum with drumsticks."},
            {"title": "Pum, pum, pum.", "footer": "Boom, boom, boom.", "prompt": PROMPT_PREFIX + "big colorful letters PUM PUM PUM bouncing off a drum."},
            {"title": "El tambor tiene ritmo.", "footer": "The drum has rhythm.", "prompt": PROMPT_PREFIX + "children marching in a parade with drums, happy and rhythmic."},
            {"title": "El tambor es redondo.", "footer": "The drum is round.", "prompt": PROMPT_PREFIX + "a round drum seen from above showing its circular shape."},
            {"title": "¡Me gusta el tambor!", "footer": "I like the drum!", "prompt": PROMPT_PREFIX + "a child with a big smile playing drums with confetti around."},
        ],
        "vocab": [{"es":"tambor","en":"drum","emoji":"🥁"},{"es":"ruido","en":"noise","emoji":"🔊"},{"es":"golpeo","en":"I hit","emoji":"💥"},{"es":"ritmo","en":"rhythm","emoji":"🎶"},{"es":"redondo","en":"round","emoji":"⭕"},{"es":"fuerte","en":"loud","emoji":"📢"}],
        "badge": {"emoji":"🥁","name":"Tamborilero Feliz","nameEn":"Happy Drummer"}
    },
    {
        "slug": "week-98-cantar", "title": "Cantar", "subtitle": "Singing", "theme": "musica", "week": 98, "emoji": "🎤",
        "meta_desc": "Learn about singing in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, cantar Spanish, singing Spanish kids",
        "pages": [
            {"title": "Cantar", "footer": "Singing", "prompt": PROMPT_PREFIX + "a child singing joyfully with musical notes floating around them."},
            {"title": "Yo canto una canción.", "footer": "I sing a song.", "prompt": PROMPT_PREFIX + "a child holding a microphone singing with colorful notes."},
            {"title": "Cantamos juntos.", "footer": "We sing together.", "prompt": PROMPT_PREFIX + "a group of children singing together in a circle, happy faces."},
            {"title": "La canción es alegre.", "footer": "The song is happy.", "prompt": PROMPT_PREFIX + "musical notes in bright colors dancing around a happy sun."},
            {"title": "Canto en la mañana.", "footer": "I sing in the morning.", "prompt": PROMPT_PREFIX + "a child singing by a window with morning sunshine coming in."},
            {"title": "Los pájaros cantan.", "footer": "The birds sing.", "prompt": PROMPT_PREFIX + "colorful birds on a branch singing with musical notes."},
            {"title": "¡Cantar es divertido!", "footer": "Singing is fun!", "prompt": PROMPT_PREFIX + "children on a stage singing and dancing with confetti falling."},
        ],
        "vocab": [{"es":"cantar","en":"sing","emoji":"🎤"},{"es":"canción","en":"song","emoji":"🎵"},{"es":"juntos","en":"together","emoji":"👥"},{"es":"alegre","en":"happy","emoji":"😊"},{"es":"mañana","en":"morning","emoji":"🌅"},{"es":"voz","en":"voice","emoji":"🗣️"}],
        "badge": {"emoji":"🎤","name":"Cantante Estrella","nameEn":"Star Singer"}
    },
    {
        "slug": "week-99-bailar", "title": "Bailar", "subtitle": "Dancing", "theme": "musica", "week": 99, "emoji": "💃",
        "meta_desc": "Learn about dancing in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, bailar Spanish, dancing Spanish kids",
        "pages": [
            {"title": "Bailar", "footer": "Dancing", "prompt": PROMPT_PREFIX + "a child dancing joyfully with colorful ribbons swirling around."},
            {"title": "Yo bailo.", "footer": "I dance.", "prompt": PROMPT_PREFIX + "a happy child spinning and dancing in a field of flowers."},
            {"title": "Bailamos juntos.", "footer": "We dance together.", "prompt": PROMPT_PREFIX + "children dancing in a circle holding hands in a park."},
            {"title": "Muevo mis manos.", "footer": "I move my hands.", "prompt": PROMPT_PREFIX + "a child waving hands gracefully while dancing, ribbons in hands."},
            {"title": "Muevo mis pies.", "footer": "I move my feet.", "prompt": PROMPT_PREFIX + "colorful dancing shoes tapping on a dance floor with sparkles."},
            {"title": "La música me hace bailar.", "footer": "Music makes me dance.", "prompt": PROMPT_PREFIX + "a child dancing next to a radio with musical notes flowing out."},
            {"title": "¡Bailar es divertido!", "footer": "Dancing is fun!", "prompt": PROMPT_PREFIX + "children at a dance party with disco lights and confetti."},
        ],
        "vocab": [{"es":"bailar","en":"dance","emoji":"💃"},{"es":"manos","en":"hands","emoji":"🙌"},{"es":"pies","en":"feet","emoji":"🦶"},{"es":"música","en":"music","emoji":"🎵"},{"es":"mover","en":"move","emoji":"🏃"},{"es":"juntos","en":"together","emoji":"👥"}],
        "badge": {"emoji":"💃","name":"Bailarín Estrella","nameEn":"Star Dancer"}
    },
    {
        "slug": "week-100-el-piano", "title": "El Piano", "subtitle": "The Piano", "theme": "musica", "week": 100, "emoji": "🎹",
        "meta_desc": "Learn about the piano in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, el piano Spanish, piano Spanish kids",
        "pages": [
            {"title": "El Piano", "footer": "The Piano", "prompt": PROMPT_PREFIX + "a beautiful grand piano in a sunlit room with flowers nearby."},
            {"title": "El piano tiene teclas.", "footer": "The piano has keys.", "prompt": PROMPT_PREFIX + "close-up of black and white piano keys with gentle light."},
            {"title": "Las teclas son blancas y negras.", "footer": "The keys are white and black.", "prompt": PROMPT_PREFIX + "alternating black and white piano keys with colorful notes floating."},
            {"title": "Yo toco el piano.", "footer": "I play the piano.", "prompt": PROMPT_PREFIX + "a child sitting at a piano playing with small hands on keys."},
            {"title": "El piano suena dulce.", "footer": "The piano sounds sweet.", "prompt": PROMPT_PREFIX + "musical notes flowing from a piano like a gentle river of colors."},
            {"title": "Practico todos los días.", "footer": "I practice every day.", "prompt": PROMPT_PREFIX + "a child practicing piano with a happy expression, music book open."},
            {"title": "¡Me encanta el piano!", "footer": "I love the piano!", "prompt": PROMPT_PREFIX + "a child taking a bow after playing piano with family clapping."},
        ],
        "vocab": [{"es":"piano","en":"piano","emoji":"🎹"},{"es":"teclas","en":"keys","emoji":"⬜"},{"es":"blancas","en":"white","emoji":"⬜"},{"es":"negras","en":"black","emoji":"⬛"},{"es":"toco","en":"I play","emoji":"🎶"},{"es":"dulce","en":"sweet","emoji":"🍬"}],
        "badge": {"emoji":"🎹","name":"Pianista Brillante","nameEn":"Brilliant Pianist"}
    },
    {
        "slug": "week-101-la-flauta", "title": "La Flauta", "subtitle": "The Flute", "theme": "musica", "week": 101, "emoji": "🪈",
        "meta_desc": "Learn about the flute in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, la flauta Spanish, flute Spanish kids",
        "pages": [
            {"title": "La Flauta", "footer": "The Flute", "prompt": PROMPT_PREFIX + "a shiny silver flute on a velvet cloth with flowers around it."},
            {"title": "La flauta es larga.", "footer": "The flute is long.", "prompt": PROMPT_PREFIX + "a long silver flute being held horizontally by a child."},
            {"title": "Yo soplo la flauta.", "footer": "I blow the flute.", "prompt": PROMPT_PREFIX + "a child gently blowing into a recorder flute with notes coming out."},
            {"title": "La flauta suena suave.", "footer": "The flute sounds soft.", "prompt": PROMPT_PREFIX + "gentle pastel musical notes floating from a flute like butterflies."},
            {"title": "Los pájaros escuchan.", "footer": "The birds listen.", "prompt": PROMPT_PREFIX + "birds perched on branches listening to a child playing flute in a garden."},
            {"title": "Toco en el jardín.", "footer": "I play in the garden.", "prompt": PROMPT_PREFIX + "a child playing flute in a beautiful garden with flowers swaying."},
            {"title": "¡La flauta es mágica!", "footer": "The flute is magical!", "prompt": PROMPT_PREFIX + "a child playing flute with magical sparkles and butterflies appearing."},
        ],
        "vocab": [{"es":"flauta","en":"flute","emoji":"🪈"},{"es":"larga","en":"long","emoji":"📏"},{"es":"soplo","en":"I blow","emoji":"💨"},{"es":"suave","en":"soft","emoji":"🤫"},{"es":"escuchan","en":"listen","emoji":"👂"},{"es":"mágica","en":"magical","emoji":"✨"}],
        "badge": {"emoji":"🪈","name":"Flautista Mágico","nameEn":"Magical Flutist"}
    },
    {
        "slug": "week-102-la-musica", "title": "La Música", "subtitle": "Music", "theme": "musica", "week": 102, "emoji": "🎵",
        "meta_desc": "Learn about music in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, la música Spanish, music Spanish kids",
        "pages": [
            {"title": "La Música", "footer": "Music", "prompt": PROMPT_PREFIX + "colorful musical notes and instruments floating in a magical scene."},
            {"title": "La música es alegre.", "footer": "Music is happy.", "prompt": PROMPT_PREFIX + "smiling children surrounded by floating colorful musical notes."},
            {"title": "La música nos une.", "footer": "Music brings us together.", "prompt": PROMPT_PREFIX + "diverse children playing different instruments together in a circle."},
            {"title": "Hay muchos instrumentos.", "footer": "There are many instruments.", "prompt": PROMPT_PREFIX + "various colorful instruments: guitar, drum, piano, flute arranged together."},
            {"title": "La música está en todos lados.", "footer": "Music is everywhere.", "prompt": PROMPT_PREFIX + "musical notes flowing through nature: birds, wind, water, all making music."},
            {"title": "Yo hago música.", "footer": "I make music.", "prompt": PROMPT_PREFIX + "a child happily playing with various simple instruments, maracas and tambourine."},
            {"title": "¡Viva la música!", "footer": "Long live music!", "prompt": PROMPT_PREFIX + "a joyful celebration with children dancing and playing instruments, confetti."},
        ],
        "vocab": [{"es":"música","en":"music","emoji":"🎵"},{"es":"alegre","en":"happy","emoji":"😊"},{"es":"instrumentos","en":"instruments","emoji":"🎺"},{"es":"escuchar","en":"listen","emoji":"👂"},{"es":"cantar","en":"sing","emoji":"🎤"},{"es":"bailar","en":"dance","emoji":"💃"}],
        "badge": {"emoji":"🎵","name":"Músico Estrella","nameEn":"Star Musician"}
    },
    {
        "slug": "week-103-los-juegos", "title": "Los Juegos", "subtitle": "Games", "theme": "musica", "week": 103, "emoji": "🎮",
        "meta_desc": "Learn about games in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, los juegos Spanish, games Spanish kids",
        "pages": [
            {"title": "Los Juegos", "footer": "Games", "prompt": PROMPT_PREFIX + "colorful board games, balls, and toys arranged on a playroom floor."},
            {"title": "Me gusta jugar.", "footer": "I like to play.", "prompt": PROMPT_PREFIX + "a happy child surrounded by various fun games and toys."},
            {"title": "Jugamos a la pelota.", "footer": "We play ball.", "prompt": PROMPT_PREFIX + "children kicking a colorful ball in a green field."},
            {"title": "Jugamos a escondernos.", "footer": "We play hide and seek.", "prompt": PROMPT_PREFIX + "a child hiding behind a tree while another counts, in a park."},
            {"title": "Los bloques son divertidos.", "footer": "Blocks are fun.", "prompt": PROMPT_PREFIX + "a child building a tall tower with colorful wooden blocks."},
            {"title": "Jugamos con amigos.", "footer": "We play with friends.", "prompt": PROMPT_PREFIX + "a group of children playing a board game together, laughing."},
            {"title": "¡Jugar es lo mejor!", "footer": "Playing is the best!", "prompt": PROMPT_PREFIX + "children celebrating and jumping with joy surrounded by games and toys."},
        ],
        "vocab": [{"es":"juegos","en":"games","emoji":"🎮"},{"es":"jugar","en":"play","emoji":"⚽"},{"es":"pelota","en":"ball","emoji":"🏐"},{"es":"bloques","en":"blocks","emoji":"🧱"},{"es":"amigos","en":"friends","emoji":"👫"},{"es":"divertido","en":"fun","emoji":"🎉"}],
        "badge": {"emoji":"🎮","name":"Campeón de Juegos","nameEn":"Game Champion"}
    },
    # MI MUNDO (weeks 104-111)
    {
        "slug": "week-104-mi-casa", "title": "Mi Casa", "subtitle": "My House", "theme": "mi-mundo", "week": 104, "emoji": "🏠",
        "meta_desc": "Learn about the house in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, mi casa Spanish, house Spanish kids",
        "pages": [
            {"title": "Mi Casa", "footer": "My House", "prompt": PROMPT_PREFIX + "a cozy colorful house with a red roof, garden, and welcoming front door."},
            {"title": "Mi casa es bonita.", "footer": "My house is pretty.", "prompt": PROMPT_PREFIX + "a charming house with flowers in the windows and a white fence."},
            {"title": "Tiene una puerta.", "footer": "It has a door.", "prompt": PROMPT_PREFIX + "a friendly colorful front door of a house with a welcome mat."},
            {"title": "Tiene ventanas.", "footer": "It has windows.", "prompt": PROMPT_PREFIX + "cute windows with curtains and flower boxes on a house wall."},
            {"title": "Mi cuarto es aquí.", "footer": "My room is here.", "prompt": PROMPT_PREFIX + "a cozy child's bedroom with colorful toys, bed, and a nightlight."},
            {"title": "La cocina huele rico.", "footer": "The kitchen smells good.", "prompt": PROMPT_PREFIX + "a warm kitchen with someone cooking, steam rising from a pot."},
            {"title": "¡Me gusta mi casa!", "footer": "I like my house!", "prompt": PROMPT_PREFIX + "a happy family standing in front of their cozy house, waving."},
        ],
        "vocab": [{"es":"casa","en":"house","emoji":"🏠"},{"es":"puerta","en":"door","emoji":"🚪"},{"es":"ventana","en":"window","emoji":"🪟"},{"es":"cuarto","en":"room","emoji":"🛏️"},{"es":"cocina","en":"kitchen","emoji":"🍳"},{"es":"bonita","en":"pretty","emoji":"🌸"}],
        "badge": {"emoji":"🏠","name":"Constructor de Casas","nameEn":"House Builder"}
    },
    {
        "slug": "week-105-mi-escuela", "title": "Mi Escuela", "subtitle": "My School", "theme": "mi-mundo", "week": 105, "emoji": "🏫",
        "meta_desc": "Learn about school in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, mi escuela Spanish, school Spanish kids",
        "pages": [
            {"title": "Mi Escuela", "footer": "My School", "prompt": PROMPT_PREFIX + "a cheerful school building with a playground and children arriving."},
            {"title": "Voy a la escuela.", "footer": "I go to school.", "prompt": PROMPT_PREFIX + "a child walking to school with a backpack, waving to friends."},
            {"title": "Mi maestra es amable.", "footer": "My teacher is kind.", "prompt": PROMPT_PREFIX + "a kind teacher reading a book to children sitting in a circle."},
            {"title": "Aprendo muchas cosas.", "footer": "I learn many things.", "prompt": PROMPT_PREFIX + "a child at a desk with books, crayons, and a globe, learning."},
            {"title": "Juego en el recreo.", "footer": "I play at recess.", "prompt": PROMPT_PREFIX + "children playing on a playground with slides and swings at recess."},
            {"title": "Tengo muchos amigos.", "footer": "I have many friends.", "prompt": PROMPT_PREFIX + "diverse children smiling together in a classroom, friends."},
            {"title": "¡Me gusta mi escuela!", "footer": "I like my school!", "prompt": PROMPT_PREFIX + "a happy child at school entrance giving a thumbs up."},
        ],
        "vocab": [{"es":"escuela","en":"school","emoji":"🏫"},{"es":"maestra","en":"teacher","emoji":"👩‍🏫"},{"es":"aprendo","en":"I learn","emoji":"📚"},{"es":"recreo","en":"recess","emoji":"⛹️"},{"es":"amigos","en":"friends","emoji":"👫"},{"es":"libros","en":"books","emoji":"📖"}],
        "badge": {"emoji":"🏫","name":"Estudiante Estrella","nameEn":"Star Student"}
    },
    {
        "slug": "week-106-mi-parque", "title": "Mi Parque", "subtitle": "My Park", "theme": "mi-mundo", "week": 106, "emoji": "🛝",
        "meta_desc": "Learn about the park in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, mi parque Spanish, park Spanish kids",
        "pages": [
            {"title": "Mi Parque", "footer": "My Park", "prompt": PROMPT_PREFIX + "a beautiful park with green trees, playground, and children playing."},
            {"title": "Voy al parque.", "footer": "I go to the park.", "prompt": PROMPT_PREFIX + "a child skipping happily toward a park entrance with trees."},
            {"title": "Hay un columpio.", "footer": "There is a swing.", "prompt": PROMPT_PREFIX + "a colorful swing set with a child swinging high in the air."},
            {"title": "Hay una resbaladilla.", "footer": "There is a slide.", "prompt": PROMPT_PREFIX + "a child sliding down a colorful slide with a big smile."},
            {"title": "Corro en el pasto.", "footer": "I run on the grass.", "prompt": PROMPT_PREFIX + "a child running freely on green grass in the park with butterflies."},
            {"title": "Veo las flores.", "footer": "I see the flowers.", "prompt": PROMPT_PREFIX + "a child bending down to smell colorful flowers in the park."},
            {"title": "¡El parque es genial!", "footer": "The park is great!", "prompt": PROMPT_PREFIX + "children playing together in a sunny park with a rainbow."},
        ],
        "vocab": [{"es":"parque","en":"park","emoji":"🛝"},{"es":"columpio","en":"swing","emoji":"🎠"},{"es":"resbaladilla","en":"slide","emoji":"🛝"},{"es":"pasto","en":"grass","emoji":"🌿"},{"es":"corro","en":"I run","emoji":"🏃"},{"es":"flores","en":"flowers","emoji":"🌺"}],
        "badge": {"emoji":"🛝","name":"Rey del Parque","nameEn":"Park King"}
    },
    {
        "slug": "week-107-mi-jardin", "title": "Mi Jardín", "subtitle": "My Garden", "theme": "mi-mundo", "week": 107, "emoji": "🌻",
        "meta_desc": "Learn about the garden in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, mi jardín Spanish, garden Spanish kids",
        "pages": [
            {"title": "Mi Jardín", "footer": "My Garden", "prompt": PROMPT_PREFIX + "a beautiful garden with colorful flowers, vegetables, and a small fence."},
            {"title": "Yo siembro semillas.", "footer": "I plant seeds.", "prompt": PROMPT_PREFIX + "a child planting seeds in soil with small gardening tools."},
            {"title": "Las plantas crecen.", "footer": "The plants grow.", "prompt": PROMPT_PREFIX + "small green sprouts growing from the soil in a garden bed."},
            {"title": "Riego las flores.", "footer": "I water the flowers.", "prompt": PROMPT_PREFIX + "a child watering flowers with a small watering can, water sparkling."},
            {"title": "Las mariposas vienen.", "footer": "The butterflies come.", "prompt": PROMPT_PREFIX + "colorful butterflies visiting flowers in a sunny garden."},
            {"title": "Hay tomates rojos.", "footer": "There are red tomatoes.", "prompt": PROMPT_PREFIX + "ripe red tomatoes growing on a vine in a garden."},
            {"title": "¡Mi jardín es hermoso!", "footer": "My garden is beautiful!", "prompt": PROMPT_PREFIX + "a child standing proudly in a blooming colorful garden."},
        ],
        "vocab": [{"es":"jardín","en":"garden","emoji":"🌻"},{"es":"semillas","en":"seeds","emoji":"🌱"},{"es":"plantas","en":"plants","emoji":"🌿"},{"es":"riego","en":"I water","emoji":"💧"},{"es":"mariposas","en":"butterflies","emoji":"🦋"},{"es":"tomates","en":"tomatoes","emoji":"🍅"}],
        "badge": {"emoji":"🌻","name":"Jardinero Feliz","nameEn":"Happy Gardener"}
    },
    {
        "slug": "week-108-mi-tienda", "title": "Mi Tienda", "subtitle": "My Store", "theme": "mi-mundo", "week": 108, "emoji": "🏪",
        "meta_desc": "Learn about the store in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, mi tienda Spanish, store Spanish kids",
        "pages": [
            {"title": "Mi Tienda", "footer": "My Store", "prompt": PROMPT_PREFIX + "a friendly neighborhood store with a colorful awning and fruits displayed."},
            {"title": "Vamos a la tienda.", "footer": "Let's go to the store.", "prompt": PROMPT_PREFIX + "a parent and child walking toward a cute neighborhood store."},
            {"title": "Hay frutas frescas.", "footer": "There are fresh fruits.", "prompt": PROMPT_PREFIX + "colorful fresh fruits arranged beautifully on store shelves."},
            {"title": "Hay pan caliente.", "footer": "There is warm bread.", "prompt": PROMPT_PREFIX + "a bakery section with warm golden bread loaves on display."},
            {"title": "Yo escojo una manzana.", "footer": "I choose an apple.", "prompt": PROMPT_PREFIX + "a child reaching for a red apple from a fruit display in a store."},
            {"title": "Pagamos en la caja.", "footer": "We pay at the register.", "prompt": PROMPT_PREFIX + "a friendly cashier at a register with a child watching."},
            {"title": "¡Me gusta la tienda!", "footer": "I like the store!", "prompt": PROMPT_PREFIX + "a happy child leaving the store with a small grocery bag."},
        ],
        "vocab": [{"es":"tienda","en":"store","emoji":"🏪"},{"es":"frutas","en":"fruits","emoji":"🍎"},{"es":"pan","en":"bread","emoji":"🍞"},{"es":"escojo","en":"I choose","emoji":"👆"},{"es":"pagamos","en":"we pay","emoji":"💰"},{"es":"bolsa","en":"bag","emoji":"🛍️"}],
        "badge": {"emoji":"🏪","name":"Comprador Estrella","nameEn":"Star Shopper"}
    },
    {
        "slug": "week-109-mi-biblioteca", "title": "Mi Biblioteca", "subtitle": "My Library", "theme": "mi-mundo", "week": 109, "emoji": "📚",
        "meta_desc": "Learn about the library in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, mi biblioteca Spanish, library Spanish kids",
        "pages": [
            {"title": "Mi Biblioteca", "footer": "My Library", "prompt": PROMPT_PREFIX + "a cozy library with tall bookshelves and comfortable reading nooks."},
            {"title": "Hay muchos libros.", "footer": "There are many books.", "prompt": PROMPT_PREFIX + "colorful books arranged on library shelves, all different sizes."},
            {"title": "Yo leo un cuento.", "footer": "I read a story.", "prompt": PROMPT_PREFIX + "a child sitting in a cozy chair reading a picture book."},
            {"title": "Los libros son mágicos.", "footer": "Books are magical.", "prompt": PROMPT_PREFIX + "an open book with magical scenes rising from its pages, sparkles."},
            {"title": "Leo con mi mamá.", "footer": "I read with my mom.", "prompt": PROMPT_PREFIX + "a mother and child reading together on a cozy library couch."},
            {"title": "Escojo mi libro.", "footer": "I choose my book.", "prompt": PROMPT_PREFIX + "a child reaching for a book on a low library shelf."},
            {"title": "¡Me encantan los libros!", "footer": "I love books!", "prompt": PROMPT_PREFIX + "a happy child hugging a stack of colorful books in a library."},
        ],
        "vocab": [{"es":"biblioteca","en":"library","emoji":"📚"},{"es":"libros","en":"books","emoji":"📖"},{"es":"leo","en":"I read","emoji":"👀"},{"es":"cuento","en":"story","emoji":"📕"},{"es":"mágicos","en":"magical","emoji":"✨"},{"es":"escojo","en":"I choose","emoji":"👆"}],
        "badge": {"emoji":"📚","name":"Ratón de Biblioteca","nameEn":"Bookworm"}
    },
    {
        "slug": "week-110-mi-iglesia", "title": "Mi Iglesia", "subtitle": "My Church", "theme": "mi-mundo", "week": 110, "emoji": "⛪",
        "meta_desc": "Learn about the church in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, mi iglesia Spanish, church Spanish kids",
        "pages": [
            {"title": "Mi Iglesia", "footer": "My Church", "prompt": PROMPT_PREFIX + "a pretty church building with a bell tower, stained glass, and garden."},
            {"title": "Vamos a la iglesia.", "footer": "We go to church.", "prompt": PROMPT_PREFIX + "a family walking together toward a welcoming church on a sunny day."},
            {"title": "La iglesia es grande.", "footer": "The church is big.", "prompt": PROMPT_PREFIX + "a large friendly church building with tall doors and a cross on top."},
            {"title": "Cantamos canciones.", "footer": "We sing songs.", "prompt": PROMPT_PREFIX + "people singing together in a church with musical notes floating."},
            {"title": "Escuchamos historias.", "footer": "We listen to stories.", "prompt": PROMPT_PREFIX + "children sitting and listening to a story being told in church."},
            {"title": "Somos amables.", "footer": "We are kind.", "prompt": PROMPT_PREFIX + "children sharing and being kind to each other outside a church."},
            {"title": "¡Me gusta mi iglesia!", "footer": "I like my church!", "prompt": PROMPT_PREFIX + "a child waving happily in front of a pretty church with a garden."},
        ],
        "vocab": [{"es":"iglesia","en":"church","emoji":"⛪"},{"es":"cantamos","en":"we sing","emoji":"🎶"},{"es":"historias","en":"stories","emoji":"📖"},{"es":"amables","en":"kind","emoji":"💕"},{"es":"familia","en":"family","emoji":"👨‍👩‍👧"},{"es":"campana","en":"bell","emoji":"🔔"}],
        "badge": {"emoji":"⛪","name":"Corazón Bondadoso","nameEn":"Kind Heart"}
    },
    {
        "slug": "week-111-mi-ciudad", "title": "Mi Ciudad", "subtitle": "My City", "theme": "mi-mundo", "week": 111, "emoji": "🏙️",
        "meta_desc": "Learn about the city in Spanish with audio pronunciation. Ages 2-5.",
        "keywords": "learn Spanish preschool, mi ciudad Spanish, city Spanish kids",
        "pages": [
            {"title": "Mi Ciudad", "footer": "My City", "prompt": PROMPT_PREFIX + "a friendly colorful city with buildings, trees, and people walking."},
            {"title": "La ciudad tiene edificios.", "footer": "The city has buildings.", "prompt": PROMPT_PREFIX + "tall colorful buildings in a city with blue sky above."},
            {"title": "Hay carros y autobuses.", "footer": "There are cars and buses.", "prompt": PROMPT_PREFIX + "colorful cars and a bus on a city street with a crosswalk."},
            {"title": "La gente camina.", "footer": "People walk.", "prompt": PROMPT_PREFIX + "friendly people walking on a city sidewalk with shops and trees."},
            {"title": "Hay un parque en la ciudad.", "footer": "There is a park in the city.", "prompt": PROMPT_PREFIX + "a green park in the middle of a city with children playing."},
            {"title": "Las luces brillan de noche.", "footer": "The lights shine at night.", "prompt": PROMPT_PREFIX + "a city at night with warm glowing lights from windows and street lamps."},
            {"title": "¡Mi ciudad es hermosa!", "footer": "My city is beautiful!", "prompt": PROMPT_PREFIX + "a panoramic view of a beautiful colorful city at sunset."},
        ],
        "vocab": [{"es":"ciudad","en":"city","emoji":"🏙️"},{"es":"edificios","en":"buildings","emoji":"🏢"},{"es":"carros","en":"cars","emoji":"🚗"},{"es":"gente","en":"people","emoji":"👥"},{"es":"parque","en":"park","emoji":"🌳"},{"es":"luces","en":"lights","emoji":"💡"}],
        "badge": {"emoji":"🏙️","name":"Explorador Urbano","nameEn":"Urban Explorer"}
    },
]

# Write each config
for book in books:
    path = os.path.join(CONFIGS_DIR, f"{book['slug'].split('-', 2)[2]}.json")
    with open(path, 'w') as f:
        json.dump(book, f, ensure_ascii=False, indent=2)
    print(f"Created {path}")
