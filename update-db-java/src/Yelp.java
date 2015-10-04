import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/** Program which updates YELP API data for each restaurant in the DB */

public class Yelp {

   private static final String CONSUMER_KEY = "";
   private static final String CONSUMER_SECRET = "";
   private static final String TOKEN = "";
   private static final String TOKEN_SECRET = "";

   private static YelpAPI api = new YelpAPI(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET);

   public static void main(String[] args) throws Exception {
      // DB connection object
      Connection connection = null;

      // init connection to database
      try {
         connection = (Connection) DriverManager.getConnection(
               "jdbc:mysql://127.0.0.1/flushingfood", "root", "");
      } catch (SQLException e1) {
         e1.printStackTrace();
      }

      // objects to interact with the DB
      Statement s = connection.createStatement();
      Statement i = connection.createStatement();

      // Query DB and store results in ResultSet      
      ResultSet rs = s.executeQuery("select * from `yelp`");

      // Loop through ResultSet object
      while (rs.next()) {
         // extract restaurant ID and phone number
         String phone = rs.getString("phone");
         String key = rs.getString("yelp");

         // Query YELP API for JSON attributes
         String result = api.searchByBusinessId(key).toString();

         // Parse YELP API callback for desired attributes
         JSONObject jsonObject = (JSONObject) JSONValue.parse(result);
         String newImageURL = (String) jsonObject.get("rating_img_url");
         String newRatingCount = String.valueOf(jsonObject.get("review_count"));
         
         // debugging
         System.out.println(key + ", " + newRatingCount);
         
         // Update DB with updated parameters
         String query = "UPDATE `flushingfood`.`yelp` SET `ratingCount` = '%COUNT%', `ratingUrl` = '%URL%' WHERE `yelp`.`phone` = '%PHONE%';";
         query = query.replaceFirst("%COUNT%", newRatingCount);
         query = query.replaceFirst("%URL%", newImageURL);
         query = query.replaceFirst("%PHONE%", phone);
         i.execute(query);
      }

      // close DB connection
      connection.close();
   }
}