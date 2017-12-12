# MealPlannerApp
Meal planner prep app

----
Web app that enables users to use a personal calendar to plan out their meals.

Requirements:
1) Python
2) Django
3) Selenium for python
4) Firefox

----

Set Up Instructions:

```python
pip install django

pip install selenium
```



To run test case:
```
python functional_test.py
```

This test case was created to test if selenium is working properly. Use this before installing selenium to get an error. If used after installing selenium, should open up an empty firefox window with address pointing to localhost:8000/


Start project:
```python
python manage.py runserver
```
Use this when in FreeRangeHuman/src directory to start server.
Then go to http://localhost:8000/ to verify django is working!


Run tests:
```python
python manage.py test
```
