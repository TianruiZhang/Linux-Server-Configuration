#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Selection, MenuItem, User

engine = create_engine("sqlite:///menu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(
    name="James Chang",
    email="jameschang1992@gmail.com",
    picture="https://drive.google.com/open?id=0B9-3llFqZxcNSjlmVE1Ub1ZyTk0"
    )
session.add(User1)
session.commit()

FirstSelection = Selection(
    user_id=1,
    name="Appetizers & Party Platters")
session.add(FirstSelection)
session.commit()
AntipastoPlatter = MenuItem(
    user_id=1,
    name="Antipasto Platter",
    description='''
    An array of prosciutto, sopressata, salami, provolone cheese, marinated
    fresh mozzarella, grilled vegetables, marinated artichokes and olives.
    Served with crusty bread and saffron aioli to spread.''',
    price="$69.99",
    selection=FirstSelection)
session.add(AntipastoPlatter)
session.commit()
VegetableAntipasto = MenuItem(
    user_id=1,
    name="Vegetable Antipasto",
    description='''A kaleidoscope of delectable grilled eggplant, portobello
    mushrooms, carrots, onions, squash and bell peppers with provolone
    and marinated fresh mozzarella cheese. Accompanied by saffron aioli, hummus
    and assorted crusty breads.''',
    price="$44.99",
    selection=FirstSelection)
session.add(VegetableAntipasto)
session.commit()
CheeseDisplay = MenuItem(
    user_id=1,
    name="Cheese Display",
    description='''A sextet of cheeses to delight the palate: cheddar,
    dill havarti, jarlsberg, brie, bleu and herb cheese served with crackers
    and baguette.''',
    price="$49.99",
    selection=FirstSelection)
session.add(CheeseDisplay)
session.commit()
CruditePlatter = MenuItem(
    user_id=1,
    name="Crudite Platter",
    description='''A bountiful presentation of fresh garden vegetables to dip
    in buttermilk ranch and hummus.''',
    price="$39.99",
    selection=FirstSelection)
session.add(CruditePlatter)
session.commit()
FreshFruitDisplay = MenuItem(
    user_id=1,
    name="Fresh Fruit Display",
    description='''A luscious selection of seasonal fruit such as pineapple,
    melon and berries in a colorful arrangement, with a touch of the
    exotic.''',
    price="$39.99",
    selection=FirstSelection)
session.add(FreshFruitDisplay)
session.commit()
FreshRoastedDeliMeatsandCheese = MenuItem(
    user_id=1,
    name='''Fresh Roasted Deli Meats and Cheese''',
    description='''Create your own meal from our freshly baked or grilled deli
    meats: garlic rosemary roast beef, roasted turkey breast, grilled chicken
    breast – and delectable cheeses – creamy havarti, Emmentaler Swiss and
    hearty cheddar. Accompanied by sandwich bread, grilled red onions, sliced
    tomato, leaf lettuce and a trio of tasty spreads – saffron aioli, whole
    grain mustard and mayonnaise.''',
    price="$69.99",
    selection=FirstSelection)
session.add(FreshRoastedDeliMeatsandCheese)
session.commit()
FreshFruitandCheese = MenuItem(
    user_id=1,
    name="Fresh Fruit and Cheese",
    description='''Ripe seasonal fresh fruit arranged with brie, cheddar,
    Jarlsberg and bleu cheeses. Served with crackers and baguette.''',
    price="$49.99",
    selection=FirstSelection)
session.add(FreshFruitandCheese)
session.commit()
LondonBroilPlatter = MenuItem(
    user_id=1,
    name="London Broil Platter",
    description='''We marinate lean beef, cook it medium rare, then slice and
    artfully present it with julienne grilled onions, portobello mushrooms,
    horseradish mayo and saffron aioli. Includes a sliced baguette.''',
    price="$139.99",
    selection=FirstSelection)
session.add(LondonBroilPlatter)
session.commit()
PoachedSalmonMedallions = MenuItem(
    user_id=1,
    name="Poached Salmon Medallions",
    description='''Delicate Atlantic salmon medallions garnished with a
    signature trio – tomato caper relish, lemon mustard sauce and citrus
    salsa.''',
    price="$99.99",
    selection=FirstSelection)
