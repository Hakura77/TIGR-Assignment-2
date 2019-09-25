#Bad Smells Detected
1. Bad smells: Long Method
     - Category:  Bloater 
     - Location: TigrParser.py line 22-71
     - Reasons:  
         1. the method parse has 51 lines, which can not fit in one screen.
         2. the method code will be hard to understand and maintained by other developer.
         3. against the single responsible principle. 
 - Strategy: extract the long method into small methods

2. Bad smells: Feature Envy
     - Category: Couplers 
     - Location: TigrParser.py line 62 self.drawer.__getattribute__
     - Reasons: break encapsulation of drawer
     - Strategy: make a method in class TigrParser to use instead of using the using Drawers
     private method
     
3. Bad smells: Duplicate Code
     - Category: Dispensables
     - Location: all the error handling in TigrParser.py and TigrReader.py
     - Reasons: 
                1.The error handling is all over the place
                2.It's difficult to read and maintain the code
     - Strategy: extract all the Error handling into a class ErrorHandle


 