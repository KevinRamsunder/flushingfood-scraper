public class Phone {

	public static String unphonify(String phone) {
		String k = phone;
		String ret = "";

		for (int i = 1; i < 4; i++) {
			ret += k.charAt(i);
		}

		for (int i = 6; i < 9; i++) {
			ret += k.charAt(i);
		}

		for (int i = 10; i < 14; i++) {
			ret += k.charAt(i);
		}

		return ret;
	}

	public static String phonify(String phone) {
		String k = phone;
		String ret = "(";

		for (int i = 0; i < 3; i++) {
			ret += k.charAt(i);
		}

		ret += ") ";

		for (int i = 3; i < 6; i++) {
			ret += k.charAt(i);
		}

		ret += "-";

		for (int i = 6; i < 10; i++) {
			ret += k.charAt(i);
		}

		return ret;
	}
}