session.add(PoachedSalmonMedallions)
session.commit()
QuesadillaPlatter = MenuItem(
    user_id=1,
    name="Quesadilla Platter",
    description='''Black bean quesadillas and chicken quesadillas cut into
    triangles and dislayed with pico de gallo and guacamole.''',
    price="$49.99",
    selection=FirstSelection)
session.add(QuesadillaPlatter)
session.commit()
WingTrio = MenuItem(
    user_id=1,
    name="Wing Trio",
    description='''Chef’s signature chicken wings - buffalo, black cherry BBQ
    and maple BBQ - garnished with crunchy fresh vegetable sticks.''',
    price="$49.99",
    selection=FirstSelection)
session.add(WingTrio)
session.commit()

SecondSelection = Selection(
    user_id=1,
    name="Boxed Lunches & Sandwiches")
session.add(SecondSelection)
session.commit()
HoagieSandwichPlatter = MenuItem(
    user_id=1,
    name="Hoagie Sandwich Platter",
    description='''Hoagies cut into 4" pieces so you can try a variety. The
    small platter features classic Italian, turkey, and roasted eggplant
    hoagies. The large platter also includes hot Italian and chicken avocado
    hoagies.''',
    price="$59.99",
    selection=SecondSelection)
session.add(HoagieSandwichPlatter)
session.commit()
HoagieSandwichFeast = MenuItem(
    user_id=1,
    name="Hoagie Sandwich Feast",
    description='''Make it a feast and we’ll include a large tossed garden
    salad with balsamic vinaigrette, our signature smoked mozzarella pasta
    salad, and an assortment of tea cookies, brownies and dessert bars. our
    Hoagies are cut into 4" pieces so you can try a variety. The small Platter
    features classic Italian, turkey, and roasted eggplant hoagies. The large
    platter also includes hot Italian and chicken avocado hoagies.''',
    price="$99.99",
    selection=SecondSelection)
session.add(HoagieSandwichFeast)
session.commit()
SignatureWrapPlatter = MenuItem(
    user_id=1,
    name="Signature Wrap Platter",
    description='''A delicious combination of ingredients wrapped in a
    flavorful tortilla and arranged in a tempting display. Includes double
    honey turkey, tuna salad, mediterranean vegetable, and grilled chicken
    caesar wraps.''',
    price="$59.99",
    selection=SecondSelection)
session.add(SignatureWrapPlatter)
session.commit()
SignatureWrapFeast = MenuItem(
    user_id=1,
    name="Signature Wrap Feast",
    description='''Make it a feast and we’ll include a large tossed garden
    salad with balsamic vinaigrette, our signature smoked mozzarella pasta
    salad, and an assortment of tea cookies, brownies and dessert bars. Our
    Signature Wraps include double honey turkey, tuna salad, mediterranean
    vegetable, and grilled chicken caesar wraps.''',
    price="$99.99",
    selection=SecondSelection)
session.add(SignatureWrapFeast)
session.commit()
EuropeanSandwichPlatter = MenuItem(
    user_id=1,
    name="European Sandwich Platter",
    description='''Sophisticated fillings stacked between slices of fresh-baked
    ciabatta bread: Chicken & Gouda, Prosciutto Caprese, Grilled Vegetable with
    Chevre, Mediterranean Tuna, and Genoa Salami & Provolone.''',
    price="$59.99",
    selection=SecondSelection)
session.add(EuropeanSandwichPlatter)
session.commit()
EuropeanSandwichFeast = MenuItem(
    user_id=1,
    name="European Sandwich Feast",
    description='''Make it a feast and we’ll include a large tossed garden
    salad with balsamic vinaigrette, our signature smoked mozzarella pasta
    salad, and an assortment of tea cookies, brownies and dessert bars. Our
    European Sandwich Platter is sophisticated fillings stacked between slices
    of fresh-baked ciabatta bread: Chicken & Gouda, Prosciutto Caprese, Grilled
    Vegetable with Chevre, Mediterranean Tuna, and Genoa Salami &
    Provolone.''',
    price="$99.99",
    selection=SecondSelection)
session.add(EuropeanSandwichFeast)
session.commit()
BoxLunchChickenAvocadoHoagie = MenuItem(
    user_id=1,
    name='''Box Lunch: Chicken Avocado Hoagie''',
    description='''Our chicken avocado hoagie along with fruit salad, potato
    chips and a freshly baked cookie. Includes plastic flatware and paper
    napkins.''',
    price="$12.99",
    selection=SecondSelection)
