/**
 * Week 23: El Corazón (The Heart)
 * Theme: Love and Caring
 * Target Age: 2-5 years
 * Monthly Theme: February - El Amor (Love)
 */

const BOOK_CONFIG = {
  id: "week-23-el-corazon",
  title: "El Corazón",
  subtitle: "The Heart",
  language: "es",
  weekNumber: 23,
  monthlyTheme: "February: El Amor (Love)",
  targetAge: "2-5",
  vocabularyCount: 7,
  pageCount: 10,
  
  seoKeywords: [
    "spanish preschool books",
    "learn love spanish",
    "heart vocabulary spanish",
    "free spanish books kids",
    "corazón español niños",
    "montessori spanish",
    "phoenix bilingual preschool",
    "family spanish preschool",
    "spanish emotions kids",
    "valentine spanish preschool"
  ],
  
  pages: [
    // Page 1: Title Page
    {
      pageNumber: 1,
      type: "title",
      text: "<h1>El Corazón</h1><p class='subtitle'>The Heart</p><p class='theme'>Week 23 • February: Love</p>",
      imagePrompt: "A large bright red heart surrounded by smaller pink and red hearts, sparkles and stars, soft glowing background, cartoon style, cheerful and loving, suitable for ages 2-5",
      image: "images/page-01-cover.webp",
      audioText: "El Corazón",
      vocabulary: null
    },
    
    // Page 2: corazón (heart)
    {
      pageNumber: 2,
      vocabulary: "corazón",
      translation: "heart",
      sentence: "Mi <span class='word-highlight'>corazón</span> es rojo.",
      englishTranslation: "My heart is red.",
      imagePrompt: "A large bright red cartoon heart with a happy smiling face, sparkles around it, white background, simple and clear, cheerful, suitable for preschoolers ages 2-5",
      image: "images/page-02-corazon.webp",
      audioText: "Mi corazón es rojo"
    },
    
    // Page 3: amar (to love)
    {
      pageNumber: 3,
      vocabulary: "amar",
      translation: "to love",
      sentence: "Yo <span class='word-highlight'>amo</span> a mi familia.",
      englishTranslation: "I love my family.",
      imagePrompt: "Happy diverse family of four (mom, dad, two children) standing together with hearts floating around them, warm colors, cartoon style, loving and cheerful, suitable for ages 2-5",
      image: "images/page-03-amar.webp",
      audioText: "Yo amo a mi familia"
    },
    
    // Page 4: cuidar (to care for)
    {
      pageNumber: 4,
      vocabulary: "cuidar",
      translation: "to care for",
      sentence: "Me gusta <span class='word-highlight'>cuidar</span> a mi hermanito.",
      englishTranslation: "I like to care for my little brother.",
      imagePrompt: "Older preschool child gently helping younger sibling with toy, both smiling, soft colors, hearts in background, cartoon style, caring and gentle, suitable for ages 2-5",
      image: "images/page-04-cuidar.webp",
      audioText: "Me gusta cuidar a mi hermanito"
    },
    
    // Page 5: familia (family)
    {
      pageNumber: 5,
      vocabulary: "familia",
      translation: "family",
      sentence: "Mi <span class='word-highlight'>familia</span> es especial.",
      englishTranslation: "My family is special.",
      imagePrompt: "Diverse multi-generational family portrait including grandparents, parents, and children, all smiling warmly, colorful clothing, hearts decorating the border, cartoon style, loving atmosphere, ages 2-5",
      image: "images/page-05-familia.webp",
      audioText: "Mi familia es especial"
    },
    
    // Page 6: beso (kiss)
    {
      pageNumber: 6,
      vocabulary: "beso",
      translation: "kiss",
      sentence: "Mamá me da un <span class='word-highlight'>beso</span>.",
      englishTranslation: "Mom gives me a kiss.",
      imagePrompt: "Loving mother giving a gentle kiss on the cheek to her smiling preschool child, hearts floating around them, soft warm colors, cartoon style, tender moment, suitable for ages 2-5",
      image: "images/page-06-beso.webp",
      audioText: "Mamá me da un beso"
    },
    
    // Page 7: abrazo (hug)
    {
      pageNumber: 7,
      vocabulary: "abrazo",
      translation: "hug",
      sentence: "Un <span class='word-highlight'>abrazo</span> es cálido.",
      englishTranslation: "A hug is warm.",
      imagePrompt: "Two preschool children giving each other a warm, tight hug with big smiles, hearts all around them, warm yellow and pink background, cartoon style, loving and cozy, suitable for ages 2-5",
      image: "images/page-07-abrazo.webp",
      audioText: "Un abrazo es cálido"
    },
    
    // Page 8: rojo (red)
    {
      pageNumber: 8,
      vocabulary: "rojo",
      translation: "red",
      sentence: "El corazón es <span class='word-highlight'>rojo</span>.",
      englishTranslation: "The heart is red.",
      imagePrompt: "Multiple red hearts of different sizes floating on a white background, bright red color, simple and clear, cartoon style, cheerful, suitable for preschoolers ages 2-5",
      image: "images/page-08-rojo.webp",
      audioText: "El corazón es rojo"
    },
    
    // Page 9: Review/Celebration
    {
      pageNumber: 9,
      type: "review",
      vocabulary: "amor",
      translation: "love",
      sentence: "¡El <span class='word-highlight'>amor</span> es hermoso!",
      englishTranslation: "Love is beautiful!",
      imagePrompt: "Large glowing heart in center with family, friends, and children holding hands around it in a circle, rainbow colors, stars and sparkles, celebration theme, cartoon style, joyful and loving, ages 2-5",
      image: "images/page-09-amor.webp",
      audioText: "El amor es hermoso"
    },
    
    // Page 10: The End + CTAs
    {
      pageNumber: 10,
      type: "end",
      text: `
        <h2>¡Fin!</h2>
        <p class='subtitle'>The End</p>
        <div class="end-message">
          <p>❤️ ¡Te amo mucho!</p>
          <p class="english">I love you so much!</p>
        </div>
      `,
      imagePrompt: "The word 'FIN' in large colorful letters surrounded by red and pink hearts, sparkles and stars, bright cheerful background, cartoon style, suitable for preschoolers",
      image: "images/page-10-end.webp",
      audioText: "Fin. Te amo mucho",
      ctas: true
    }
  ]
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BOOK_CONFIG;
}
