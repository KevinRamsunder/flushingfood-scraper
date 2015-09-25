public class Yelp {
	
	private static YelpAPI yelp = new YelpAPI("", "", "", "");
	
	public Yelp() {
		
	}
	
	/** Query Yelp API for given 'restaurantID'. Return the full JSON string */
	public String getJsonFromRestaurantID(String restaurantID) {
		JSONParser parser = new JSONParser();
		String parsedResults = parser.parse(yelp.searchByBusinessId(restaurantID)).toString();
		return parsedResults;
	}
	
	/** Query Yelp API for given 'restaurantID' and extract a JSON value based on 'jsonKey' */
	public String getJsonValueFromRestaurantID(String restaurantID, String jsonKey) throws JsonKeyNotFoundException {
		String restaurantJSON = getJsonFromRestaurantID(restaurantID);
		return getKeyFromParsedJSON(restaurantJSON, jsonKey);
	}
	
	public String getKeyFromParsedJSON(String parsedJSON, String jsonKey) throws JsonKeyNotFoundException {
		JsonObject jsonObject = (JSONObject) JSONValue.parse(parsedJSON);
		
		if(jsonObject.get(jsonKey) == null) {
			throw new JsonKeyNotFoundException("This key does not exist");
		} else {
			return jsonObject.get(jsonKey).toString();
		}
	}
}
