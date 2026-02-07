/**
 * Week 22: Los Amigos (Friends)
 * Theme: Friendship and Kindness
 * Target Age: 2-5 years
 * Monthly Theme: February - El Amor (Love)
 */

const BOOK_CONFIG = {
  id: "week-22-los-amigos",
  title: "Los Amigos",
  subtitle: "Friends",
  language: "es",
  weekNumber: 22,
  monthlyTheme: "February: El Amor (Love)",
  targetAge: "2-5",
  vocabularyCount: 7,
  pageCount: 10,
  
  seoKeywords: [
    "spanish preschool books",
    "learn friends spanish",
    "friendship vocabulary spanish",
    "free spanish books kids",
    "amigos español niños",
    "montessori spanish",
    "phoenix bilingual preschool",
    "kindness spanish preschool",
    "spanish emotions kids"
  ],
  
  pages: [
    // Page 1: Title Page
    {
      pageNumber: 1,
      type: "title",
      text: "<h1>Los Amigos</h1><p class='subtitle'>Friends</p><p class='theme'>Week 22 • February: Love</p>",
      imagePrompt: "Two happy diverse preschool children holding hands and smiling, bright sunny background, cartoon style, cheerful, friendship theme, colorful, suitable for ages 2-5",
      image: "images/page-01-cover.webp",
      audioText: "Los Amigos",
      vocabulary: null
    },
    
    // Page 2: amigo (friend)
    {
      pageNumber: 2,
      vocabulary: "amigo",
      translation: "friend",
      sentence: "Este es mi <span class='word-highlight'>amigo</span>.",
      englishTranslation: "This is my friend.",
      imagePrompt: "Two smiling preschool children (one boy, one girl) waving hello, diverse, colorful clothing, playground background, cartoon style, bright and cheerful, suitable for preschoolers",
      image: "images/page-02-amigo.webp",
      audioText: "Este es mi amigo"
    },
    
    // Page 3: jugar (to play)
    {
      pageNumber: 3,
      vocabulary: "jugar",
      translation: "to play",
      sentence: "Me gusta <span class='word-highlight'>jugar</span> con mis amigos.",
      englishTranslation: "I like to play with my friends.",
      imagePrompt: "Three diverse preschool children playing with colorful building blocks together, laughing and happy, indoor classroom setting, cartoon style, bright colors, playful atmosphere, ages 2-5",
      image: "images/page-03-jugar.webp",
      audioText: "Me gusta jugar con mis amigos"
    },
    
    // Page 4: compartir (to share)
    {
      pageNumber: 4,
      vocabulary: "compartir",
      translation: "to share",
      sentence: "Voy a <span class='word-highlight'>compartir</span> mi juguete.",
      englishTranslation: "I am going to share my toy.",
      imagePrompt: "Two preschool children sharing a colorful toy car, both smiling and reaching for it gently, bright background, cartoon style, positive interaction, kindness theme, suitable for ages 2-5",
      image: "images/page-04-compartir.webp",
      audioText: "Voy a compartir mi juguete"
    },
    
    // Page 5: ayudar (to help)
    {
      pageNumber: 5,
      vocabulary: "ayudar",
      translation: "to help",
      sentence: "Me gusta <span class='word-highlight'>ayudar</span> a mis amigos.",
      englishTranslation: "I like to help my friends.",
      imagePrompt: "One preschool child helping another child tie their shoe, both smiling, outdoor playground setting, cartoon style, bright cheerful colors, helpful gesture, suitable for preschoolers",
      image: "images/page-05-ayudar.webp",
      audioText: "Me gusta ayudar a mis amigos"
    },
    
    // Page 6: reír (to laugh)
    {
      pageNumber: 6,
      vocabulary: "reír",
      translation: "to laugh",
      sentence: "Nos gusta <span class='word-highlight'>reír</span> juntos.",
      englishTranslation: "We like to laugh together.",
      imagePrompt: "Three diverse preschool children laughing together, mouths open in big smiles, holding their bellies, colorful background with stars and sparkles, cartoon style, joyful and fun, ages 2-5",
      image: "images/page-06-reir.webp",
      audioText: "Nos gusta reír juntos"
    },
    
    // Page 7: abrazar (to hug)
    {
      pageNumber: 7,
      vocabulary: "abrazar",
      translation: "to hug",
      sentence: "Voy a <span class='word-highlight'>abrazar</span> a mi amigo.",
      englishTranslation: "I am going to hug my friend.",
      imagePrompt: "Two preschool children giving each other a warm hug, big smiles, hearts floating around them, soft pastel background, cartoon style, loving and gentle, suitable for ages 2-5",
      image: "images/page-07-abrazar.webp",
      audioText: "Voy a abrazar a mi amigo"
    },
    
    // Page 8: gentil (kind/gentle)
    {
      pageNumber: 8,
      vocabulary: "gentil",
      translation: "kind, gentle",
      sentence: "Soy <span class='word-highlight'>gentil</span> con mis amigos.",
      englishTranslation: "I am kind with my friends.",
      imagePrompt: "A preschool child gently petting a small bunny while another child watches with a smile, soft colors, peaceful setting, cartoon style, gentle and caring theme, suitable for ages 2-5",
      image: "images/page-08-gentil.webp",
      audioText: "Soy gentil con mis amigos"
    },
    
    // Page 9: Review/Celebration
    {
      pageNumber: 9,
      type: "review",
      vocabulary: "todos",
      translation: "everyone",
      sentence: "¡<span class='word-highlight'>Todos</span> somos amigos!",
      englishTranslation: "We are all friends!",
      imagePrompt: "Group of five diverse preschool children holding hands in a circle, all smiling and happy, rainbow in background, celebration theme, cartoon style, colorful and joyful, ages 2-5",
      image: "images/page-09-todos.webp",
      audioText: "Todos somos amigos"
    },
    
    // Page 10: The End + CTAs
    {
      pageNumber: 10,
      type: "end",
      text: `
        <h2>¡Fin!</h2>
        <p class='subtitle'>The End</p>
        <div class="end-message">
          <p>🤝 ¡Eres un gran amigo!</p>
          <p class="english">You are a great friend!</p>
        </div>
      `,
      imagePrompt: "The word 'FIN' in large colorful letters with happy children silhouettes around it, confetti and celebration elements, bright and cheerful, cartoon style, suitable for preschoolers",
      image: "images/page-10-end.webp",
      audioText: "Fin. Eres un gran amigo",
      ctas: true
    }
  ]
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BOOK_CONFIG;
}
