class BaseChai:
    def __init__(self, type_):
        self.type = type_

    def prepare(self):
        print(f"Preparing {self.type} chai....")


class MasalaChai(BaseChai):
    def add_spices(self):
        print("Adding cardamom, ginger, cloves.")


class ChaiShop:
    chai_cls = BaseChai

    def __init__(self):
        self.chai = self.chai_cls("Regular")

    def serve(self):
        print(f"Serving {self.chai.type} chai in the shop")
        self.chai.prepare()


class FancyChaiShop(ChaiShop):
    chai_cls = MasalaChai


shop = ChaiShop()           #  ChaiShop ka object bana (BaseChai("Regular"))
fancy = FancyChaiShop()     #  FancyChaiShop ka object bana (MasalaChai("Regular"))

shop.serve()                #  Serving Regular chai in the shop
                            #  Preparing Regular chai....

fancy.serve()               #  Serving Regular chai in the shop
                            #  Preparing Regular chai....

fancy.chai.add_spices()     #  Adding cardamom, ginger, cloves.



# Serving Regular chai in the shop
# Preparing Regular chai....
# Serving Regular chai in the shop
# Preparing Regular chai....
# Adding cardamom, ginger, cloves.
