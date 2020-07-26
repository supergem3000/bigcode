from Storage import Storage
from Preprocesser import Preprocesser
from Analyser import Analyser
from Output import Output

FILE_PATH = ".\\test_data.json"

def init():
    storage = Storage(FILE_PATH)
    preprocesser = Preprocesser(storage)
    preprocesser.grouping()
    preprocesser.organize()
    preprocesser.complement()
    analyser = Analyser(storage)
    analyser.kmeans()
    Output.write_case_cluster(storage.get_case_cluster())
    Output.visualize_case_cluster(storage.get_km_data(), storage.get_label())
    analyser.calc_total_weight()
    analyser.calc_user_result()
    Output.write_user_result(storage.get_user_result())
    Output.visualize_user_result(storage.get_user_result())

if __name__ == "__main__":
    init()
