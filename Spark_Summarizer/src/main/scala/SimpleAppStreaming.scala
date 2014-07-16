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
    val ssc = new StreamingContext(sparkConf, Seconds(10))
    ssc.checkpoint("./Streaming_logs")

    // Create a socket stream on target ip:port and count the
    // words in input stream of \n delimited text (eg. generated by 'nc')
    // Note that no duplication in storage level only for running locally.
    // Replication necessary in distributed scenario for fault tolerance.
    val lines = ssc.socketTextStream("localhost", 9999, StorageLevel.MEMORY_AND_DISK_SER)
    val unigrams = lines.flatMap(_.split(" "))
    val bigrams = lines.flatMap(bi_string_fixer(_))

    val unigramDstream = unigrams.map(x => (x, 1))
    val bigramsDstream = bigrams.map(x => (x, 1))

    val uniStateDstream = unigramDstream.updateStateByKey[Int](updateFunc)
    val biStateDstream = bigramsDstream.updateStateByKey[Int](updateFunc)

    val uniSorted = uniStateDstream.map { case(tag, count) =>  (count, tag) }.transform(rdd => rdd.sortByKey(false))
    val biSorted = biStateDstream.map { case(tag, count) =>  (count, tag) }.transform(rdd => rdd.sortByKey(false))

    var topUni: Array[(Int, String)] = null
    var topBi: Array[(Int, String)] = null



    //We need to take the top # of unigrams, this code will store them in topUni
    uniSorted.foreachRDD(rdd => {
    val currentTopUniCounts = rdd.take(10)
    topUni = currentTopUniCounts
    //println("\nTop 10 Uni:\n" + rdd.take(10).mkString("\n"))
     } )

    //We need to take the top # of bigrams, this code will store them in topBi
    biSorted.foreachRDD(rdd => {
    val currentTopBiCounts = rdd.take(15)
    topBi = currentTopBiCounts
    //println("\nTop 15 Bi:\n" + rdd.take(15).mkString("\n"))
     } )

    //This is so that we don't get a null pointer exception right off the bat
    var model = Array((0, ""))
    var modelLength = 0

    //These will be null until we get information
    //It doesn't make sense to do anything until we get that information
    biSorted.foreachRDD(rdd => {
    if (topUni != null && topBi != null) {
        model = topUni ++ topBi
        modelLength = model.length
    }
    })

        // //We use our model here to create a tuple (sentence, vectorOfCoverage)

    var vectorizedSentences = lines.map(sentence => vector_mapper(sentence, model))

    var summary_vector: ArrayBuffer[Int] = collection.mutable.ArrayBuffer.fill(model.length)(0)
    var summary = ("", summary_vector)

    // vectorizedSentences.print()
    var i = 0
    var old_summary = ""
    biSorted.foreachRDD(rdd => {
        summary_vector = collection.mutable.ArrayBuffer.fill(model.length)(0)
        if (summary._1 != "") {
            old_summary = summary._1
            summary = ("", summary_vector)
        }
        else {
            summary = ("", summary_vector)
        }
    })

    while (i < 5) {
        var scores = vectorizedSentences.map(sent_vector => score_mapper(sent_vector, summary._2)).map(tuple => (tuple._3, (tuple._1, tuple._2))).transform(rdd => rdd.sortByKey(false)).persist()
        // vectorizedSentences.print()
        //Scores are calculated based on the vectorOfCoverage and what has already been covered, summary._2
        //scores.print()
        var topScore: Array[(Int, (String, ArrayBuffer[Int]))] = null

        //We need to delve into the Dstream here to grab the top most score
        scores.foreachRDD(rdd => {
            val currentTopScore = rdd.take(1)
            topScore = currentTopScore
            var old_summary_top_score = summary_scoreer(old_summary, model, summary._2) 
            println("\nTop Score:\n" + rdd.take(1).mkString("\n")) 
            println("\nTop Old Score:\n" + old_summary_top_score._2._1 + "\n\n\n") 
            if (topScore.length > 0) { //Or old summary
                println("\n\n\n\n Summary Creation sentence: " + i + "\n\n")
                if (topScore(0)._1 > old_summary_top_score._1) {
                    var new_summary_sentence = summary._1 + "\n" + topScore(0)._2._1 //<- Error
                    var new_summary_vector = topScore(0)._2._2
                    summary = (new_summary_sentence, new_summary_vector)
                    println("\n\n\nSummary:\n" + summary._1 + "\n\n\n\n")
                }
                else {
                    var new_summary_sentence = summary._1 + "\n" + old_summary_top_score._2._1 //<- Error
                    var new_summary_vector = old_summary_top_score._2._2
                    summary = (new_summary_sentence, new_summary_vector)
                    println("\n\n\nSummary:\n" + summary._1 + "\n\n\n\n")
                }

            }
        } )

        i = i + 1
    }
    ssc.start()
    ssc.awaitTermination()
  }
}
