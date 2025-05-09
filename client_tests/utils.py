class Utils:
    @staticmethod
    def prepare_for_assert(string: str) -> str:
        return string.lower().replace(",", "").replace(".", "").replace("'", "")
