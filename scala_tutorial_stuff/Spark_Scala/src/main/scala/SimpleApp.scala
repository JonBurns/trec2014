/* SimpleApp.scala */
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import collection.mutable.ArrayBuffer
import scala.util.control.Breaks._

object SimpleApp {
    val ENGLISH_STOP_WORDS = List( "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fify", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves", "``", "''", "...", ",''", "''.", ",", ".", "'s", "$", "reuters", "ap", 
    "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "tech", 
    "news", "index", "mon", "tue", "wed", "thu", "fri", "sat", "'s", "a", "a's", "able", 
    "about", "above", "according", "accordingly", "across", "actually", "after", 
    "afterwards", "again", "against", "ain't", "all", "allow", "allows", "almost", 
    "alone", "along", "already", "also", "although", "always", "am", "amid", "among", 
    "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", 
    "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate", "are", 
    "aren't", "around", "as", "aside", "ask", "asking", "associated", "at", "available", "away", 
    "awfully", "b", "be", "became", "because", "become", "becomes", "becoming", "been", "before", 
    "beforehand", "behind", "being", "believe", "below", "beside", "besides", "best", "better", 
    "between", "beyond", "both", "brief", "but", "by", "c", "c'mon", "c's", "came", "can", "can't", 
    "cannot", "cant", "cause", "causes", "certain", "certainly", "changes", "clearly", "co", 
    "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", 
    "containing", "contains", "corresponding", "could", "couldn't", "course", "currently", "d", 
    "definitely", "described", "despite", "did", "didn't", "different", "do", "does", "doesn't", "doing", 
    "don't", "done", "down", "downwards", "during", "e", "each", "edu", "eg", "e.g.", "eight", "either", 
    "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "etc.", "even", "ever", 
    "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", 
    "f", "far", "few", "fifth", "five", "followed", "following", "follows", "for", "former", "formerly",
     "forth", "four", "from", "further", "furthermore", "g", "get", "gets", "getting", "given", "gives",
      "go", "goes", "going", "gone", "got", "gotten", "greetings", "h", "had", "hadn't", "happens", 
      "hardly", "has", "hasn't", "have", "haven't", "having", "he", "he's", "hello", "help", "hence", 
      "her", "here", "here's", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", 
      "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however", "i", "i'd", "i'll", 
      "i'm", "i've", "ie", "i.e.", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", 
      "indicate", "indicated", "indicates", "inner", "insofar", "instead", "into", "inward", "is", "isn't", 
      "it", "it'd", "it'll", "it's", "its", "itself", "j", "just", "k", "keep", "keeps", "kept", "know", 
      "knows", "known", "l", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "let's", 
      "like", "liked", "likely", "little", "look", "looking", "looks", "ltd", "m", "mainly", "many", "may", 
      "maybe", "me", "mean", "meanwhile", "merely", "might", "more", "moreover", "most", "mostly", "mr.", 
      "ms.", "much", "must", "my", "myself", "n", "namely", "nd", "near", "nearly", "necessary", "need", 
      "needs", "neither", "never", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", 
      "noone", "nor", "normally", "not", "nothing", "novel", "now", "nowhere", "o", "obviously", "of", 
      "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other", 
      "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own", 
      "p", "particular", "particularly", "per", "perhaps", "placed", "please", "plus", "possible", "presumably", 
      "probably", "provides", "q", "que", "quite", "qv", "r", "rather", "rd", "re", "really", "reasonably", "regarding", 
      "regardless", "regards", "relatively", "respectively", "right", "s", "said", "same", "saw", "say", "saying", "says", 
      "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", 
      "sent", "serious", "seriously", "seven", "several", "shall", "she", "should", "shouldn't", "since", "six", "so", 
      "some", "somebody", "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", 
      "sorry", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "t", "t's", "take", "taken",
       "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that's", "thats", "the", "their", "theirs", 
       "them", "themselves", "then", "thence", "there", "there's", "thereafter", "thereby", "therefore", "therein", 
       "theres", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've", "think", "third", "this", 
       "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", 
       "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "u", "un", 
       "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used", "useful",
        "uses", "using", "usually", "uucp", "v", "value", "various", "very", "via", "viz", "vs", "w", "want", "wants", 
        "was", "wasn't", "way", "we", "we'd", "we'll", "we're", "we've", "welcome", "well", "went", "were", "weren't", 
        "what", "what's", "whatever", "when", "whence", "whenever", "where", "where's", "whereafter", "whereas", "whereby", 
        "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "who's", "whoever", "whole", 
        "whom", "whose", "why", "will", "willing", "wish", "with", "within", "without", "won't", "wonder", "would", 
        "would", "wouldn't", "x", "y", "yes", "yet", "you", "you'd", "you'll", "you're", "you've", "your", "yours", 
        "yourself", "yourselves", "z", "zero", ".'", ",'")

   val query = "activities Morris Dees Southern Poverty Law Center".toLowerCase().split(" ")
   var debug = ""

   def filterer(aline: String): Boolean = {
        var count: Int = 0
        for (word <- query) {
            if (aline.toLowerCase() contains word) 
                count += 1         
        }
        if (count > 0) true
        else false
    }

  def uni_string_fixer(astring: String): Array[String] = {
    /* replace(" n't", "n't").replace(' \' ', '') */
    val new_string = astring.replaceAll(" n't", "n't").replaceAll( " '", "").replaceAll( " [.]", "").replaceAll( "[.]", "").replaceAll( ",", "").replaceAll("'", "").replaceAll("`` ", "").replaceAll("`", "").replaceAll("   ", " ").replaceAll("  ", " ").replaceAll("\n", "").toLowerCase().trim
    new_string.split(" ")
    }

