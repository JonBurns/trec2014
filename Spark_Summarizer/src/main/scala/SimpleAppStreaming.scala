/* SimpleApp.scala */
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.api.java.function._
import org.apache.spark.streaming._
import org.apache.spark.streaming.api._

import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.StreamingContext._
import org.apache.spark.storage.StorageLevel

import collection.mutable.ArrayBuffer

import scala.util.control.Breaks._


/**
 * Counts words in UTF8 encoded, '\n' delimited text received from the network every second.
 *
 * Usage: NetworkWordCount <hostname> <port>
 * <hostname> and <port> describe the TCP server that Spark Streaming would connect to receive data.
 *
 * To run this on your local machine, you need to first run a Netcat server
 *    `$ nc -lk 9999`
 * and then run the example
 *    `$ sbt package
 *    '$ spark-submit --class "NetworkWordCount" --master local[4] target/scala-2.10/simple-project_2.10-1.0.jar
 */




object NetworkWordCount {

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

   def uni_string_fixer(astring: String): Array[String] = {
    /* replace(" n't", "n't").replace(' \' ', '') */
    val new_string = astring.replaceAll(" n't", "n't").replaceAll( " '", "").replaceAll( " [.]", "").replaceAll( "[.]", "").replaceAll( ",", "").replaceAll("'", "").replaceAll("`` ", "").replaceAll("`", "").replaceAll("   ", " ").replaceAll("  ", " ").replaceAll("\n", "").toLowerCase().trim

    val list_of_words = new_string.split(" ").filter(item => !(ENGLISH_STOP_WORDS contains item))

    list_of_words
  }

  def bi_string_fixer(astring: String): Array[String] = {
    /* replace(" n't", "n't").replace(' \' ', '') */
    val new_string = astring.replaceAll(" n't", "n't").replaceAll( " '", "").replaceAll( " [.]", "").replaceAll( "[.]", "").replaceAll( ",", "").replaceAll("'", "").replaceAll("`` ", "").replaceAll("`", "").replaceAll("   ", " ").replaceAll("  ", " ").replaceAll("\n", "").toLowerCase().trim

    val list_of_words = new_string.split(" ").filter(item => !(ENGLISH_STOP_WORDS contains item))

    var new_list: Array[String] = Array[String]()
    for (x <- (0 to list_of_words.length - 2)) {
        var temp_string = list_of_words(x).toString() + " " + list_of_words(x + 1).toString()
        new_list = new_list :+ temp_string
      }

    new_list
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


    for (x <- (0 until vector.length - 1)) {
        try {
        if (vector_one(x) == 1 || vector_two(x) == 1) { //<----- Error
            vector(x) = 1
        }
        } catch {
            case e: Exception => System.err.println("Error in logical OR")
        }
    }
    vector
  }

  def summary_scoreer(summary: String, model: Array[(Int, String)], currentSummaryVector: ArrayBuffer[Int]): (Int, (String, ArrayBuffer[Int])) = {
    var sentences = summary.split("\n")
    var vectorizedSentenceHolder: ArrayBuffer[(String, ArrayBuffer[Int])] = new ArrayBuffer[(String, ArrayBuffer[Int])]
    var scoreHolder: ArrayBuffer[(String, ArrayBuffer[Int], Int)] = new ArrayBuffer[(String, ArrayBuffer[Int], Int)]
    for (sentence <- sentences) {
        vectorizedSentenceHolder.append(vector_mapper(sentence, model))
    }
    var max = 0
    var max_sentence: (String, ArrayBuffer[Int], Int) = null
    for (sentVector <- vectorizedSentenceHolder) {
        var score = score_mapper(sentVector, currentSummaryVector)
        scoreHolder.append(score)
        if (score._3 > max) {
            max_sentence = score
        }
    }
    //test return
    if (max_sentence != null){
        (max_sentence._3, (max_sentence._1, max_sentence._2))
    }
    else {
        (-1, ("", ArrayBuffer(1)))
    }
    // (1, ("", ArrayBuffer(1)))
  }

