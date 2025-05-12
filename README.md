# ShiftGrid Trading Robot

The price of market assets is constantly affected by many random, unpredictable events. Often, various complex analysis schemes do not provide any advantages over classical trading methods that have been proven for decades. The result of hard work and long-term experiments was the creation of a fully autonomous ShiftGrid trading robot using a significantly modified Grid strategy. After a simple parameter setting, the launched robot no longer needs any user control actions, bringing a profit every day.

The basis of the ShiftGrid strategy is trading on a grid of asset price levels. At any given time, the robot has two active pending orders: one to buy below the current price, the other to sell above the current price. The robot constantly monitors the status of orders. When one of the orders is executed, the robot cancels the second order and places two new orders. The price range between the grid levels and the number of these levels are configurable by the user. You can set up both a uniform grid and a variable pitch (in any mathematical progression or arbitrarily).