session.add(BoxLunchChickenAvocadoHoagie)
session.commit()
BoxLunchDoubleHoneyTurkeyWrap = MenuItem(
    user_id=1,
    name='''Box Lunch: Double Honey Turkey Wrap''',
    description='''Our double honey turkey wrap along with fruit salad, potato
    chips and a freshly baked cookie. Includes plastic flatware and paper
    napkins.''',
    price="$12.99",
    selection=SecondSelection)
session.add(BoxLunchDoubleHoneyTurkeyWrap)
session.commit()
BoxLunchMediterraneanVegetableWrap = MenuItem(
    user_id=1,
    name='''Box Lunch: Mediterranean Vegetable Wrap''',
    description='''Our mediterranean vegetable wrap along with fruit salad,
    potato chips and a freshly baked cookie. Includes plastic flatware and
    paper napkins.''',
    price="$12.99",
    selection=SecondSelection)
session.add(BoxLunchMediterraneanVegetableWrap)
session.commit()
BoxLunchClassicHoagie = MenuItem(
    user_id=1,
    name='''Box Lunch: Classic Hoagie''',
    description='''Our classic Italian hoagie along with fruit salad, potato
    chips and a freshly baked cookie. Includes plastic flatware and paper
    napkins.''',
    price="$12.99",
    selection=SecondSelection)
session.add(BoxLunchClassicHoagie)
session.commit()

ThirdSelection = Selection(
    user_id=1,
    name="Sushi")
session.add(ThirdSelection)
session.commit()
NigiriAndRollClassicPlatterSmallWhiteRice = MenuItem(
    user_id=1,
    name='''Nigiri And Roll Classic Platter: Small White Rice''',
    description='''Traditional Sushi 4pc Tuna Nigiri, 4pc Salmon Nigiri, 4pc
    Shrimp Nigiri, 4pc Salmon Avocado Roll, 4pc Avocado Cucumber Roll, 8pc
    California with Masago''',
    price="$41.99",
    selection=ThirdSelection)
session.add(NigiriAndRollClassicPlatterSmallWhiteRice)
session.commit()
NigiriAndRollClassicPlatterLargeWhiteRice = MenuItem(
    user_id=1,
    name='''Nigiri And Roll Classic Platter: Large White Rice''',
    description='''Traditional Sushi 4pc Tuna Nigiri, 4pc Salmon Nigiri, 4pc
    Shrimp Nigiri, 4pc Albacore Nigiri, 8pc Cucumber Roll, 8pc Tuna Roll, 8pc
    Salmon Roll, 8pc California with Masago''',
    price="$54.99",
    selection=ThirdSelection)
session.add(NigiriAndRollClassicPlatterLargeWhiteRice)
session.commit()
NigiriAndRollClassicPlatterSmallBrownRice = MenuItem(
    user_id=1,
    name='''Nigiri And Roll Classic Platter: Small Brown Rice''',
    description='''Traditional Sushi 4pc Tuna Nigiri, 4pc Salmon Nigiri, 4pc
    Shrimp Nigiri, 4pc Salmon Avocado Roll, 4pc Avocado Cucumber Roll, 8pc
    California with Masago''',
    price="$43.99",
    selection=ThirdSelection)
session.add(NigiriAndRollClassicPlatterSmallBrownRice)
session.commit()
NigiriAndRollClassicPlatterLargeBrownRice = MenuItem(
    user_id=1,
    name='''Nigiri And Roll Classic Platter: Large Brown Rice''',
    description='''Traditional Sushi. 4pc Tuna Nigiri, 4pc Salmon Nigiri, 4pc
    Shrimp Nigiri, 4pc Albacore Nigiri, 8pc Cucumber Roll, 8pc Tuna Roll, 8pc
    Salmon Roll, 8pc California with Masago''',
    price="$57.99",
    selection=ThirdSelection)
session.add(NigiriAndRollClassicPlatterLargeBrownRice)
session.commit()
SupaDupaDeluxePlatterSmallWhiteRice = MenuItem(
    user_id=1,
    name='''Supa Dupa Deluxe Platter: Small White Rice''',
    description='''Premium Sushi 4pc Red Dragon Crunch Roll, 4pc Pink Dragon
    Crunch Roll, 8pc Shrimp Tempura Mango Roll, 4pc Cucumber Roll, 4pc Avocado
    Roll, 4pc Tuna Roll, 4pc Salmon Roll''',
    price="$36.99",
    selection=ThirdSelection)