  def bi_string_fixer(astring: String): Array[String] = {
    /* replace(" n't", "n't").replace(' \' ', '') */
    val new_string = astring.replaceAll(" n't", "n't").replaceAll( " '", "").replaceAll( " [.]", "").replaceAll( "[.]", "").replaceAll( ",", "").replaceAll("'", "").replaceAll("`` ", "").replaceAll("`", "").replaceAll("   ", " ").replaceAll("  ", " ").replaceAll("\n", "").toLowerCase().trim

    val list_of_words = new_string.split(" ")

    var new_list: Array[String] = Array[String]()
    for (x <- (0 to list_of_words.length - 2)) {
        var temp_string = list_of_words(x).toString() + " " + list_of_words(x + 1).toString()
        new_list = new_list :+ temp_string
      }

    new_list
    }

   def tri_string_fixer(astring: String): Array[String] = {
    /* replace(" n't", "n't").replace(' \' ', '') */
    val new_string = astring.replaceAll(" n't", "n't").replaceAll( " '", "").replaceAll( " [.]", "").replaceAll( "[.]", "").replaceAll( ",", "").replaceAll("'", "").replaceAll("`` ", "").replaceAll("`", "").replaceAll("   ", " ").replaceAll("  ", " ").replaceAll("\n", "").toLowerCase().trim

    val list_of_words = new_string.split(" ")

    var new_list: Array[String] = Array[String]()
    for (x <- (0 to list_of_words.length - 3)) {
        var temp_string = list_of_words(x).toString() + " " + list_of_words(x + 1).toString() + " " + list_of_words(x + 2).toString()
        new_list = new_list :+ temp_string
      }

    new_list
    }

  def filter_stop_words(aword: String): Boolean = {
    var alist = aword.split(" ")
    var count: Int = 0
    for (x <- alist) {
        if (ENGLISH_STOP_WORDS.contains(x))
            count += 1
    }
    if (count > 0) false
    else true
  }

  def vector_mapper(asentence: String, model: Array[(Int, String)]): (String, ArrayBuffer[Int]) = {
    val new_sentence = asentence.replaceAll(" n't", "n't").replaceAll( " '", "").replaceAll( " [.]", "").replaceAll( "[.]", "").replaceAll( ",", "").replaceAll("'", "").replaceAll("`` ", "").replaceAll("`", "").replaceAll("   ", " ").replaceAll("  ", " ").replaceAll("\n", "").toLowerCase().trim
    var vector: ArrayBuffer[Int] = collection.mutable.ArrayBuffer.fill(model.length)(0)
    for (x <- (0 until vector.length - 1)) {
        val word: String = model(x)._2
        if (new_sentence contains word) {
            vector(x) = 1
        }

    }
    (asentence, vector)
    
  }

  def score_mapper(sent_vector: (String, ArrayBuffer[Int]), summary_vector: ArrayBuffer[Int]): (String, ArrayBuffer[Int], Int) = {
    var result_vector = vector_logical_OR(sent_vector._2, summary_vector)

    var i = 0
    var sum = 0
    while(i < result_vector.length) {
        sum += result_vector(i)
        i += 1
    }
    (sent_vector._1, result_vector, sum)
  }

  def vector_logical_OR(vector_one: ArrayBuffer[Int], vector_two: ArrayBuffer[Int]): ArrayBuffer[Int] = {
    var vector: ArrayBuffer[Int] = collection.mutable.ArrayBuffer.fill(vector_one.length)(0)

    for (x <- (0 until vector.length)) {
        if (vector_one(x) == 1 || vector_two(x) == 1) {
            vector(x) = 1
        }
    }
    vector
  }



  def main(args: Array[String]) {
    val logFile = "/Users/jonathanburns/Development/SummerResearch/trec2014/Old_Summarization_Files/ROUGE/DUC-2007/docs/D0701A/" // Should be some file on your system
    val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)
    val logData = sc.textFile(logFile, 2).cache()

    val uni_counts = logData.filter(filterer).flatMap(line => uni_string_fixer(line)).filter(filter_stop_words).map(word => (word, 1)).reduceByKey(_+_).map(tuple => (tuple._2, tuple._1)).sortByKey().top(20)
    val bi_counts = logData.filter(filterer).flatMap(line => bi_string_fixer(line)).filter(filter_stop_words).map(word => (word, 1)).reduceByKey(_+_).map(tuple => (tuple._2, tuple._1)).sortByKey().top(20)
    val tri_counts = logData.filter(filterer).flatMap(line => tri_string_fixer(line)).filter(filter_stop_words).map(word => (word, 1)).reduceByKey(_+_).map(tuple => (tuple._2, tuple._1)).sortByKey().top(20)

    var model = uni_counts ++ bi_counts ++ tri_counts

    val mapped_sentences = logData.map(sentence => vector_mapper(sentence, model)).sortByKey().cache()
    var summary_vector: ArrayBuffer[Int] = collection.mutable.ArrayBuffer.fill(model.length)(0)
    var summary = ("", summary_vector)

    var scores = mapped_sentences.map(sent_vector => score_mapper(sent_vector, summary._2)).map(tuple => (tuple._3, (tuple._1, tuple._2))).sortByKey(false).take(1)

    while (summary._1.split(" ").length < 250) {
        var scores = mapped_sentences.map(sent_vector => score_mapper(sent_vector, summary._2)).map(tuple => (tuple._3, (tuple._1, tuple._2))).sortByKey(false).take(1)
        var new_summary_sentence = summary._1 + "\n" + scores(0)._2._1
        var new_summary_vector = scores(0)._2._2
        summary = (new_summary_sentence, new_summary_vector)
    }

    println(summary)

  }

}