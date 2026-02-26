const bookConfig = {
    week: 24,
    title: "La Lluvia y el Sol",
    titleEnglish: "The Rain and the Sun",
    topic: "Weather / El Clima",
    targetAge: "2-5 years",
    pages: 8,
    learningObjectives: [
        "Weather vocabulary in Spanish",
        "Understanding rain and sun cycle",
        "Basic nature observation",
        "Sequencing (before/after concept)"
    ],
    vocabulary: [
        { spanish: "el cielo", english: "the sky", pronunciation: "SYEH-loh" },
        { spanish: "las nubes", english: "the clouds", pronunciation: "NOO-bes" },
        { spanish: "la lluvia", english: "the rain", pronunciation: "lah YOO-vee-ah" },
        { spanish: "el paraguas", english: "the umbrella", pronunciation: "pah-rah-GWAS" },
        { spanish: "los charcos", english: "the puddles", pronunciation: "CHAR-kohs" },
        { spanish: "el sol", english: "the sun", pronunciation: "el sohl" },
        { spanish: "el arcoíris", english: "the rainbow", pronunciation: "ar-koh-EE-rees" },
        { spanish: "el día", english: "the day", pronunciation: "DEE-ah" }
    ],
    seoKeywords: [
        "spanish weather vocabulary",
        "clima en español",
        "spanish books for kids",
        "lluvia y sol",
        "preschool spanish",
        "bilingual children's books",
        "free spanish books"
    ],
    metaDescription: "Aprende sobre el clima en español con 'La Lluvia y el Sol' - un libro interactivo gratuito para niños de 2-5 años. Enseña lluvia, sol, arcoíris y más.",
    difficulty: "Beginner",
    category: "Weather",
    themes: ["Nature", "Seasons", "Science"],
    culturalNotes: "Weather vocabulary is universal but essential for daily conversation. This book teaches the natural cycle of rain and sunshine, introducing basic weather patterns.",
    parentTips: [
        "Point out weather changes when you're outside together",
        "Ask '¿Qué tiempo hace hoy?' (What's the weather today?)",
        "Make it interactive: jump in puddles, watch rain, feel sunshine",
        "Connect to real experiences: 'Remember when we saw a rainbow?'"
    ],
    extensionActivities: [
        "Draw and label weather pictures",
        "Keep a weather chart for a week",
        "Make paper umbrellas",
        "Create rainbow art with paint or crayons"
    ],
    dateCreated: "2026-02-24",
    createdBy: "Luna 📚",
    version: "1.0"
};

// For Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = bookConfig;
}
