import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class FlushingFood {
   
   public static void main(String[] args) {
      Document doc = null;
      
      try {
         doc = Jsoup.connect("http://flushingfood.com").timeout(30 * 1000).get();
      } catch (IOException e) {
         System.out.println(e.getLocalizedMessage());
         System.exit(0);
      }
      
      Elements pics = doc.select("div.position_content[id^=u]");
      
      for(Element e : pics) {
         System.out.println(e.child(1).child(0).select("span").get(0).ownText());
         
         Elements address = e.child(2).select("p");
         for(Element e1 : address) {
            System.out.print(" - " + e1.text());
         }
         
         System.out.println("\n");
      }
   }
}