  def main(args: Array[String]) {
    // if (args.length < 2) {
    //   System.err.println("Usage: NetworkWordCount <hostname> <port>")
    //   System.exit(1)
    // }
    val updateFunc = (values: Seq[Int], state: Option[Int]) => {
      val currentCount = values.foldLeft(0)(_ + _)

      val previousCount = state.getOrElse(0)

      Some(currentCount + previousCount)
    }

    //StreamingExamples.setStreamingLogLevels()

    // Create the context with a 1 second batch size
    val sparkConf = new SparkConf().setAppName("NetworkWordCount")
    val ssc = new StreamingContext(sparkConf, Seconds(30))
    ssc.checkpoint("./Streaming_logs")
    // Create a socket stream on target ip:port and count the
    // words in input stream of \n delimited text (eg. generated by 'nc')
    // Note that no duplication in storage level only for running locally.
    // Replication necessary in distributed scenario for fault tolerance.
    val lines = ssc.socketTextStream("localhost", 9999, StorageLevel.MEMORY_AND_DISK_SER)
    val unigrams = lines.flatMap(uni_string_fixer(_))
    val bigrams = lines.flatMap(bi_string_fixer(_))

    val unigramDstream = unigrams.map(x => (x, 1))
    val bigramsDstream = bigrams.map(x => (x, 1))

    val uniStateDstream = unigramDstream.updateStateByKey[Int](updateFunc)
    val biStateDstream = bigramsDstream.updateStateByKey[Int](updateFunc)

    val currentUniSorted= unigramDstream.reduceByKey(_ + _).map { case(tag, count) =>  (count, tag) }.transform(rdd => rdd.sortByKey(false))
    val currentBiSorted = bigramsDstream.reduceByKey(_ + _).map { case(tag, count) =>  (count, tag) }.transform(rdd => rdd.sortByKey(false))

    val uniSorted = uniStateDstream.map { case(tag, count) =>  (count, tag) }.transform(rdd => rdd.sortByKey(false))
    val biSorted = biStateDstream.map { case(tag, count) =>  (count, tag) }.transform(rdd => rdd.sortByKey(false))

    var topUni: Array[(Int, String)] = null
    var topBi: Array[(Int, String)] = null

    var currentTopUni: Array[(Int, String)] = null
    var currentTopBi: Array[(Int, String)] = null


    //We need to take the top # of unigrams, this code will store them in topUni
    uniSorted.foreachRDD(rdd => {
    val currentTopUniCounts = rdd.take(20)
    topUni = currentTopUniCounts
    println("\nTop 20 Uni(Stateful):\n" + rdd.take(20).mkString("\n"))
     } )

    //We need to take the top # of bigrams, this code will store them in topBi
    biSorted.foreachRDD(rdd => {
    val currentTopBiCounts = rdd.take(15)
    topBi = currentTopBiCounts
    println("\nTop 15 Bi(Stateful):\n" + rdd.take(15).mkString("\n"))
     } )

    currentUniSorted.foreachRDD(rdd => {
    val currentTopUniCounts = rdd.take(20)
    currentTopUni = currentTopUniCounts
    println("\nTop 20 Uni(Non-Stateful):\n" + rdd.take(10).mkString("\n"))
     } )

    currentBiSorted.foreachRDD(rdd => {
    val currentTopBiCounts = rdd.take(15)
    currentTopBi = currentTopBiCounts
    println("\nTop 15 Bi(Non-Stateful):\n" + rdd.take(5).mkString("\n"))
     } )

    //This is so that we don't get a null pointer exception right off the bat
    var model = Array((0, ""))
    var modelLength = 0

    //These will be null until we get information
    //It doesn't make sense to do anything until we get that information
    biSorted.foreachRDD(rdd => {
    if (topUni != null && topBi != null) {
        model = topUni ++ topBi ++ currentTopUni ++ currentTopBi
        modelLength = model.length
        println("\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for (x <- model) {
            println(x)
        }
        println("Length: " + model.length)
        println("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n")
    }
    })

    //     // //We use our model here to create a tuple (sentence, vectorOfCoverage)

    // var vectorizedSentences = lines.map(sentence => vector_mapper(sentence, model))

    // var summary_vector: ArrayBuffer[Int] = collection.mutable.ArrayBuffer.fill(model.length)(0)
    // var summary = ("", summary_vector)

    // // vectorizedSentences.print()
    // var i = 0
    // var old_summary = ""
    // biSorted.foreachRDD(rdd => {
    //     summary_vector = collection.mutable.ArrayBuffer.fill(model.length)(0)
    //     if (summary._1 != "") {
    //         old_summary = summary._1
    //         summary = ("", summary_vector)
    //     }
    //     else {
    //         summary = ("", summary_vector)
    //     }
    // })

    // while (i < 10) {

    //     var scores = vectorizedSentences.map(sent_vector => score_mapper(sent_vector, summary._2)).map(tuple => (tuple._3, (tuple._1, tuple._2))).transform(rdd => rdd.sortByKey(false)).persist()
    //     // vectorizedSentences.print()
    //     //Scores are calculated based on the vectorOfCoverage and what has already been covered, summary._2
    //     //scores.print()
    //     var topScore: Array[(Int, (String, ArrayBuffer[Int]))] = null

    //     //We need to delve into the Dstream here to grab the top most score
    //     scores.foreachRDD(rdd => {
    //         val oldScore = 0    
    //         val currentTopScore = rdd.take(1)
    //         topScore = currentTopScore

    //         var i = 0
    //         var sum = 0
    //         while(i < summary._2.length) {
    //             sum += summary._2(i)
    //             i += 1
    //         }

    //         var old_summary_top_score = summary_scoreer(old_summary, model, summary._2) 
    //         println("\nCurrent Summary Total: " + sum + "\n\n") 
    //         println("\nTop Score:\n" + rdd.take(1).mkString("\n")) 
    //         println("\nTop Old Score:\n" + old_summary_top_score._2._1 + " " + old_summary_top_score._1 + "\n\n\n") 

    //         if (topScore.length == 0)  {
    //             summary = (old_summary, ArrayBuffer(0))
    //         }
    //         else if ((topScore.length > 0) || (old_summary != "")) { //Or old summary
    //             println("\n\n\n\n Summary Creation sentence: " + i + "\n\n")

    //             if ((topScore(0)._1 >= old_summary_top_score._1) && (topScore(0)._1 - sum != 0)) {
    //                 var new_summary_sentence = summary._1 + "\n" + topScore(0)._2._1 //<- Error
    //                 var new_summary_vector = topScore(0)._2._2



    //                 println("\n\n~~~~~~~~~~~~~New Chosen~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nSummary:\n Old Vector: " + summary._2 + "\n New Vector: " + new_summary_vector + "\n Difference: " + (topScore(0)._1 - sum)) 
    //                 summary = (new_summary_sentence, new_summary_vector)
    //                 println("\n\n" + summary._1 + "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
                    
    //             }

    //             else if ((topScore(0)._1 < old_summary_top_score._1) && (old_summary_top_score._1 - sum != 0)) {
    //                 var new_summary_sentence = summary._1 + "\n" + old_summary_top_score._2._1 //<- Error
    //                 var new_summary_vector = old_summary_top_score._2._2



    //                 println("\n\n~~~~~~~~~~~~~Old Chosen~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nSummary:\n Old Vector: " + summary._2 + "\n New Vector: " + new_summary_vector + "\n Difference: " + (old_summary_top_score._1 - sum))
    //                 summary = (new_summary_sentence, new_summary_vector)
    //                 println("\n\n" + summary._1 + "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    //                 //old_summary = old_summary.split("\n").filter(sentence => !(summary._1 contains sentence)).mkString("\n")
    //             }
    //             else {
    //                 println("\n\n\n\n0 Added bonus, no sentence added!\n")
    //                 println("\n\n" + summary._1 + "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n\n")
    //             }

    //         }
    //     } )

    //     i = i + 1
    // }
    ssc.start()
    ssc.awaitTermination()
  }
}