session.add(SupaDupaDeluxePlatterSmallWhiteRice)
session.commit()
SupaDupaDeluxePlatterLargeWhiteRice = MenuItem(
    user_id=1,
    name='''Supa Dupa Deluxe Platter: Large White Rice''',
    description='''Premium Sushi 8pc Green Dragon Crunch Roll, 8pc California
    Roll, 8pc Shrimp Tempura Mango Roll, 4pc Red Dragon Crunch Roll, 4pc Pink
    Dragon Crunch Roll, 4pc Salmon Roll, 4pc Cucumber Roll, 4pc Avocado Roll,
    4pc Tuna Roll''',
    price="$47.99",
    selection=ThirdSelection)
session.add(SupaDupaDeluxePlatterLargeWhiteRice)
session.commit()
SupaDupaDeluxePlatterSmallBrownRice = MenuItem(
    user_id=1,
    name='''Supa Dupa Deluxe Platter: Small Brown Rice''',
    description='''Premium Sushi 4pc Red Dragon Crunch Roll, 4pc Pink Dragon
    Crunch Roll, 8pc Shrimp Tempura Mango Roll, 4pc Cucumber Roll, 4pc Avocado
    Roll, 4pc Tuna Roll, 4pc Salmon Roll''',
    price="$38.99",
    selection=ThirdSelection)
session.add(SupaDupaDeluxePlatterSmallBrownRice)
session.commit()
SupaDupaDeluxePlatterLargeBrownRice = MenuItem(
    user_id=1,
    name='''Supa Dupa Deluxe Platter: Large Brown Rice''',
    description='''Premium Sushi 8pc Green Dragon Crunch Roll, 8pc California
    Roll, 8pc Shrimp Tempura Mango Roll, 4pc Red Dragon Crunch Roll, 4pc Pink
    Dragon Crunch Roll, 4pc Salmon Roll, 4pc Cucumber Roll, 4pc Avocado Roll,
    4pc Tuna Roll''',
    price="$50.99",
    selection=ThirdSelection)
session.add(SupaDupaDeluxePlatterLargeBrownRice)
session.commit()
VeryVeggieSushiPlatterSmallWhiteRice = MenuItem(
    user_id=1,
    name='''Very Veggie Sushi Platter: Small White Rice''',
    description='''Vegan Vegetarian Friendly 4pc Veggie Dragon Roll, 8pc Purple
    Basil Veggie Roll, 8pc Avocado Cucumber Roll, 8pc Veggie Roll, 8pc Avocado
    Roll, 8pc Carrot Roll, Our own Ginger Miso Dressing to dip''',
    price="$24.49",
    selection=ThirdSelection)
session.add(VeryVeggieSushiPlatterSmallWhiteRice)
session.commit()
VeryVeggieSushiPlatterLargeWhiteRice = MenuItem(
    user_id=1,
    name='''Very Veggie Sushi Platter: Small White Rice''',
    description='''Vegan Vegetarian Friendly 8pc Purple Basil Veggie Roll, 8pc
    Veggie Roll, 8pc Veggie Dragon Roll, 8pc Avocado Cucumber Roll, 8pc Carrot
    Roll, 8pc Cucumber Roll, 2pc Inari, Our own Ginger Miso Dressing to dip''',
    price="$35.99",
    selection=ThirdSelection)
session.add(VeryVeggieSushiPlatterLargeWhiteRice)
session.commit()
VeryVeggieSushiPlatterSmallBrownRice = MenuItem(
    user_id=1,
    name='''Very Veggie Sushi Platter: Small Brown Rice''',
    description='''Vegan Vegetarian Friendly 4pc Veggie Dragon Roll, 8pc Purple
    Basil Veggie Roll, 8pc Avocado Cucumber Roll, 8pc Veggie Roll, 8pc Avocado
    Roll, 8pc Carrot Roll, Our own Ginger Miso Dressing to dip''',
    price="$26.99",
    selection=ThirdSelection)
session.add(VeryVeggieSushiPlatterSmallBrownRice)
session.commit()
VeryVeggieSushiPlatterLargeBrownRice = MenuItem(
    user_id=1,
    name='''Very Veggie Sushi Platter: Large Brown Rice''',
    description='''Vegan Vegetarian Friendly 8pc Purple Basil Veggie Roll,
    8pc Veggie Roll, 8pc Veggie Dragon Roll, 8pc Avocado Cucumber Roll,
    8pc Carrot Roll, 8pc Cucumber Roll, 2pc Inari, Our own Ginger Miso Dressing
    to dip''',
    price="$39.99",
    selection=ThirdSelection)
