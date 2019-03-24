import murmurhash
from config_parse import XmlConfiger


class ABTest:
    def __init__(self):
        self.__exp = {}
        self.__bucket_num = 1e10
        self.__hasher = murmurhash.mrmr

    def parse_from_xml(self, xml_path):
        data = XmlConfiger(xml_path).get_data()
        for unit in data["data"]:
            if unit["tag"] == "bucket_num":
                self.__bucket_num = int(unit["text"])
            elif unit["tag"] == "exp":
                exp_id = int(unit["attrib"]["exp_id"])
                exp_name = unit["attrib"]["exp_name"]
                exp_rate = float(unit["attrib"]["exp_rate"])
                layered = bool(int(unit["attrib"]["layered"]))
                self.__add_exp(exp_id, exp_name, exp_rate, layered)
                if layered:
                    layers_data = unit["data"]
                    for layer_data in layers_data:
                        layer_id = int(layer_data["attrib"]["layer_id"])
                        layer_name = layer_data["attrib"]["layer_name"]
                        self.__add_layer(exp_id, layer_id, layer_name)
                        for sub_layer_data in layer_data["data"]:
                            sub_layer_id = int(sub_layer_data["attrib"]["layer_id"])
                            sub_layer_name = sub_layer_data["attrib"]["layer_name"]
                            sub_layer_rate = float(sub_layer_data["attrib"]["layer_rate"])
                            self.__add_sub_layer(exp_id, layer_id, sub_layer_id, sub_layer_name, sub_layer_rate)
        self.__check()

    def get_exp(self, string):
        bucket, layers = self.__hash(string), []
        for exp_id, exp_name, exp_val, layered in self.__exp_data:
            if bucket <= exp_val:
                if layered:
                    layers = self.__get_layers(exp_id, bucket)
                return exp_id, exp_name, layered, layers
        return None, None, None, None

    def __check(self):
        if self.__bucket_num < 10:
            raise Exception("Bucket Num <= 10")
        if not self.__check_sum():
            raise Exception("Exp Sum != 100%")

    def __hash(self, string):
        return self.__hasher.hash(string) % self.__bucket_num

    def __add_exp(self, exp_id, exp_name, exp_rate, layered = False):
        # layered = True 分层流量实验
        # layered = False 独占流量实验
        self.__exp[exp_id] = {
            "exp_id": exp_id,
            "exp_name": exp_name,
            "exp_rate": exp_rate,
            "layered": layered
        }
        if layered:
            self.__exp[exp_id]["layers"] = {}

    # layered 分层流量实验加层
    def __add_layer(self, exp_id, layer_id, layer_name):
        self.__exp[exp_id]["layers"][layer_id] = {
            "layer_id": layer_id,
            "layer_name": layer_name,
            "sub_layers": {}
        }

    def __add_sub_layer(self, exp_id, layer_id, sub_layer_id, sub_layer_name, sub_layer_rate):
        self.__exp[exp_id]["layers"][layer_id]["sub_layers"][sub_layer_id] = {
            "sub_layer_id": sub_layer_id,
            "sub_layer_name": sub_layer_name,
            "sub_layer_rate": sub_layer_rate
        }

    def __check_sum(self):
        all_rate = 0.0
        for exp_id in self.__exp:
            all_rate += self.__exp[exp_id]["exp_rate"]
            if self.__exp[exp_id]["layered"] == 1:
                if len(self.__exp[exp_id]["layers"]) == 0:
                    return False
                for layer_id in self.__exp[exp_id]["layers"]:
                    D = self.__exp[exp_id]["layers"][layer_id]["sub_layers"]
                    sub_all_rate = sum([D[sub_layer_id]["sub_layer_rate"] for sub_layer_id in D])
                    if sub_all_rate != 1:
                        return False
        if all_rate != 1:
            return False
        self.__redata()
        return True

    def __redata(self):
        self.__exp_data = []
        self.__layer_data = {}
        curr_exp_val = 0
        for exp_id in self.__exp:
            curr_exp_val += self.__exp[exp_id]["exp_rate"] * self.__bucket_num
            self.__exp_data.append(
                (self.__exp[exp_id]["exp_id"],
                 self.__exp[exp_id]["exp_name"],
                 curr_exp_val,
                 self.__exp[exp_id]["layered"]))
            if self.__exp[exp_id]["layered"]:
                self.__layer_data[exp_id] = {}
                for layer_id in self.__exp[exp_id]["layers"]:
                    layer_name = self.__exp[exp_id]["layers"][layer_id]["layer_name"]
                    self.__layer_data[exp_id][layer_id] = []
                    D = self.__exp[exp_id]["layers"][layer_id]["sub_layers"]
                    curr_sub_layer_val = 0
                    for sub_layer_id in D:
                        sub_layer_name = D[sub_layer_id]["sub_layer_name"]
                        sub_layer_rate = D[sub_layer_id]["sub_layer_rate"]
                        curr_sub_layer_val += sub_layer_rate * self.__bucket_num
                        self.__layer_data[exp_id][layer_id].append(
                            (layer_id, layer_name, sub_layer_id, sub_layer_name, curr_sub_layer_val))

    def __get_layers(self, exp_id, bucket):
        layers = []
        for layer_id in self.__layer_data[exp_id]:
            new_bucket = self.__hash(str(bucket) + str(layer_id))
            for _, layer_name, sub_layer_id, sub_layer_name, sub_layer_val in self.__layer_data[exp_id][layer_id]:
                if new_bucket <= sub_layer_val:
                    layers.append((layer_id, layer_name, sub_layer_id, sub_layer_name))
                    break
        return layers