session.add(VeryVeggieSushiPlatterLargeBrownRice)
session.commit()

FourthSelection = Selection(
    user_id=1,
    name="Desserts & Cakes")
session.add(FourthSelection)
session.commit()
ElegantDessertPlatter = MenuItem(
    user_id=1,
    name='''Elegant Dessert Platter''',
    description='''A delightful assortment of miniature pastries including
    jewel-like fruit tarts, cheesecakes and éclairs.''',
    price="$45.99",
    selection=FourthSelection)
session.add(ElegantDessertPlatter)
session.commit()
TeaCookiesBars = MenuItem(
    user_id=1,
    name='''Tea Cookies & Bars''',
    description='''Turtle pecan bars, chocolate chip shortbread, checkerboard
    cookies, carrot cake and lemon bars, and almond horns, piled high with a
    fresh fruit garnish.''',
    price="$29.99",
    selection=FourthSelection)
session.add(TeaCookiesBars)
session.commit()
BrowniesBars = MenuItem(
    user_id=1,
    name='''Brownies & Bars''',
    description='''Lemon bars, fudge brownies, peanut butter bars and walnut
    brownies, piled high with a fresh fruit garnish.''',
    price="$29.99",
    selection=FourthSelection)
session.add(BrowniesBars)
session.commit()
JumboCookies = MenuItem(
    user_id=1,
    name='''Jumbo Cookies''',
    description='''A selection of our jumbo sized cookies, including double
    chocolate chip, snickerdoodle and oatmeal raisin.''',
    price="$15.99",
    selection=FourthSelection)
session.add(JumboCookies)
session.commit()
SheetCakeChocolate = MenuItem(
    user_id=1,
    name='''Sheet Cake: Chocolate''',
    description='''Rich chocolate cake layered and covered with chocolate
    buttercream icing. If you wish to have your decoration customized, please
    call the store and ask to speak to the Bakery.''',
    price="$40.00",
    selection=FourthSelection)
session.add(SheetCakeChocolate)
session.commit()
SheetCakeVanilla = MenuItem(
    user_id=1,
    name='''Sheet Cake: Vanilla''',
    description='''Moist vanilla cake layered and covered with vanilla
    buttercream icing. If you wish to have your decoration customized, please
    call the store and ask to speak to the Bakery.''',
    price="$40.00",
    selection=FourthSelection)
session.add(SheetCakeVanilla)
session.commit()
SheetCakeStrawberryandCream = MenuItem(
    user_id=1,
    name='''Sheet Cake: Strawberry and Cream''',
    description='''Moist yellow cake layered with whipped cream and
    strawberries, covered in sweetened whipped cream and garnished with glazed
    strawberries.''',
    price="$49.99",
    selection=FourthSelection)
session.add(SheetCakeStrawberryandCream)
session.commit()
SheetCakeFreshFruit = MenuItem(
    user_id=1,
    name='''Sheet Cake: Fresh Fruit''',
    description='''Moist yellow cake layered with whipped cream and berries,
    covered in sweetened whipped cream and garnished with glazed seasonal fresh
    fruit.''',
    price="$50.00",
    selection=FourthSelection)
session.add(SheetCakeFreshFruit)
session.commit()

FifthSelection = Selection(
    user_id=1,
    name="Breakfast & Brunch")
session.add(FifthSelection)
session.commit()
LargeBagelPlatter = MenuItem(
    user_id=1,
    name='''Large Bagel Platter''',
    description='''Cinnamon Raisin Bagel: 280 calories per 1 ea, Honey Wheat
    Bagel: 270 calories per 1 ea, Onion Bagel: 280 calories per 1 ea, Plain
    Bagel: 280 calories per 1 ea''',
    price="$50.00",
    selection=FifthSelection)
session.add(LargeBagelPlatter)
session.commit()
BreakfastTreats = MenuItem(
    user_id=1,
    name='''Breakfast Treats''',
    description='''An assortment of our muffins, croissants and danish.''',
    price="$25.99",
    selection=FifthSelection)
session.add(BreakfastTreats)
session.commit()

print("Menu items added!")
